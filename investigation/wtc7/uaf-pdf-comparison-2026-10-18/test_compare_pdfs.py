"""In-memory synthetic controls, before inspecting the historical pair."""
import unittest
import fitz
from compare_pdfs import digest, page_record

def fixture(text="control", color=(1, 0, 0), producer="control A"):
    doc = fitz.open()
    page = doc.new_page(width=200, height=200)
    page.insert_text((20, 40), text)
    page.draw_rect(fitz.Rect(20, 70, 60, 100), color=color, fill=color)
    doc.set_metadata({"producer": producer})
    return doc.tobytes()

def measured(b):
    with fitz.open(stream=b, filetype="pdf") as doc:
        if doc.is_repaired:
            raise ValueError("repaired fixture rejected")
        return page_record(doc[0])[0]

class Controls(unittest.TestCase):
    def test_metadata_only(self):
        a, b = fixture(), fixture(producer="control B")
        self.assertNotEqual(digest(a), digest(b))
        for channel in ["raw_text", "normalized_text", "raster"]:
            self.assertEqual(measured(a)[channel], measured(b)[channel])

    def test_text(self):
        a, b = measured(fixture()), measured(fixture(text="changed"))
        self.assertNotEqual(a["raw_text"], b["raw_text"])
        self.assertNotEqual(a["raster"], b["raster"])

    def test_graphics(self):
        a, b = measured(fixture()), measured(fixture(color=(0, 0, 1)))
        self.assertEqual(a["raw_text"], b["raw_text"])
        self.assertNotEqual(a["raster"], b["raster"])

    def test_malformed(self):
        with self.assertRaises(Exception):
            measured(b"%PDF-1.4\nnot a complete document")

    def test_truncated(self):
        with self.assertRaises(Exception):
            measured(fixture()[:80])

    def test_failed_extraction_is_failure(self):
        class Failed:
            def get_text(self, *args, **kwargs):
                raise RuntimeError("deliberate extraction failure")
        with self.assertRaises(RuntimeError):
            page_record(Failed())

    def test_repeatability(self):
        b = fixture()
        self.assertEqual(measured(b), measured(b))

if __name__ == "__main__":
    unittest.main(verbosity=2)
