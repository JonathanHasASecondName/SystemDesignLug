import pandas as pd
from graph_reader import graph_reader
#Input values
diameter_1 = 0.001
thickness_1 = 0.001
width_1 = 0.002
stress_yield = 1000
stress_ultimate = 1000
density = 2800

#Calculated parameters
A_1=A_4=width_1/2-(0.7071*diameter_1/2)
A_2=A_3=width_1/2-diameter_1/2
A_av=6/(3/A_1+1/A_2+1/A_3+1/A_4)
A_br=diameter_1*thickness_1

#Getting the data
def P_bry_calculation(thickness_1, diameter_1, width_1, stress_ultimate):
    t_over_D = thickness_1 / diameter_1
    e_over_D = 0.5 * width_1 / diameter_1
    K_bry =
    P_bry = K_bry * A_br * stress_ultimate
    return P_bry

def P_ty_calculation(A_av, A_br, stress_yield):
    Aav_over_Abr = A_av/A_br
    K_ty =
    P_ty = K_ty * A_br * stress_yield
    return P_ty

def P_y(diameter_1,thickness_1,width_1,stress_yield,stress_ultimate):
    K_t = graph_reader.get_datapoint(
        load_case='tension',
        line_number='9',
        Aav_over_Abr=1)
    tension_area = (width_1 - diameter_1) * thickness_1
    P_y = tension_area * K_t * stress_yield
    return P_y

def interaction_eq():
    P_y = P_y(diameter_1,thickness_1,width_1,stress_yield,stress_ultimate)
    P_ty = P_ty_calculation(A_av, A_br, stress_yield)
    P_bry  = P_bry_calculation(thickness_1, diameter_1, width_1, stress_ultimate)

#mass function
def calculate_mass(diameter_1,thickness_1,width_1,density):
    radius = diameter_1/2
    big_radius = width_1/2
    volume = (((3.14*big_radius**2)/2)+(width_1*(width_1/2))-(3.14*(radius**2)))*thickness_1
    mass = volume * density
    return mass



