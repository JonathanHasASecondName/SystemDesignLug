#ALL UNITS SI
#YIELD is taken as failure mode but method is made for ultimate ASSUMPTION

from graph_reader import graph_reader

def yield_load(diameter_1,thickness_1,width_1,stress_yield,stress_ultimate):
    k_t=graph_reader.get_datapoint(
        load_case='tension',
        line_number='9',
        Aav_over_Abr=1)

    tension_area=(width_1-diameter_1)*thickness_1
    P_y=tension_area*k_t*stress_yield


    return P_y

print(yield_load(0.05,0.005,0.08,550*10**6,620*10**6))