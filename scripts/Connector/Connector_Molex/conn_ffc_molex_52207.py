#!/usr/bin/env python3

import sys
import os
#sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path

# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree
from math import sqrt
import argparse
import yaml
from helpers import *
from KicadModTree import *

sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields
from footprint_keepout_area import addRectangularKeepout

pinrange = range(3, 31) # 3-30 circuits

series = ""
series_long = ('Molex 1.00mm Pitch Easy-On, ' +
               'Right-Angle, ZIF, Top Contact FFC/FPC')
manufacturer = 'Molex'
orientation = 'H'
number_of_rows = 1

conn_category = "FFC-FPC"

lib_by_conn_category = True

part_code = "52207-{:02d}60"

pitch = 1.0
pad_size = (0.6, 1.9)
mp_size = (2.1, 2.8)
pad_y = -1.6 - 0.6 - pad_size[1] / 2
mp_y = pad_y + pad_size[1] / 2 + mp_size[1] / 2
mount_pin_width = 0.8
mount_pin_height = 2
pin_length = 2
actuator_ext_w = 3.5
body_height = 4.3
actuator_closed_height = 5.6
actuator_open_height = 6.9
back_y = pad_y - pad_size[1] / 2 + 0.3 + pin_length


def make_module(pin_count, configuration):
    mpn = part_code.format(pin_count)
    datasheet='https://www.molex.com/pdm_docs/sd/52207{:02d}60_sd.pdf'.format(pin_count)

    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(
        man = manufacturer,
        series = series,
        mpn = mpn,
        num_rows = number_of_rows,
        pins = pin_count,
	pins_per_row = pin_count,
        mounting_pad = "-1MP",
        pitch = pitch,
        orientation = orientation_str)

    footprint_name = footprint_name.replace("__",'_')

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setAttribute('smd')
    kicad_mod.setDescription(
        ("Molex {:s}, {:s}, {:d} Circuits ({:s}), " +
         "generated with kicad-footprint-generator").format(
        series_long, mpn, pin_count, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(
        man=manufacturer,
        series=series,
        orientation=orientation_str,
        entry=configuration['entry_direction'][orientation]))

    # calculate per package values
    pin_span = pin_count - 1
    body_width = pin_span + 5.7
    actuator_width = pin_span + 2 * actuator_ext_w


    
    pad_silk_off = (configuration['silk_pad_clearance'] +
                    (configuration['silk_line_width'] / 2))
    fab_silk_off = configuration['silk_fab_offset']

    ## Mounting Pads ##

    mp_pos = ((pin_span / 2) + 2.1 + (mp_size[0] / 2), mp_y)

    def make_anchor_pad(x_direction):
        kicad_mod.append(
            Pad(number = configuration['mounting_pad_number'],
                type = Pad.TYPE_SMT,
                shape = Pad.SHAPE_RECT,
                at = [x_direction * mp_pos[0], mp_pos[1]],
                size = mp_size,
                layers = Pad.LAYERS_SMT))
    make_anchor_pad(-1)
    make_anchor_pad(1)

    ## Pads ##

    kicad_mod.append(
        PadArray(center = [0, pad_y],
            pincount = pin_count,
            x_spacing = pitch,
            type = Pad.TYPE_SMT,
            shape = Pad.SHAPE_RECT,
            size = pad_size,
            layers = Pad.LAYERS_SMT))

    ## Fab ##

    fab_body_outline = [
        {'x': -(body_width / 2) - mount_pin_width, 'y': back_y},
        {'x': -(body_width / 2) - mount_pin_width, 'y': back_y + mount_pin_height},
        {'x': -(body_width / 2), 'y': back_y + mount_pin_height},
        {'x': -(body_width / 2), 'y': back_y + body_height},
        {'x': -(actuator_width / 2), 'y': back_y + body_height},
        {'x': -(actuator_width / 2), 'y': back_y + actuator_closed_height},
        {'x': (actuator_width / 2), 'y': back_y + actuator_closed_height},
        {'x': (actuator_width / 2), 'y': back_y + body_height},
        {'x': (body_width / 2), 'y': back_y + body_height},
        {'x': (body_width / 2), 'y': back_y + mount_pin_height},
        {'x': (body_width / 2) + mount_pin_width, 'y': back_y + mount_pin_height},
        {'x': (body_width / 2) + mount_pin_width, 'y': back_y},
        {'x': -(body_width / 2) - mount_pin_width, 'y': back_y}
    ]
    
    kicad_mod.append(PolygoneLine(
        polygone = fab_body_outline,
        layer = 'F.Fab',
        width = configuration['fab_line_width']))
    
    fab_pin1_mark = [
        {'x': -(pin_span / 2) - 0.5, 'y': back_y},
        {'x': -(pin_span / 2), 'y': back_y + 0.75},
        {'x': -(pin_span / 2) + 0.5, 'y': back_y}
    ]
    
    kicad_mod.append(PolygoneLine(
        polygone = fab_pin1_mark,
        layer = 'F.Fab',
        width = configuration['fab_line_width']))
    
    fab_open_actuator_outline = [
        {'x': -(body_width / 2), 'y': back_y + actuator_closed_height},
        {'x': -(body_width / 2), 'y': back_y + (actuator_closed_height + actuator_open_height) / 2},
        {'x': -(actuator_width / 2), 'y': back_y + (actuator_closed_height + actuator_open_height) / 2},
        {'x': -(actuator_width / 2), 'y': back_y + actuator_open_height},
        {'x': (actuator_width / 2), 'y': back_y + actuator_open_height},
        {'x': (actuator_width / 2), 'y': back_y + (actuator_closed_height + actuator_open_height) / 2},
        {'x': (body_width / 2), 'y': back_y + (actuator_closed_height + actuator_open_height) / 2},
        {'x': (body_width / 2), 'y': back_y + actuator_closed_height}
    ]
        
    kicad_mod.append(PolygoneLine(
        polygone = fab_open_actuator_outline,
        layer = 'F.Fab',
        width = configuration['fab_line_width']))
    
    ### SilkS ##
    
    silk_outline1 = [
        {'x': (-(pin_span / 2) - (pad_size[0] / 2)) - pad_silk_off, 'y': pad_y - (pad_size[1] / 2)},
        {'x': (-(pin_span / 2) - (pad_size[0] / 2)) - pad_silk_off, 'y': back_y - fab_silk_off},
        {'x': -mp_pos[0] + mp_size[0] / 2 + pad_silk_off, 'y': back_y - fab_silk_off}
    ]
    
    silk_outline2 = [
        {'x': -(body_width / 2) - fab_silk_off, 'y': mp_pos[1] + mp_size[1] / 2 + pad_silk_off},
        {'x': -(body_width / 2) - fab_silk_off, 'y': back_y + body_height - fab_silk_off},
        {'x': -(actuator_width / 2) - fab_silk_off, 'y': back_y + body_height - fab_silk_off},
        {'x': -(actuator_width / 2) - fab_silk_off, 'y': back_y + actuator_closed_height + fab_silk_off},
        {'x': (actuator_width / 2) + fab_silk_off, 'y': back_y + actuator_closed_height + fab_silk_off},
        {'x': (actuator_width / 2) + fab_silk_off, 'y': back_y + body_height - fab_silk_off},
        {'x': (body_width / 2) + fab_silk_off, 'y': back_y + body_height - fab_silk_off},
        {'x': (body_width / 2) + fab_silk_off, 'y': mp_pos[1] + mp_size[1] / 2 + pad_silk_off}
    ]
    
    silk_outline3 = [
        {'x': (pin_span / 2) + (pad_size[0] / 2) + pad_silk_off, 'y': back_y - fab_silk_off},
        {'x': mp_pos[0] - mp_size[0] / 2 - pad_silk_off, 'y': back_y - fab_silk_off}
    ]

    kicad_mod.append(PolygoneLine(
        polygone = silk_outline1,
        layer = 'F.SilkS',
        width = configuration['silk_line_width']))
    
    kicad_mod.append(PolygoneLine(
        polygone = silk_outline2,
        layer = 'F.SilkS',
        width = configuration['silk_line_width']))
    
    kicad_mod.append(PolygoneLine(
        polygone = silk_outline3,
        layer = 'F.SilkS',
        width = configuration['silk_line_width']))
    
    ### CrtYd ##
    
    bounding_box = {
        'top': pad_y - (pad_size[1] / 2),
        'left': (-mp_pos[0] - (mp_size[0] / 2)),
        'bottom': back_y + actuator_open_height,
        'right': (mp_pos[0] + (mp_size[0] / 2))}
    
    cx1 = roundToBase(bounding_box['left']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(bounding_box['top']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    
    cx2 = roundToBase(bounding_box['right']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(bounding_box['bottom']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    
    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))
    
    ### Text ##
    
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=bounding_box, courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position='center')
    
    
    
    
    ###################### Output and 3d model ############################
    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')
    
    if lib_by_conn_category:
        lib_name = configuration['lib_name_specific_function_format_string'].format(category=conn_category)
    else:
        lib_name = configuration['lib_name_format_string'].format(series=series, man=manufacturer)
    
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=footprint_name)
    kicad_mod.append(Model(filename=model_name))
    
    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)
    
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../conn_config_KLCv3.yaml')
    args = parser.parse_args()

    with open(args.global_config, 'r') as config_stream:
        try:
            configuration = yaml.safe_load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(args.series_config, 'r') as config_stream:
        try:
            configuration.update(yaml.safe_load(config_stream))
        except yaml.YAMLError as exc:
            print(exc)

    for pincount in pinrange:
        make_module(pincount, configuration)
