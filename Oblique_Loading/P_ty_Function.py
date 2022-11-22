f_ty=float(480000000) #[Pa]
diameter_1=float(2) #[cm]
thickness_1=float(1) #[cm]
width_1=float(4) #[cm]
design_load=float(1000) #[N]


a_1=a_4=width_1/2-(0.7071*diameter_1/2)
a_2=a_3=width_1/2-diameter_1/2
a_av=6/(3/a_1+1/a_2+1/a_3+1/a_4)

a_br=diameter_1*thickness_1
ratio=a_av/a_br
print(ratio)
print(a_br)
print(a_av)

k_ty=1.18

p_ty=k_ty*a_br*f_ty*0.0001
ms=(p_ty/design_load)-1
r_tr=design_load/p_ty

print(ms)
print(p_ty)
print(r_tr)
