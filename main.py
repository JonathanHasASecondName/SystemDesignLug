import numpy as np

from configurations_generator import generate_configurations
from validation_checks import bearing_check
from validation_checks import pull_push_through_check
from validation_checks import thermal_stress_check
from materials_list import materials_list
import mass_calculator
import config

configurations = generate_configurations()
force_location = np.array([0, config.w/2, 0])

mass_list = []
for configuration in configurations:
    # print("lug, fastener material: ", configuration.lug_material, configuration.fastener_material)
    # 1. BEARING CHECK
    configuration.t_2 = bearing_check.calculate_t2(
        configuration.fastener_positions,
        configuration.D_fi,
        materials_list[configuration.lug_material]["bearing_stress"],
        config.external_forces,
        config.external_moments)
    configuration.t_3 = bearing_check.calculate_t2(
        configuration.fastener_positions,
        configuration.D_fi,
        materials_list[config.spacecraft_material]["bearing_stress"],
        config.external_forces,
        config.external_moments)

    # print("BC: ", configuration.t_2, configuration.t_3)

    # 2. PULL/PUSH THROUGH CHECK:
    pull_push_through_check_t2 = pull_push_through_check.calculate_t2(
        coordinate_array=configuration.fastener_positions,
        D_o=configuration.D_fi,
        tau_yield=materials_list[configuration.lug_material]['shear_stress'],
        forces=config.external_forces,
        force_location=force_location,
        moment=config.external_moments)
    if pull_push_through_check_t2 > configuration.t_2:
        configuration.t_2 = pull_push_through_check_t2
    pull_push_through_check_t3 = pull_push_through_check.calculate_t2(
        configuration.fastener_positions,
        configuration.D_fi,
        materials_list[config.spacecraft_material]['shear_stress'],
        config.external_forces,
        force_location,
        config.external_moments)
    if pull_push_through_check_t3 > configuration.t_3:
        configuration.t_3 = pull_push_through_check_t3
    # print("PPTC: ", pull_push_through_check_t2, pull_push_through_check_t3)
    # print("FINAL: ", configuration.t_2, configuration.t_3, '\n')

    # 3. COMPLIANCE CHECK:

    Thermal_loads_back_plate = thermal_stress_check.calculate_in_plane_loads(
        materials_list[config.lug_material]['thermal_expansion_coeff'],
        materials_list[configuration.fastener_material]['thermal_expansion_coeff'],
        115,
        materials_list[configuration.fastener_material]['Youngs_modulus'],
        1,
        materials_list[config.lug_material]['Youngs_modulus']
        configuration.D_fi,
        configuration.D_fo,
        0.00479806,
        configuration.t_2)

    Thermal_loads_vehicle_wall = thermal_stress_check.calculate_in_plane_loads(
        materials_list[config.spacecraft_material]['thermal_expansion_coeff']
        materials_list[config.fastener_material]['thermal_expansion_coeff']
        115.
        materials_list[configuration.fastener_material]['Youngs_modulus'],
        1,
        materials_list[config.spacecraft_material]['Youngs_modulus'],
        configuration.D_fi,
        configuration.D_fo,
        0.00479806,
        configuration.t_3)





    # 4. THERMAL STRESS CHECK:

    # 5. MASS CALCULATION:
    configuration.mass = mass_calculator.calculate_mass(
        t_1=config.t_1,
        t_2=configuration.t_2,
        D_1=config.D_1,
        D_2=configuration.D_fi,
        D_fo=configuration.D_fo,
        H_bolt=configuration.H_bolt,
        w=config.w,
        h=config.h,
        l_hole=config.l_hole,
        material_backplate=configuration.lug_material,
        material_bolts=configuration.fastener_material,
        num_bolts=len(configuration.fastener_positions),
        fastener_positions=configuration.fastener_positions)
    mass_list.append(configuration.mass)
    # MASS MINIMIZER:
mass_list = np.array(mass_list)
index_min = np.argmin(mass_list)
print(len(configurations))
print(vars(configurations[index_min]))
