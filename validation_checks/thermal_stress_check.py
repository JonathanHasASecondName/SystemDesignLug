import numpy as np

from configuration import Configuration

def run_check(configuration: Configuration) -> bool:

    return True

def calculate_force_ratio(compliance_a, compliance_b):
    return compliance_a/(compliance_a+compliance_b)

def calculate_compliance_a(t, youngs_mod, D_fo, D_fi):
    return 4*t/(youngs_mod*np.pi*(D_fo*D_fo-D_fi*D_fi))  # not using D_fo**2 as D_fo*D_fo is faster

def calculate_compliance_b():
    pass

def calculate_in_plane_loads(delta_exp_coeff, delta_T, youngs_mod, area_sm, compliance_ratio):
    return delta_exp_coeff*delta_T*youngs_mod*area_sm*compliance_ratio
