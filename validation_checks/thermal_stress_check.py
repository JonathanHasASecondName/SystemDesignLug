import numpy as np
import math

from configuration import Configuration

def run_check(configuration: Configuration) -> bool:

    return True

def calculate_force_ratio(compliance_a, compliance_b):
    return compliance_a/(compliance_a+compliance_b)

def calculate_compliance_a(t, youngs_mod, D_fo, D_fi):
    return 4*t/(youngs_mod*np.pi*(D_fo*D_fo-D_fi*D_fi))  # not using D_fo**2 as D_fo*D_fo is faster

def calculate_compliance_b(youngs_mod,  D_fi, d_sha):
    L_hsub = 0.4 * D_fi
    L_engsub = 0.33 * D_fi
    L_nsub =  0.4 * D_fi
    A_sha = (math.pi * (d_sha) ** 2 )/4
    A_nom = (math.pi * (D_fi) ** 2)/4

    return (1/youngs_mod)*((L_hsub/A_nom)+(L_engsub/A_sha)+(L_sha/A_sha)+(L_nsub/A_nom))

def calculate_in_plane_loads(alpha_c, alpha_b, delta_T, youngs_mod, area_sm, force_ratio):
    return (alpha_c-alpha_b)*delta_T*youngs_mod*area_sm*(1-force_ratio)
