f_ty=float(480000000) #[Pa]
diameter_1=float(0.02) #[m]
thickness_1=float(0.01) #[m]
width_1=float(0.04) #[m]
design_load=float(1000) #[N]

def ratio_d_15(f_ty,diameter_1,thickness_1,width_1,design_load):
    a_1=a_4=float(width_1/2-(0.7071*diameter_1/2))
    a_2=a_3=float(width_1/2-diameter_1/2)
    a_av=float(6/(3/a_1+1/a_2+1/a_3+1/a_4))
    a_br=float(diameter_1*thickness_1)
    ratio=float(a_av/a_br)

    return ratio

def r_transverse(a_br,f_ty,design_load):
    k_ty=graph_reader(ratio)
    p_ty=float(k_ty*a_br*f_ty)
    ms=float((p_ty/design_load)-1)
    r_tr=float(design_load/p_ty)

    return ms,r_tr





