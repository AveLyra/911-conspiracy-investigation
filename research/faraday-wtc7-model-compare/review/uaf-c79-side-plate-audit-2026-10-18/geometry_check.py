"""Conditional rigid in-plane geometry, not an engineering capacity solver."""
from decimal import Decimal
import json

def conditional_geometry(seat_width="12", web_thickness="0.580", west_gap="3.678", inside_plate_width="17.89", flange_width="11.510", axially_engaged=None, vertically_engaged=None, resistance_verified=False):
    seat, web, gap, inside, flange = map(Decimal, [seat_width,web_thickness,west_gap,inside_plate_width,flange_width])
    if min(seat,web,inside,flange)<=0 or gap<0 or inside<flange or gap>inside-flange:
        raise ValueError("Invalid dimensions for the specified idealization")
    threshold=seat/2+web/2
    margin=threshold-gap
    interception=margin>0
    engaged=axially_engaged is True and vertically_engaged is True
    if not interception or axially_engaged is False or vertically_engaged is False:
        prevention=False
    elif engaged and resistance_verified:
        prevention=True
    else:
        prevention=None
    return {
        "inputs_inches":dict(zip(["seat_width","web_thickness","west_gap","inside_plate_width","flange_width"],map(str,[seat,web,gap,inside,flange]))),
        "centered_web_clearance_threshold_inches":str(threshold),
        "west_first_contact_distance_inches":str(gap),
        "lateral_distance_between_first_contact_and_web_clearance_inches":str(margin),
        "inferred_east_gap_in_this_cross_section_inches":str(inside-flange-gap),
        "interception_precedes_web_clearance_in_projection":interception,
        "axially_engaged":axially_engaged,"vertically_engaged":vertically_engaged,
        "resistance_verified":resistance_verified,
        "actual_contact_established":engaged,
        "prevents_rigid_translation_in_this_idealization":prevention,
        "nullable_result_rule":"null means not established, not a finding that prevention fails",
        "historical_walkoff_prevention":"not determined",
        "limitations":["Report-stated dimensions, not independently measured as-built dimensions", "Centered seat/web projection assumed; skew geometry requires a full 3D coordinate check", "No rotation, rocking, vertical lift, axial escape, contact deformation, bolt/weld failure, plate yielding or fracture calculation", "Distance margin is not a strength margin or factor of safety"]
    }

if __name__=="__main__":
    print(json.dumps(conditional_geometry(),indent=2))
