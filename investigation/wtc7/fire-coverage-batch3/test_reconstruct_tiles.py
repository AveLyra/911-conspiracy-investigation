"""Synthetic geometry controls; no historical image pixels are read."""
import copy
import unittest
import reconstruct_tiles as subject


def tiles():
    result=[]
    y=720.0
    for i,h in enumerate([39]*16+[37]):
        d=h*0.5
        y-=d
        result.append({"asset_id": f"synthetic-{i}", "native_pdf_dimensions": [975,h],
                       "object_reference": {"object_id":i,"generation":0},
                       "extracted_view": {"mode":"RGB"}, "colorspace":"/DeviceRGB", "bits_per_component":8,
                       "masks":[], "invocations":[{"physical_page":252,"ctm":[467.9,0,0,d,72.1,y],
                       "clipping_operator_seen_in_current_stream_state":False}]})
    return result


class GeometryControls(unittest.TestCase):
    def test_perfect_geometry_accepts_shuffled_order(self):
        t=tiles()[::-1]
        ordered,r=subject.geometry(t)
        self.assertTrue(r["accepted"])
        self.assertEqual([x["asset_id"] for x in ordered],[x["asset_id"] for x in tiles()])
        self.assertEqual(r["dimensions"],[975,661])

    def test_scale_mismatch_fails_even_when_joins_are_contiguous(self):
        t=tiles()
        t[-1]["invocations"][0]["ctm"][3]+=0.038
        t[-1]["invocations"][0]["ctm"][5]-=0.038
        _,r=subject.geometry(t)
        self.assertFalse(r["accepted"])
        self.assertEqual(r["tiles"][-1]["preceding_join_residual_points"],0)
        self.assertIn("common vertical scale mismatch",r["tiles"][-1]["failures"])

    def test_each_transform_mask_color_width_and_gap_gate(self):
        mutations=[lambda x:x["invocations"][0]["ctm"].__setitem__(0,467),
                   lambda x:x["invocations"][0]["ctm"].__setitem__(1,0.01),
                   lambda x:x["invocations"][0]["ctm"].__setitem__(3,-19.5),
                   lambda x:x["invocations"][0]["ctm"].__setitem__(4,72.2),
                   lambda x:x["invocations"][0]["ctm"].__setitem__(5,680),
                   lambda x:x.update(masks=[1]),
                   lambda x:x.update(colorspace="/DeviceGray"),
                   lambda x:x["native_pdf_dimensions"].__setitem__(0,974),
                   lambda x:x["invocations"][0].update(clipping_operator_seen_in_current_stream_state=True)]
        for mutate in mutations:
            t=copy.deepcopy(tiles()); mutate(t[1])
            self.assertFalse(subject.geometry(t)[1]["accepted"])


if __name__=="__main__": unittest.main(verbosity=2)
