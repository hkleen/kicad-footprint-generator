from collections import namedtuple
from collections import OrderedDict

class seriesParams():
    drill = 1.7
    annular_ring = 0.4 # overwritten by minimum pad to pad clearance.

    mount_drill = 2.5
    mount_screw_head_r = 2.5
    flange_lenght = 7.36
    scoreline_from_back = 6.0

    plug_cut_len = 3.0
    plug_cut_width = 4.3
    plug_arc_len = 1.5
    plug_trapezoid_short = 2.5
    plug_trapezoid_long = 3.0
    plug_trapezoid_width = 1
    plug_seperator_distance = 1.5

    silk_pad_clearance = 0.15
    mount_screw_info = "ISO 1481-ST 2.2x4.5 C or ISO 7049-ST 2.2x4.5 C (http://www.fasteners.eu/standards/ISO/7049/)"

    # Connector voltage ratings:
    # Rated voltage (III/3) 1000 V
    # Rated voltage (III/2) 1000 V
    # Rated voltage (II/2) 1000 V
    # Rated surge voltage (III/3) 8 kV
    # Rated surge voltage (III/2) 8 kV
    # Rated surge voltage (II/2) 6 kV
    # VDE 0110-1/4.97 8kV -> 8mm clearance
    min_pad_to_pad_clearance = 8.0

Params = namedtuple("Params",[
    'series_name',
    'angled',
    'flanged',
    'num_pins',
    'pin_pitch',
    'mount_hole',
    'order_info',
    'mount_hole_to_pin',
    'side_to_pin',
    'back_to_pin',
    'pin_Sx',
    'pin_Sy'
])

def generate_params(num_pins, series_name, pin_pitch, angled, flanged, order_info, mount_hole=False, mount_hole_to_pin=None,
            side_to_pin=None, back_to_pin=None, min_pad_to_pad_clearance=seriesParams.min_pad_to_pad_clearance):
    nominal_pin_Sx = seriesParams.drill + 2 * seriesParams.annular_ring
    nominal_pin_Sy = seriesParams.drill + 2 * 1.2
    return Params(
        series_name=series_name,
        angled=angled,
        flanged=flanged,
        num_pins=num_pins,
        pin_pitch=pin_pitch,
        mount_hole=mount_hole,
        order_info=order_info,
        mount_hole_to_pin=pin_pitch if mount_hole_to_pin is None else mount_hole_to_pin,
        side_to_pin=(3*pin_pitch if flanged else pin_pitch+2)/2.0 if side_to_pin is None else side_to_pin,
        back_to_pin= (8-9.2 if angled else 3-7.25) if back_to_pin is None else back_to_pin,
        pin_Sx=(nominal_pin_Sx if pin_pitch-nominal_pin_Sx >= min_pad_to_pad_clearance else pin_pitch - min_pad_to_pad_clearance),
        pin_Sy = nominal_pin_Sy
    )


all_params = {
    ##################################################################################################################
    # Pin Pitch 10.16 mm
    ##################################################################################################################
    'PC_01x02_G1_10.16mm' : generate_params( 2, "PC-G1", 10.16, True, False, OrderedDict([('1998933', '76A 1000V')]), side_to_pin=6.6, back_to_pin=-14.4),
    'PC_01x03_G1_10.16mm' : generate_params( 3, "PC-G1", 10.16, True, False, OrderedDict([('1998946', '76A 1000V')]), side_to_pin=6.6, back_to_pin=-14.4),
    'PC_01x04_G1_10.16mm' : generate_params( 4, "PC-G1", 10.16, True, False, OrderedDict([('1998959', '76A 1000V')]), side_to_pin=6.6, back_to_pin=-14.4),
    'PC_01x05_G1_10.16mm' : generate_params( 5, "PC-G1", 10.16, True, False, OrderedDict([('1998962', '76A 1000V')]), side_to_pin=6.6, back_to_pin=-14.4),
    'PC_01x06_G1_10.16mm' : generate_params( 6, "PC-G1", 10.16, True, False, OrderedDict([('1998975', '76A 1000V')]), side_to_pin=6.6, back_to_pin=-14.4),
    'PC_01x07_G1_10.16mm' : generate_params( 7, "PC-G1", 10.16, True, False, OrderedDict([('1998988', '76A 1000V')]), side_to_pin=6.6, back_to_pin=-14.4),
    'PC_01x08_G1_10.16mm' : generate_params( 8, "PC-G1", 10.16, True, False, OrderedDict([('1998991', '76A 1000V')]), side_to_pin=6.6, back_to_pin=-14.4),
    'PC_01x09_G1_10.16mm' : generate_params( 9, "PC-G1", 10.16, True, False, OrderedDict([('1996391', '76A 1000V')]), side_to_pin=6.6, back_to_pin=-14.4),
    ##################################################################################################################
    # Pin Pitch 10.16 mm with mounting hole and flange
    ##################################################################################################################
    'PC_01x02_G1F_10.16mm' : generate_params( 2, "PC-G1F", 10.16, True, True, OrderedDict([('1999000', '76A 1000V')]), side_to_pin=13.96, back_to_pin=-14.4, mount_hole=True, mount_hole_to_pin=10.16),
    'PC_01x03_G1F_10.16mm' : generate_params( 3, "PC-G1F", 10.16, True, True, OrderedDict([('1999013', '76A 1000V')]), side_to_pin=13.96, back_to_pin=-14.4, mount_hole=True, mount_hole_to_pin=10.16),
    'PC_01x04_G1F_10.16mm' : generate_params( 4, "PC-G1F", 10.16, True, True, OrderedDict([('1999026', '76A 1000V')]), side_to_pin=13.96, back_to_pin=-14.4, mount_hole=True, mount_hole_to_pin=10.16),
    'PC_01x05_G1F_10.16mm' : generate_params( 5, "PC-G1F", 10.16, True, True, OrderedDict([('1999039', '76A 1000V')]), side_to_pin=13.96, back_to_pin=-14.4, mount_hole=True, mount_hole_to_pin=10.16),
    'PC_01x06_G1F_10.16mm' : generate_params( 6, "PC-G1F", 10.16, True, True, OrderedDict([('1999042', '76A 1000V')]), side_to_pin=13.96, back_to_pin=-14.4, mount_hole=True, mount_hole_to_pin=10.16),
    'PC_01x07_G1F_10.16mm' : generate_params( 7, "PC-G1F", 10.16, True, True, OrderedDict([('1999055', '76A 1000V')]), side_to_pin=13.96, back_to_pin=-14.4, mount_hole=True, mount_hole_to_pin=10.16),
    'PC_01x08_G1F_10.16mm' : generate_params( 8, "PC-G1F", 10.16, True, True, OrderedDict([('1999068', '76A 1000V')]), side_to_pin=13.96, back_to_pin=-14.4, mount_hole=True, mount_hole_to_pin=10.16)

}


#lock_cutout=
CalcDim=namedtuple("CalcDim",[
    "length", "width", "left_to_pin",
    "mount_hole_left", "mount_hole_right", "flange_width",
    "plug_front", "plug_back"
])
def dimensions(params):
    mount_hole_y = 3.6 if params.angled else 0.0
    width = 34 if params.angled else 7.25
    return CalcDim(
        length = (params.num_pins-1)*params.pin_pitch + 2*params.side_to_pin
        ,width = width
        ,left_to_pin = -params.side_to_pin
        ,mount_hole_left = [-params.mount_hole_to_pin,mount_hole_y]
        ,mount_hole_right = [(params.num_pins-1)*params.pin_pitch+params.mount_hole_to_pin,mount_hole_y]
        ,flange_width = 9.2 if params.angled else 6.0
        ,plug_front = width + params.back_to_pin -0.75
        ,plug_back = params.back_to_pin+0.6+0.25
    )

def generate_description(params, mpn):
    d = "Generic Phoenix Contact connector footprint for: " + mpn + "; number of pins: " + ("%02d" %params.num_pins) + "; pin pitch: " + (('%.2f' % params.pin_pitch))\
        +"mm" + ('; Angled' if params.angled else '; Vertical')\
        + ('; threaded flange' + ('; footprint includes mount hole for mounting screw: ' + seriesParams.mount_screw_info if params.mount_hole else '') if params.flanged else '')
    for order_num, info in params.order_info.items():
        d += " || order number: " + order_num + " " + info
    return d
