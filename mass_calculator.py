import numpy as np
from materials_list import materials_list

def calculate_mass(t_1, t_2, D_1, D_2, D_fo, H_bolt, w, h, l_hole, material_backplate, material_bolts, num_bolts, fastener_positions):
    flange_mass = calculate_flange_mass()
    backplate_mass = calculate_backplate_mass(
        material_backplate=material_backplate,
        w=w,
        fastener_positions=fastener_positions,
        t_2=t_2,
        D_2=D_2,
        num_bolts=num_bolts
    )
    bolts_mass = calculate_bolts_mass(
        material_bolts=material_bolts,
        num_bolts=num_bolts,
        D_2=D_2,
        D_fo=D_fo,
        H_bolt=H_bolt,
        t_1=t_1,
        t_2=t_2)
    return flange_mass + backplate_mass + bolts_mass

def calculate_flange_mass():
    return 0

def calculate_backplate_mass(material_backplate,w,fastener_positions,t_2,D_2,num_bolts):
    plate_length = fastener_positions[-1,0]+(2*D_2)
    mass_holes = num_bolts * np.pi * ((D_2 / 2) ** 2) * t_2 * materials_list[material_backplate]['density']
    mass_backplate = plate_length*w*t_2*materials_list[material_backplate]['density'] - mass_holes
    return mass_backplate

def calculate_bolts_mass(material_bolts,num_bolts,D_2,D_fo,H_bolt,t_1,t_2,):
    mass_bolt_head = (np.pi*((D_fo/2)**2)*H_bolt)*materials_list[material_bolts]['density']
    mass_bolt_shaft = np.pi*((D_2/2)**2)*(t_1+t_2+H_bolt)*materials_list[material_bolts]['density']
    print(mass_bolt_head, mass_bolt_shaft)
    return (mass_bolt_head + mass_bolt_shaft)*num_bolts
