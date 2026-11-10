import unittest
from geometry_check import conditional_geometry

class GeometryControls(unittest.TestCase):
    def test_exact_report_arithmetic(self):
        r=conditional_geometry()
        self.assertEqual(r["centered_web_clearance_threshold_inches"],"6.290")
        self.assertEqual(r["lateral_distance_between_first_contact_and_web_clearance_inches"],"2.612")
        self.assertEqual(r["inferred_east_gap_in_this_cross_section_inches"],"2.702")
    def test_unknown_engagement_not_prevention(self):
        self.assertIsNone(conditional_geometry()["prevents_rigid_translation_in_this_idealization"])
    def test_axial_miss_not_contact(self):
        self.assertFalse(conditional_geometry(axially_engaged=False,vertically_engaged=True,resistance_verified=True)["actual_contact_established"])
    def test_vertical_miss_not_contact(self):
        self.assertFalse(conditional_geometry(axially_engaged=True,vertically_engaged=False,resistance_verified=True)["actual_contact_established"])
    def test_engagement_without_capacity_not_prevention(self):
        self.assertIsNone(conditional_geometry(axially_engaged=True,vertically_engaged=True)["prevents_rigid_translation_in_this_idealization"])
    def test_fully_assumed_rigid_stop(self):
        r=conditional_geometry(axially_engaged=True,vertically_engaged=True,resistance_verified=True)
        self.assertTrue(r["prevents_rigid_translation_in_this_idealization"])
        self.assertEqual(r["historical_walkoff_prevention"],"not determined")
    def test_late_contact(self):
        r=conditional_geometry(west_gap="7",inside_plate_width="25",axially_engaged=True,vertically_engaged=True,resistance_verified=True)
        self.assertFalse(r["interception_precedes_web_clearance_in_projection"])
    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):conditional_geometry(west_gap="-1")
    def test_repeatability(self):
        self.assertEqual(conditional_geometry(),conditional_geometry())

if __name__=="__main__":unittest.main(verbosity=2)
