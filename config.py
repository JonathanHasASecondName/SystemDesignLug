
from os import path
"""
Contains relevant file paths for the program
"""

ROOT_DIR = path.realpath(path.join(path.dirname(__file__)))
shear_factors_path = ROOT_DIR + "/shear_bearing_factors.xlsx"
tension_factors_path = ROOT_DIR + "/tension_efficiency_factors.xlsx"

# Forces applied to the entire assembly
external_forces = [1, 1, 1]  # Newton, x, y and z
external_moments = [0, 0, 0]  # Newton meter, x, y and z
