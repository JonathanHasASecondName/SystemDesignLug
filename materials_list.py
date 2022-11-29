# yieldstress in Pa, density in kg/m3
materials_list = {
    'steel': {'type': 'metal', 'yield_stress': 350000000, 'bearing_stress': 524000000, 'density': 7860, 'thermal_expansion_coeff': 17.2}, # asm.matweb.com/search/SpecificMaterial.asp?bassnum=MQ302AV
    'aluminium': {'type': 'metal', 'yield_stress': 345000000, 'bearing_stress': 524000000, 'density': 2780, 'thermal_expansion_coeff': 23.2}, # https://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MA2024T3
    'titanium': {'type': 'metal', 'yield_stress': 880000000, 'bearing_stress': 1480000000, 'density': 4430, 'thermal_expansion_coeff': 8.6} # https://asm.matweb.com/search/SpecificMaterial.asp?bassnum=mtp641
}
# NB. Thermal expansion is in micrometer/m-C. See https://asm.matweb.com/search/SpecificMaterial.asp?bassnum=mtp641