#ALL UNITS SI
#YIELD is taken as failure mode but method is made for ultimate ASSUMPTION
def yield_load(diameter_1,thickness_1,width_1,stress_yield,stress_ultimate,k_t):
    tension_area=(width_1-diameter_1)*thickness_1
    P_u=tension_area*k_t*stress_yield

    return P_u