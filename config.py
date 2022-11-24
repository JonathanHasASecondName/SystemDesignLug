
from os import path
"""
Contains relevant file paths for the program
"""

ROOT_DIR = path.realpath(path.join(path.dirname(__file__)))
shear_factors_path = ROOT_DIR + "/shear_bearing_factors.xlsx"
tension_factors_path = ROOT_DIR + "/tension_efficiency_factors.xlsx"
axial_factors_path = ROOT_DIR + "/tension_efficiency_axially_loaded.xlsx"

# Forces applied to the entire assembly
external_forces = [1, 1, 1]  # Newton, x, y and z
external_moments = [0, 0, 0]  # Newton meter, x, y and z
w = 0.2 # width
D_1 = 0.01 # diameter of hinge hole
t_1 = 0.01 # thickness lug flange
l_hole = 0.5*w