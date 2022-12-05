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
w = 0.02 # width
h = 0.1 # flange spacing
D_1 = 0.01 # diameter of hinge hole
t_1 = 0.005 # thickness lug flange
l_hole = 0.5*w
spacecraft_material = '7075-T6 aluminium'
lug_material = '356-T6 aluminium'
