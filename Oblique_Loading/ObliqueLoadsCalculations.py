import pandas as pd
from graph_reader import graph_reader
import numpy as np
#Input values
stress_yield = 550*10**6
stress_ultimate = 620*10**6
shear_stress_yield = stress_yield/2
density = 7850
F_x = 4.5
F_z = 570
F_y = 0.1 * F_z
F_y_2 = 0.059
M_x = 2.79
M_z = 2.79
#Getting the data

def Moment_x_calculation(thickness_1, diameter_1, width_1, M_x):
    tensile_stress_calc = (M_x/(diameter_1))/((width_1-diameter_1)*thickness_1)
    return tensile_stress_calc

def Force_x_calculation(thickness_1, diameter_1, width_1, F_x):
    V_x = F_x/4
    Q = (thickness_1**2)*(width_1-diameter_1)/16
    I_zz = (((width_1-diameter_1)/2)*thickness_1**3)/12
    shear_stress_calc = V_x*Q/(I_zz*thickness_1)
    return shear_stress_calc

def Moment_z_calculation(thickness_1, diameter_1, width_1, M_z, F_y_2):
    flange_distance = width_1
    Force = (M_z/flange_distance)/2 + F_y_2/4
    Area = thickness_1 * ((width_1-diameter_1)/2)
    tensile_stress_calc = Force/Area
    return tensile_stress_calc

def P_bry_calculation(thickness_1, diameter_1, width_1, stress_yield):
    A_av, A_br = AavAbrCalculation(diameter_1, thickness_1, width_1)
    t_over_D = thickness_1 / diameter_1
    if 0<=t_over_D<0.065:
        t_over_D = 0.06
    elif 0.065<=t_over_D<0.09:
        t_over_D = 0.08
    elif 0.09<=t_over_D<0.11:
        t_over_D = 0.10
    elif 0.11<=t_over_D<0.135:
        t_over_D = 0.12
    elif 0.135<=t_over_D<0.175:
        t_over_D = 0.15
    elif 0.175<=t_over_D<0.25:
        t_over_D = 0.2
    elif 0.25<=t_over_D<0.35:
        t_over_D = 0.3
    elif 0.35<=t_over_D<0.5:
        t_over_D = 0.4
    elif 0.5<t_over_D:
        t_over_D = 0.6
    e_over_D = 0.5 * width_1 / diameter_1
    K_bry = graph_reader.get_datapoint(
        load_case='shear',
        t_over_D=str(t_over_D),
        e_over_D=float(e_over_D))
    if K_bry is not None:
        P_bry = K_bry * A_br * stress_yield
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

def P_y_calculation(diameter_1,thickness_1,width_1,stress_yield):
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

def interaction_eq(diameter_1, thickness_1, width_1, stress_yield, F_y, F_z):
    A_av, A_br = AavAbrCalculation(diameter_1, thickness_1, width_1)
    P_y = P_y_calculation(diameter_1,thickness_1,width_1,stress_yield)
    P_ty = P_ty_calculation(diameter_1, thickness_1, width_1, stress_yield)
    P_bry  = P_bry_calculation(thickness_1, diameter_1, width_1, stress_yield)
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

def best_dimensions(accepted_dimensions):
    accepted_dimensions = np.array(accepted_dimensions)
    count_1 = -1
    mass_min = np.inf
    for accepted_dimension in accepted_dimensions:
        count_1 += 1
        if accepted_dimension[3] < mass_min:
            mass_min = accepted_dimension[3]
            mass_min_index = count_1
    return accepted_dimensions[mass_min_index]

accepted_dimensions = []
all_dimensions = []
for diameter_1 in np.arange(0.001, 0.02, 0.0001):
    for thickness_1 in np.arange(0.001, 0.02, 0.0001):
        for width_1 in np.arange(0.001, 0.02, 0.0001):
            if width_1 > diameter_1:
#diameter_1 = 0.0018
#thickness_1 = 0.0047
#width_1 = 0.0024
                if (P_y_calculation(diameter_1,thickness_1,width_1,stress_yield) is not None) and (P_ty_calculation(diameter_1, thickness_1, width_1, stress_yield) is not None) and (P_bry_calculation(thickness_1, diameter_1, width_1, stress_yield) is not None):
                    interac = interaction_eq(diameter_1, thickness_1, width_1, stress_yield, F_y, F_z)
                    mass_1 = 2* calculate_mass(diameter_1,thickness_1,width_1,density)
                    all_dimensions.append([diameter_1, thickness_1, width_1, mass_1, interac])
                    if interac <= 1 and Moment_x_calculation(thickness_1, diameter_1, width_1, M_x)<=stress_yield and Force_x_calculation(thickness_1, diameter_1, width_1, F_x)<=shear_stress_yield and Moment_z_calculation(thickness_1, diameter_1, width_1, M_z, F_y_2)<= stress_yield:
                        mass_1 = calculate_mass(diameter_1,thickness_1,width_1,density)
                        accepted_dimensions.append([diameter_1, thickness_1, width_1, mass_1, interac, Moment_x_calculation(thickness_1, diameter_1, width_1, M_x), Force_x_calculation(thickness_1, diameter_1, width_1, F_x),Moment_z_calculation(thickness_1, diameter_1, width_1, M_z, F_y_2)])

print(best_dimensions(accepted_dimensions))











