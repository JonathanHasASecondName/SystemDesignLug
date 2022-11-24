import pandas as pd
from graph_reader import graph_reader
import numpy as np
#Input values
stress_yield = 1000*10**6
stress_ultimate = 1000*10**6
density = 2800
F_z = 1000
F_y = 0.1 * F_z

#Getting the data
def P_bry_calculation(thickness_1, diameter_1, width_1, stress_ultimate):
    A_av, A_br = AavAbrCalculation(diameter_1, thickness_1, width_1)
    t_over_D = thickness_1 / diameter_1
    e_over_D = 0.5 * width_1 / diameter_1
    K_bry = graph_reader.get_datapoint(
        load_case='shear',
        t_over_D=str(t_over_D),
        e_over_D=float(e_over_D))
    if K_bry is not None:
        P_bry = K_bry * A_br * stress_ultimate
    else:
        P_bry = K_bry
    return P_bry

def AavAbrCalculation(diameter_1,thickness_1,width_1):
    A_1 = (width_1 / 2 - (0.7071 * diameter_1 / 2)) * thickness_1
    A_4 = A_1
    A_2 = A_3 = (width_1 / 2 - diameter_1 / 2) * thickness_1
    A_av = 6 / (3 / A_1 + 1 / A_2 + 1 / A_3 + 1 / A_4)
    A_br = diameter_1 * thickness_1
    return A_av, A_br
def P_ty_calculation(diameter_1, thickness_1, width_1, stress_yield):
    A_av, A_br = AavAbrCalculation(diameter_1, thickness_1, width_1)
    Aav_over_Abr = A_av/A_br
    K_ty = graph_reader.get_datapoint(
        load_case='tension',
        line_number='3',
        Aav_over_Abr=Aav_over_Abr)
    if K_ty is not None:
        P_ty = K_ty * A_br * stress_yield
    else:
        P_ty = K_ty
    return P_ty

def P_y_calculation(diameter_1,thickness_1,width_1,stress_yield,stress_ultimate):
    K_t = graph_reader.get_datapoint(
        load_case='axial',
        line_number_2='1',
        w_over_D=width_1/diameter_1)
    tension_area = (width_1 - diameter_1) * thickness_1
    if K_t is not None:
        P_y = tension_area * K_t * stress_yield
    else:
        P_y = K_t
    return P_y





def interaction_eq(diameter_1, thickness_1, width_1, stress_yield, stress_ultimate, F_y, F_z):
    A_av, A_br = AavAbrCalculation(diameter_1, thickness_1, width_1)
    P_y = P_y_calculation(diameter_1,thickness_1,width_1,stress_yield,stress_ultimate)
    P_ty = P_ty_calculation(diameter_1, thickness_1, width_1, stress_yield)
    P_bry  = P_bry_calculation(thickness_1, diameter_1, width_1, stress_ultimate)
    R_a = F_y / min(P_y, P_bry)
    R_tr = F_z / P_ty
    Interac = R_a ** 1.6 + R_tr ** 1.6
    return Interac



#mass function
def calculate_mass(diameter_1,thickness_1,width_1,density):
    radius = diameter_1/2
    big_radius = width_1/2
    volume = (((3.14*big_radius**2)/2)+(width_1*(width_1/2))-(3.14*(radius**2)))*thickness_1
    mass = volume * density
    return mass


accepted_dimensions = []
for diameter_1 in np.arange(0.001, 0.02, 0.001):
    for thickness_1 in np.arange(0.001, 0.02, 0.001):
        for width_1 in np.arange(0.001, 0.02, 0.001):
            if (P_y_calculation(diameter_1,thickness_1,width_1,stress_yield,stress_ultimate) is not None) and (P_ty_calculation(diameter_1, thickness_1, width_1, stress_yield) is not None) and (P_bry_calculation(thickness_1, diameter_1, width_1, stress_ultimate) is not None):
                interac = interaction_eq(diameter_1, thickness_1, width_1, stress_yield, stress_ultimate, F_y, F_z)
                if interac >=1:
                    print(P_y_calculation(diameter_1,thickness_1,width_1,stress_yield,stress_ultimate), P_ty_calculation(diameter_1, thickness_1, width_1, stress_yield), P_bry_calculation(thickness_1, diameter_1, width_1, stress_ultimate))
                    mass_1 = calculate_mass(diameter_1,thickness_1,width_1,density)
                    accepted_dimensions.append([diameter_1, thickness_1, width_1, mass_1, interac])
accepted_dimensions = np.array(accepted_dimensions)
print(accepted_dimensions)









