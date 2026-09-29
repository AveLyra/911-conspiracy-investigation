#!/usr/bin/env python3
"""Synthetic-only registration controls; not a graph digitizer or viewer.

Rectangles are exact closed envelopes of pixel-cell footprints. Image edges
range from 0 to width/height; pixel indices range only to width/height minus 1.
Boundary-only strip contacts are retained and labeled, not usable pixel areas.
All geometric candidates remain visibility-unverified.
"""
import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import io
import json
from pathlib import Path
import platform
import sys
import unittest


def rational(value):
    if type(value) is int:
        return F(value)
    if type(value) is F:
        return value
    raise ValueError("exact integer or Fraction required; no booleans/floats")


def dimensions(width, height):
    if type(width) is not int or type(height) is not int or min(width, height) <= 0:
        raise ValueError("positive integer dimensions required")
    return width, height


def rectangle(values, allow_flat=False):
    if not isinstance(values, (tuple, list)) or len(values) != 4:
        raise ValueError("rectangle requires four exact edges")
    x0, y0, x1, y1 = map(rational, values)
    if x1 < x0 or y1 < y0 or (not allow_flat and (x1 == x0 or y1 == y0)):
        raise ValueError("reversed or empty rectangle")
    return x0, y0, x1, y1


@dataclass(frozen=True)
class Strip:
    name: str
    width: int
    height: int
    ctm: tuple

    def __post_init__(self):
        dimensions(self.width, self.height)
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("explicit strip identity required")
        if not isinstance(self.ctm, (tuple, list)) or len(self.ctm) != 6:
            raise ValueError("six CTM coefficients required")
        a, b, c, d, e, f = map(rational, self.ctm)
        if a <= 0 or d <= 0 or b != 0 or c != 0:
            raise ValueError("only positive-axis, unrotated CTMs admitted")
        object.__setattr__(self, "ctm", (a, b, c, d, e, f))

    @property
    def bbox(self):
        a, _, _, d, e, f = self.ctm
        return e, f, e + a, f + d

    def image_to_pdf(self, u, v):
        u, v = rational(u), rational(v)
        if not (0 <= u <= self.width and 0 <= v <= self.height):
            raise ValueError("native image edge outside strip")
        a, _, _, d, e, f = self.ctm
        return e + a * u / self.width, f + d * (1 - v / self.height)

    def pdf_to_image(self, x, y):
        x, y = rational(x), rational(y)
        a, _, _, d, e, f = self.ctm
        if not (e <= x <= e + a and f <= y <= f + d):
            raise ValueError("PDF point outside strip footprint")
        return self.width * (x - e) / a, self.height * (1 - (y - f) / d)

    def inverse_rect(self, rect):
        x0, y0, x1, y1 = rectangle(rect, allow_flat=True)
        u0, v1 = self.pdf_to_image(x0, y0)
        u1, v0 = self.pdf_to_image(x1, y1)
        return u0, v0, u1, v1


def render_cell_pdf(x, y, width, height, page_box, extra_radius=0):
    """Exact footprint plus declared extra render-pixel radius; no JPEG error model."""
    dimensions(width, height)
    if type(x) is not int or type(y) is not int or not (0 <= x < width and 0 <= y < height):
        raise ValueError("render pixel index outside raster")
    x0, y0, x1, y1 = rectangle(page_box)
    r = rational(extra_radius)
    if r < 0 or x - r < 0 or y - r < 0 or x + 1 + r > width or y + 1 + r > height:
        raise ValueError("uncertainty envelope outside raster")
    dx, dy = (x1 - x0) / width, (y1 - y0) / height
    return (x0 + (x - r) * dx, y1 - (y + 1 + r) * dy,
            x0 + (x + 1 + r) * dx, y1 - (y - r) * dy)


def candidates(pdf_rect, strips):
    """Geometric intersections only: never a visibility, curve or unique-owner claim."""
    x0, y0, x1, y1 = rectangle(pdf_rect)
    if not isinstance(strips, (tuple, list)) or not all(type(s) is Strip for s in strips):
        raise ValueError("explicit strip sequence required")
    if len({s.name for s in strips}) != len(strips):
        raise ValueError("duplicate strip identity")
    result = []
    for strip in strips:
        a0, b0, a1, b1 = strip.bbox
        overlap = max(x0, a0), max(y0, b0), min(x1, a1), min(y1, b1)
        if overlap[0] > overlap[2] or overlap[1] > overlap[3]:
            continue
        result.append({"strip": strip.name, "pdf_intersection": overlap,
                       "native_envelope": strip.inverse_rect(overlap),
                       "boundary_only": overlap[0] == overlap[2] or overlap[1] == overlap[3],
                       "visibility": "unverified"})
    return result


BARRIERS = {"clear", "crossing", "occlusion", "dash_gap", "clip", "overprint", "unknown"}


def support_rule(left_identity, right_identity, left_visible, right_visible, adjacent, barrier):
    """Policy guard on explicit declarations, not an image classifier."""
    for identity in (left_identity, right_identity):
        if identity is not None and (not isinstance(identity, str) or not identity.strip()):
            raise ValueError("identity must be an explicit nonblank label or None")
    if any(type(v) is not bool for v in (left_visible, right_visible, adjacent)):
        raise ValueError("visibility and adjacency require explicit booleans")
    if not isinstance(barrier, str) or barrier not in BARRIERS:
        raise ValueError("unknown support state")
    reasons = []
    if left_identity is None or right_identity is None:
        reasons.append("identity_unresolved")
    elif left_identity != right_identity:
        reasons.append("identity_change")
    if not left_visible or not right_visible:
        reasons.append("visibility_unresolved")
    if not adjacent:
        reasons.append("unsupported_gap")
    if barrier != "clear":
        reasons.append(barrier)
    return {"admit": not reasons, "reasons": reasons}


def synthetic_localization():
    """Known categorical raster marks, independently enumerated cell bounds.

    Build source bytes directly; replicate each source pixel three times on
    each axis by row construction, not by any PDF/strip transform. Locate the
    color by an exhaustive byte scan, then test the separate inverse mapping.
    No historical pixels, JPEG, antialiasing, overlay renderer or browser used.
    """
    width, height, scale = 17, 9, 3
    pixels = bytearray(width * height * 3)
    marks = {(0, 0): (255, 0, 0), (16, 8): (0, 255, 0), (7, 4): (0, 0, 255)}
    for (u, v), rgb in marks.items():
        pixels[3 * (v * width + u):3 * (v * width + u) + 3] = bytes(rgb)
    rows = []
    for v in range(height):
        row = b"".join(bytes(pixels[3 * (v * width + u):3 * (v * width + u) + 3]) * scale
                       for u in range(width))
        rows.extend([row] * scale)
    rendered = b"".join(rows)
    rw, rh = width * scale, height * scale
    strip = Strip("synthetic", width, height, (34, 0, 0, 18, 0, 0))
    checks = []
    for (u, v), rgb in marks.items():
        found = [(x, y) for y in range(rh) for x in range(rw)
                 if tuple(rendered[3 * (y * rw + x):3 * (y * rw + x) + 3]) == rgb]
        expected = [(x, y) for y in range(v * scale, (v + 1) * scale)
                    for x in range(u * scale, (u + 1) * scale)]
        if found != expected:
            raise AssertionError("synthetic mark raster localization failed")
        inverses = [strip.inverse_rect(render_cell_pdf(x, y, rw, rh, strip.bbox)) for x, y in found]
        envelope = (min(a[0] for a in inverses), min(a[1] for a in inverses),
                    max(a[2] for a in inverses), max(a[3] for a in inverses))
        if envelope != (u, v, u + 1, v + 1):
            raise AssertionError("synthetic inverse localization failed")
        checks.append({"source_cell": [u, v], "render_pixels": len(found), "native_envelope": envelope})
    return {"source_rgb_sha256": hashlib.sha256(pixels).hexdigest(),
            "replicated_rgb_sha256": hashlib.sha256(rendered).hexdigest(),
            "source_size": [width, height], "render_size": [rw, rh], "marks": checks}


class Controls(unittest.TestCase):
    def setUp(self):
        self.s = Strip("A", 100, 20, (50, 0, 0, 10, 10, 30))

    def test_01_known_corners_and_interior(self):
        for uv, xy in [((0, 0), (10, 40)), ((100, 20), (60, 30)), ((20, 6), (20, 37))]:
            self.assertEqual(self.s.image_to_pdf(*uv), xy)
            self.assertEqual(self.s.pdf_to_image(*xy), uv)

    def test_02_y_inversion_not_bottom_origin(self):
        self.assertEqual(self.s.pdf_to_image(10, 39), (0, 2))
        self.assertNotEqual(self.s.pdf_to_image(10, 39), (0, 18))

    def test_03_cell_edges_not_centers(self):
        self.assertEqual(self.s.inverse_rect((20, 36, F(41, 2), F(73, 2))), (20, 7, 21, 8))
        self.assertEqual(self.s.pdf_to_image(F(81, 4), F(145, 4)), (F(41, 2), F(15, 2)))

    def test_04_last_strip_nonuniform_height(self):
        ordinary = Strip("ordinary", 100, 20, (50, 0, 0, 10, 10, 30))
        final = Strip("final", 100, 20, (50, 0, 0, 8, 10, 30))
        self.assertEqual(ordinary.pdf_to_image(20, 34), (20, 12))
        self.assertEqual(final.pdf_to_image(20, 34), (20, 10))
        self.assertNotEqual(ordinary.pdf_to_image(20, 34), final.pdf_to_image(20, 34))

    def test_05_render_quantization_known_bounds(self):
        self.assertEqual(render_cell_pdf(0, 0, 1700, 2200, (0, 0, 612, 792)),
                         (0, F(19791, 25), F(9, 25), 792))
        self.assertEqual(render_cell_pdf(100, 200, 1000, 2000, (10, 20, 110, 220)),
                         (20, F(1999, 10), F(201, 10), 200))

    def test_06_quantization_plus_assessed_radius(self):
        q = render_cell_pdf(100, 200, 1000, 2000, (10, 20, 110, 220), F(1, 2))
        self.assertEqual(q, (F(399, 20), F(3997, 20), F(403, 20), F(4001, 20)))
        self.assertEqual(q[2] - q[0], F(1, 5))
        self.assertEqual(q[3] - q[1], F(1, 5))

    def test_07_seam_returns_both_positive_area(self):
        top = Strip("top", 100, 20, (50, 0, 0, 10, 10, 40))
        got = candidates((20, 39, 21, 41), [self.s, top])
        self.assertEqual([x["strip"] for x in got], ["A", "top"])
        self.assertEqual(got[0]["native_envelope"], (20, 0, 22, 2))
        self.assertEqual(got[1]["native_envelope"], (20, 18, 22, 20))
        self.assertTrue(all(not x["boundary_only"] and x["visibility"] == "unverified" for x in got))

    def test_08_boundary_contact_retained_but_labeled(self):
        top = Strip("top", 100, 20, (50, 0, 0, 10, 10, 40))
        got = candidates((20, 39, 21, 40), [self.s, top])
        self.assertEqual([x["boundary_only"] for x in got], [False, True])
        self.assertEqual(got[1]["native_envelope"], (20, 20, 22, 20))

    def test_09_overlap_does_not_choose_owner(self):
        same = Strip("other", 100, 20, self.s.ctm)
        got = candidates((20, 35, 21, 36), [self.s, same])
        self.assertEqual(len(got), 2)
        self.assertEqual(got[0]["native_envelope"], got[1]["native_envelope"])

    def test_10_outside_has_no_candidate(self):
        self.assertEqual(candidates((100, 100, 101, 101), [self.s]), [])

    def test_11_invalid_numeric_types(self):
        for value in (True, False, 1.0, float("nan"), float("inf"), "1", None):
            with self.subTest(kind=type(value).__name__), self.assertRaises(ValueError):
                rational(value)

    def test_12_invalid_ctms_dimensions_identity(self):
        for args in [("A", 0, 2, (1, 0, 0, 1, 0, 0)), ("", 2, 2, (1, 0, 0, 1, 0, 0)),
                     ("A", 2, 2, (0, 0, 0, 1, 0, 0)), ("A", 2, 2, (-1, 0, 0, 1, 0, 0)),
                     ("A", 2, 2, (1, 1, 0, 1, 0, 0)), ("A", 2, 2, (1, 0, 1, 1, 0, 0)),
                     ("A", 2, 2, (1, 0, 0, 1)), ("A", True, 2, (1, 0, 0, 1, 0, 0))]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                Strip(*args)

    def test_13_out_of_range_points(self):
        for point in [(-1, 0), (101, 0), (0, 21)]:
            with self.assertRaises(ValueError):
                self.s.image_to_pdf(*point)
        for point in [(9, 35), (61, 35), (20, 41)]:
            with self.assertRaises(ValueError):
                self.s.pdf_to_image(*point)

    def test_14_malformed_rectangles_and_duplicate_identity(self):
        for rect in [(1, 2, 3), (1, 2, 1, 3), (3, 2, 1, 4), (1, 4, 3, 2)]:
            with self.assertRaises(ValueError):
                candidates(rect, [self.s])
        with self.assertRaises(ValueError):
            candidates((20, 35, 21, 36), [self.s, self.s])

    def test_15_render_invalid_and_no_silent_clamp(self):
        for x, y, r in [(-1, 0, 0), (10, 0, 0), (0, 10, 0), (True, 0, 0),
                        (0, 0, 1), (5, 5, -1)]:
            with self.assertRaises(ValueError):
                render_cell_pdf(x, y, 10, 10, (0, 0, 10, 10), r)

    def test_16_conservative_support_clear_only(self):
        self.assertEqual(support_rule("red-solid", "red-solid", True, True, True, "clear"),
                         {"admit": True, "reasons": []})
        for reason in sorted(BARRIERS - {"clear"}):
            got = support_rule("red-solid", "red-solid", True, True, True, reason)
            self.assertEqual(got, {"admit": False, "reasons": [reason]})

    def test_17_ambiguity_not_numeric_error_bar(self):
        got = support_rule(None, "red-solid", True, True, True, "clear")
        self.assertEqual(got["reasons"], ["identity_unresolved"])
        self.assertFalse(got["admit"])
        self.assertFalse(support_rule("red-solid", "red-dashed", True, True, True, "clear")["admit"])

    def test_18_visibility_and_gaps_remain_unsupported(self):
        self.assertFalse(support_rule("A", "A", False, True, True, "clear")["admit"])
        self.assertFalse(support_rule("A", "A", True, True, False, "clear")["admit"])
        for args in [("", "A", True, True, True, "clear"), ("A", "A", 1, True, True, "clear"),
                     ("A", "A", True, True, True, "inferred-dash")]:
            with self.assertRaises(ValueError):
                support_rule(*args)

    def test_19_known_raster_localization(self):
        result = synthetic_localization()
        self.assertEqual(len(result["marks"]), 3)
        self.assertEqual(sum(x["render_pixels"] for x in result["marks"]), 27)

    def test_20_source_scale_not_render_precision(self):
        low = self.s.inverse_rect(render_cell_pdf(20, 7, 100, 20, self.s.bbox))
        high = self.s.inverse_rect(render_cell_pdf(40, 14, 200, 40, self.s.bbox))
        self.assertEqual(low, (20, 7, 21, 8))
        self.assertEqual(high, (20, 7, F(41, 2), F(15, 2)))
        # A smaller render footprint is not a claim of finer source resolution.
        self.assertEqual(self.s.width, 100)
        self.assertEqual(self.s.height, 20)


PINS = {
    "REGISTRATION-STAGE.md": "18e212edcf4950f370bd30119597b20f786015d61da03fe4aeb19b23125f004c",
    "NUMERICAL-PROTOCOL.md": "e03c47c1945b9eb9fd0a040d757d5f5f66bf76791ced8944323d3c92d1120df3",
    "HUMAN-REVIEW-GATE.md": "2e6f34d2e2d6d423c440c8a56b4a3c4796429d59f4d0baf0cf03609341a271ee",
    "technical-preparation.md": "a4d820f468dd80932f4144048eba545e70129f994c4b93e0f02f6a7f88e54550",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", help="exclusive-create registration-controls01.json in this directory")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    def hashes():
        actual = {name: hashlib.sha256((here / name).read_bytes()).hexdigest() for name in PINS}
        if actual != PINS:
            raise ValueError("changed instruction pin; controls not run")
        return actual
    before = hashes()
    code_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
    names = [t.id().split(".")[-1] for t in suite]
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=0).run(suite)
    receipt = {"status": "PASS" if result.wasSuccessful() else "FAIL", "scope": "synthetic-only",
               "python": platform.python_version(), "executable": sys.executable,
               "code_sha256": code_hash, "input_sha256": before, "test_count": result.testsRun,
               "test_names": names, "failures": [{"test": t.id(), "detail": d} for t, d in result.failures],
               "errors": [{"test": t.id(), "detail": d} for t, d in result.errors],
               "synthetic_raster": synthetic_localization() if result.wasSuccessful() else None,
               "historical_images_read": 0, "historical_ordinates": 0,
               "human_gate_satisfied": False, "browser_verified": False}
    if hashes() != before or hashlib.sha256(Path(__file__).read_bytes()).hexdigest() != code_hash:
        raise ValueError("inputs changed during controls")
    payload = json.dumps(receipt, indent=2, sort_keys=True, default=str) + "\n"
    if args.out:
        requested = Path(args.out)
        if requested.name != "registration-controls01.json" or requested.resolve().parent != here:
            raise ValueError("output outside this job's single owned receipt")
        with requested.open("x", encoding="utf-8") as stream:
            stream.write(payload)
    print(payload, end="")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
