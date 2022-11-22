import pandas as pd

#Input values
diameter_1 = 0.001
thickness_1 = 0.001
width_1 = 0.002
stress_yield = 1000
stress_ultimate = 1000

#Calculated parameters
A_br =
t_over_D = thickness_1/diameter_1
e_over_D  = 0.5*width_1/diameter_1

#Getting the data
t_over_Ds = [0.06,0.08,0.10,0.12,0.15,0.2,0.3,0.4,0.6]
curve = min(t_over_Ds, key=lambda x:abs(x-t_over_D))
curve_data = pd.read_excel('shear_bearing_factors.xlsx', sheet_name = str(curve))
e_over_Ds = curve_data["e_over_D"].tolist()
K_bry = curve_data.at[curve_data[curve_data['e_over_D']==min(e_over_Ds, key=lambda x:abs(x-e_over_D))].index.values[0], 'Kbry'])

#Final equation
P_bry = K_bry*stress_ultimate*A_br
