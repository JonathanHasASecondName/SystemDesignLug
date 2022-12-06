import numpy as np
from os import path
"""
Contains relevant file paths for the program
"""

ROOT_DIR = path.realpath(path.join(path.dirname(__file__)))
shear_factors_path = ROOT_DIR + "/shear_bearing_factors.xlsx"
tension_factors_path = ROOT_DIR + "/tension_efficiency_factors.xlsx"
axial_factors_path = ROOT_DIR + "/tension_efficiency_axially_loaded.xlsx"

# Forces applied to the entire assembly
external_forces = np.array([0, 57, 570])  # Newton, x, y and z
#external_forces = np.array([0, 1000, 1000])  # Newton, x, y and z
external_moments = np.array([2.79, 0, 2.79])  # Newton meter, x, y and z
w = max(0.0051,0.01) # width
h = 0.0046 # flange spacing
D_1 = 0.0026 # diameter of hinge hole
t_1 = 0.001 # thickness lug flange
l_hole = 0.5*D_1 + 0.002
spacecraft_material = '2024-T4 aluminium'
lug_material = '4130 steel'
force_safety_factor = 1
thermal_loads_safety_factor = 2