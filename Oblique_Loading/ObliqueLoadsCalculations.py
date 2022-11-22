import pandas as pd

#Input values
diameter_1 = 0.001
thickness_1 = 0.001
width_1 = 0.002
stress_yield = 1000
stress_ultimate = 1000

#Calculated parameters
A_1=A_4=width_1/2-(0.7071*diameter_1/2)
A_2=A_3=width_1/2-diameter_1/2
A_av=6/(3/A_1+1/A_2+1/A_3+1/A_4)
A_br=diameter_1*thickness_1

#Getting the data
def P_bry_calculation(thickness_1, diameter_1, width_1, stress_ultimate):
    t_over_D = thickness_1 / diameter_1
    e_over_D = 0.5 * width_1 / diameter_1
    t_over_Ds = [0.06,0.08,0.10,0.12,0.15,0.2,0.3,0.4,0.6]
    curve = min(t_over_Ds, key=lambda x:abs(x-t_over_D))
    curve_data = pd.read_excel('shear_bearing_factors.xlsx', sheet_name = str(curve))
    e_over_Ds = curve_data["e_over_D"].tolist()
    K_bry = curve_data.at[curve_data[curve_data['e_over_D']==min(e_over_Ds, key=lambda x:abs(x-e_over_D))].index.values[0], 'Kbry']
    P_bry = K_bry * A_br * stress_ultimate
    return P_bry

def P_ty(A_av, A_br, stress_yield):
    curve_data = pd.read_excel('tension_efficiency_factors.xlsx', sheet_name = str(3))
    Aav_over_Abr = A_av/A_br
    Aav_over_Abrs = curve_data["Aav_over_Abr"].tolist()
    K_ty = curve_data.at[curve_data[curve_data['Aav_over_Abr']==min(Aav_over_Abrs, key=lambda x:abs(x-Aav_over_Abr))].index.values[0], 'Kty']
    P_ty = K_ty * A_br * stress_yield
    return P_ty

print(P_bry_calculation(thickness_1, diameter_1, width_1, stress_ultimate))


