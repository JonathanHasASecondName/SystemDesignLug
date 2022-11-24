def ratio_d_15():
    a_1=a_4=float(width_1/2-(0.7071*diameter_1/2))
    a_2=a_3=float(width_1/2-diameter_1/2)
    a_av=float(6/(3/a_1+1/a_2+1/a_3+1/a_4))
    ratio=float(a_av/a_br)

    return ratio

def r_transverse():
    k_ty=graph_reader.get_datapoint(
    load_case='tension',
    line_number='3',
    Aav_over_Abr=ratio_d_15()
)
    p_ty=float(k_ty*a_br*f_ty)
    ms=float((p_ty/design_load)-1)
    r_tr=float(design_load/p_ty)
    print(r_tr)
    return ms,r_tr

print(r_transverse())



