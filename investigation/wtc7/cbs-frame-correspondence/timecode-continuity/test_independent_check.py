"""Synthetic controls only; imports no production arithmetic or historical data."""

import copy
import unittest

import independent_check as check


def packed(h, m, s, f, drop=False, flags=0):
    # Synthetic writer for known numeric components, not used by the auditor.
    out = bytearray([0x13])
    for value in (f, s, m, h):
        out.append((value // 10) * 16 + value % 10)
    out[1] |= 0x40 if drop else 0
    word = int.from_bytes(out[1:], "big") | flags
    return "13" + word.to_bytes(4, "big").hex()


def fixtures(values, clip=1, text="00;00;00;00"):
    document = {"clip": clip, "result": {"frames": len(values), "target_variants": [
        {"area": "subcode", "raw_hex": raw, "occurrences": 40,
         "first_frame": i, "last_frame": i, "frames_present": 1}
        for i, raw in enumerate(values)]}}
    header = {"clip": clip, "video_header": {"scale": 333673, "rate": 10000000,
                                             "length": len(values)},
              "fields": {key: [{"prefix_utf8": text}] for key in ("tc_O", "tc_A")}}
    return document, header


class IndependentTests(unittest.TestCase):
    def test_byte_order_masks_and_positional_flags(self):
        row = check.decode(packed(12, 34, 56, 21, True, 0x808080c0))
        self.assertEqual(row["components_h_m_s_f"], [12, 34, 56, 21])
        self.assertEqual(row["positional_flag_hex"], "c08080c0")
        self.assertTrue(row["drop_bit"])
        self.assertFalse(row["component_issues"])

    def test_each_invalid_bcd_is_null_not_zero(self):
        for index, name in enumerate(("f", "s", "m", "h"), 1):
            with self.subTest(name=name):
                raw = bytearray.fromhex(packed(0, 0, 0, 0))
                raw[index] = 0x0a
                row = check.decode(raw.hex())
                self.assertIn(name + "_invalid_bcd", row["component_issues"])
                self.assertIn(name + "_range", row["component_issues"])
                self.assertIsNone(row["components_h_m_s_f"][("h", "m", "s", "f").index(name)])
                self.assertTrue(all(row[lane] is None for lane in check.LANES))

    def test_each_out_of_range_component(self):
        for parts, issue in (([24, 0, 0, 0], "h_range"), ([0, 60, 0, 0], "m_range"),
                             ([0, 0, 60, 0], "s_range"), ([0, 0, 0, 30], "f_range")):
            row = check.decode(packed(*parts))
            self.assertIn(issue, row["component_issues"])
            self.assertIsNone(row["selected"])

    def test_all_ones_invalid_and_no_payload_repair(self):
        row = check.decode("13ffffffff")
        self.assertEqual(row["components_h_m_s_f"], [None] * 4)
        self.assertIsNone(row["selected"])
        for raw in ("ffffffff", "12ffffffff", "13FFFFFFFF", "13ff", None):
            with self.assertRaises(ValueError):
                check.decode(raw)

    def test_drop_minute_tenth_hour_and_day_ordinals(self):
        cases = [([0, 0, 59, 29], 1799), ([0, 1, 0, 2], 1800),
                 ([0, 9, 59, 29], 17981), ([0, 10, 0, 0], 17982),
                 ([0, 59, 59, 29], 107891), ([1, 0, 0, 0], 107892),
                 ([23, 59, 59, 29], 2589407)]
        for parts, expected in cases:
            self.assertEqual(check.ordinal(parts, True), (expected, []))
        self.assertEqual(check.ordinal([23, 59, 59, 29], False), (2591999, []))

    def test_omitted_label_does_not_invalidate_forced_nd(self):
        for frame in (0, 1):
            row = check.decode(packed(0, 1, 0, frame, True))
            self.assertEqual(row["nd"], 1800 + frame)
            self.assertIsNone(row["df"])
            self.assertIsNone(row["selected"])
            self.assertEqual(row["selected_issues"], ["omitted_drop_frame_label"])

    def test_enumerate_complete_ten_minute_labels(self):
        expected = 0
        for minute in range(10):
            for second in range(60):
                for frame in range(30):
                    if minute and second == 0 and frame < 2:
                        continue
                    self.assertEqual(check.ordinal([0, minute, second, frame], True)[0], expected)
                    expected += 1
        self.assertEqual(expected, 17982)

    def test_transition_gaps_repeats_flags_and_backward_jumps(self):
        values = [packed(0, 0, 0, 1), packed(0, 0, 0, 2),
                  packed(0, 0, 0, 2, flags=0x80000000), packed(0, 0, 0, 5),
                  packed(0, 0, 0, 0)]
        result = check.compute_clip(*fixtures(values, text="00;00;00;01"))
        self.assertEqual([e["selected_delta"] for e in result["transitions"]], [1, 0, 3, -5])
        self.assertEqual(result["summary"]["lanes"]["selected"]["non_one_step_right_frames"], [2, 3, 4])
        self.assertEqual(result["summary"]["flag_change_right_frames"], [2, 3])

    def test_mode_change_keeps_raw_difference_but_unavailable_transition(self):
        rows = [check.decode(packed(0, 0, 0, 0)), check.decode(packed(0, 0, 0, 1, True))]
        edge = check.transitions(rows)[0]
        self.assertEqual(edge["selected_raw_difference"], 1)
        self.assertIsNone(edge["selected_delta"])
        self.assertTrue(edge["drop_bit_changed"])

    def test_possible_daily_wrap_is_not_unwrapped(self):
        for drop, modulus in ((False, 2592000), (True, 2589408)):
            rows = [check.decode(packed(23, 59, 59, 29, drop)),
                    check.decode(packed(0, 0, 0, 0, drop))]
            edge = check.transitions(rows)[0]
            self.assertEqual(edge["selected_delta"], 1 - modulus)
            self.assertTrue(edge["selected_possible_daily_rollover"])

    def test_missing_conflicting_nonunique_or_wrong_population_rejected(self):
        doc, _ = fixtures([packed(0, 0, 0, 1), packed(0, 0, 0, 2)])
        variants = []
        missing = copy.deepcopy(doc); missing["result"]["target_variants"].pop(); variants.append(missing)
        conflict = copy.deepcopy(doc); conflict["result"]["target_variants"].append(copy.deepcopy(conflict["result"]["target_variants"][0])); variants.append(conflict)
        nonunique = copy.deepcopy(doc); nonunique["result"]["target_variants"][1]["raw_hex"] = nonunique["result"]["target_variants"][0]["raw_hex"]; variants.append(nonunique)
        for key, value in (("frames_present", True), ("occurrences", 39),
                           ("first_frame", -1), ("last_frame", 1), ("area", "vaux")):
            wrong = copy.deepcopy(doc); wrong["result"]["target_variants"][0][key] = value; variants.append(wrong)
        for wrong in variants:
            with self.assertRaises(ValueError):
                check.reconstruct(wrong, 2)

    def test_strict_native_label_and_rational_spans(self):
        for text in ("00:00:00:00", "００;00;00;00", "00;00;00;00\n", None):
            self.assertTrue(check.parse_header(text)["issues"])
        values = [packed(0, 0, 0, 0), packed(0, 0, 0, 1)]
        result = check.compute_clip(*fixtures(values))
        summary = result["summary"]
        self.assertEqual(summary["first_to_last_avi_span"], "333673/10000000")
        self.assertEqual(summary["container_duration_avi"], "333673/5000000")
        self.assertEqual(summary["first_to_last_nominal_dv_span"], "1001/30000")
        self.assertEqual(summary["period_difference_avi_minus_nominal"], "19/30000000")
        for key in ("tc_O", "tc_A"):
            self.assertTrue(summary["header_comparisons"][key]["matches_first_components"])
        for key in ("scale", "rate", "length"):
            doc, header = fixtures(values)
            header["video_header"][key] = 0
            with self.assertRaises(ValueError):
                check.compute_clip(doc, header)

    def test_all_28_pairs_and_negative_overlap_positions(self):
        clips = [check.compute_clip(*fixtures([packed(0, 0, i, 0), packed(0, 0, i, 1)], i + 1))
                 for i in range(8)]
        pairs = check.compare_clips(clips)
        self.assertEqual(len(pairs), 28)
        first = pairs[0]["lanes"]["selected"]
        self.assertEqual(first, {"start_difference": 30, "all_left_ordinals_before_right": True,
                                 "boundary_counter_distance": 29, "unrepresented_counter_positions": 28})
        reversed_pair = check.compare_clips([clips[1], clips[0]])[0]["lanes"]["selected"]
        self.assertEqual(reversed_pair["unrepresented_counter_positions"], -32)
        self.assertFalse(reversed_pair["all_left_ordinals_before_right"])

    def test_mixed_mode_interclip_is_unavailable_only_for_selected(self):
        a = check.compute_clip(*fixtures([packed(0, 0, 0, 0)], 1))
        b = check.compute_clip(*fixtures([packed(0, 0, 0, 1, True)], 2))
        lanes = check.compare_clips([a, b])[0]["lanes"]
        self.assertIsNone(lanes["selected"])
        self.assertIsNotNone(lanes["nd"])
        self.assertIsNotNone(lanes["df"])

    def test_material_mismatch_and_unknown_fields_rejected(self):
        expected = {"value": 1, "component_issues": ["h_range", "h_invalid_bcd"]}
        check.compare({"value": 1, "component_issues": ["h_invalid_bcd", "h_range"]}, expected)
        for bad in ({"value": 2, "component_issues": expected["component_issues"]},
                    {**expected, "extra": True}, {"value": True, "component_issues": expected["component_issues"]}):
            with self.assertRaises(ValueError):
                check.compare(bad, expected)


if __name__ == "__main__":
    unittest.main()
