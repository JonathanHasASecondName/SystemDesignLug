import numpy as np
import csv

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
        config.external_forces*config.force_safety_factor,
        0,
        config.external_moments)

    configuration.t_3 = bearing_check.calculate_t2(
        configuration.fastener_positions,
        configuration.D_fi,
        materials_list[config.spacecraft_material]["bearing_stress"],
        config.external_forces*config.force_safety_factor,
        0,
        config.external_moments)

    # print("BC: ", configuration.t_2, configuration.t_3)

    # 2. PULL/PUSH THROUGH CHECK:
    pull_push_through_check_t2 = pull_push_through_check.calculate_t2(
        coordinate_array=configuration.fastener_positions,
        D_o=configuration.D_fi,
        tau_yield=materials_list[configuration.lug_material]['shear_stress'],
        forces=config.external_forces*config.force_safety_factor,
        force_location=force_location,
        moment=config.external_moments)
    if pull_push_through_check_t2 > configuration.t_2:
        configuration.t_2 = pull_push_through_check_t2
    pull_push_through_check_t3 = pull_push_through_check.calculate_t2(
        configuration.fastener_positions,
        configuration.D_fi,
        materials_list[config.spacecraft_material]['shear_stress'],
        config.external_forces*config.force_safety_factor,
        force_location,
        config.external_moments)
    if pull_push_through_check_t3 > configuration.t_3:
        configuration.t_3 = pull_push_through_check_t3
    # print("PPTC: ", pull_push_through_check_t2, pull_push_through_check_t3)
    # print("FINAL: ", configuration.t_2, configuration.t_3, '\n')

    # 3. COMPLIANCE CHECK:

    Thermal_loads_back_plate = thermal_stress_check.calculate_in_plane_loads(
        alpha_c=materials_list[config.lug_material]['thermal_expansion_coeff']/1e6,
        alpha_b=materials_list[configuration.fastener_material]['thermal_expansion_coeff']/1e6,
        delta_T=115,
        youngs_mod_fastener=materials_list[configuration.fastener_material]['Youngs_modulus'],
        area_sm=3.14*configuration.D_fi*configuration.D_fi,
        youngs_mod_clam=materials_list[config.lug_material]['Youngs_modulus'],
        D_fi=configuration.D_fi,
        D_fo=configuration.D_fo,
        d_sha=configuration.fastener_minor_diameter,
        t=configuration.t_2,
        L_sha=configuration.t_3 + configuration.t_2
    )

    Thermal_loads_vehicle_wall = thermal_stress_check.calculate_in_plane_loads(
        alpha_c=materials_list[config.spacecraft_material]['thermal_expansion_coeff']/1e6,
        alpha_b=materials_list[configuration.fastener_material]['thermal_expansion_coeff']/1e6,
        delta_T=115,
        youngs_mod_fastener=materials_list[configuration.fastener_material]['Youngs_modulus'],
        area_sm=3.14*configuration.D_fi*configuration.D_fi,
        youngs_mod_clam=materials_list[config.spacecraft_material]['Youngs_modulus'],
        D_fi=configuration.D_fi,
        D_fo=configuration.D_fo,
        d_sha=configuration.fastener_minor_diameter,
        t=configuration.t_3,
        L_sha=configuration.t_3+configuration.t_2
    )

    configuration.thermal_loads_backplate = Thermal_loads_back_plate
    configuration.thermal_loads_vehicle_wall = Thermal_loads_vehicle_wall

    #print(f"SC alpha: : {materials_list[config.spacecraft_material]['thermal_expansion_coeff']/1e6}\n FAST alpha : {materials_list[configuration.fastener_material]['thermal_expansion_coeff']/1e6}")
    #print(f"Thermal Loads Backplate : {Thermal_loads_back_plate}\n Thermal Loads Vehicle Wall : {Thermal_loads_vehicle_wall}\n")

    # 4. THERMAL STRESS CHECK BACKPLATE:

    # take thermal loads, add them to original loads, and re-run bearing check to see if it passes

    thermal_check = bearing_check.check_thickness(
        configuration.fastener_positions,
        configuration.D_fi,
        materials_list[configuration.lug_material]["bearing_stress"],
        config.external_forces*config.force_safety_factor,
        configuration.thermal_loads_backplate*config.thermal_loads_safety_factor,
        config.external_moments,
        configuration.t_2)

    while thermal_check == False:

        thermal_loads_t_2 = bearing_check.calculate_t2(
            configuration.fastener_positions,
            configuration.D_fi,
            materials_list[configuration.lug_material]["bearing_stress"],
            config.external_forces * config.force_safety_factor,
            configuration.thermal_loads_backplate*config.thermal_loads_safety_factor,
            config.external_moments
        )

        configuration.t_2 = thermal_loads_t_2

        Thermal_loads_back_plate = thermal_stress_check.calculate_in_plane_loads(
            alpha_c=materials_list[config.lug_material]['thermal_expansion_coeff'] / 1e6,
            alpha_b=materials_list[configuration.fastener_material]['thermal_expansion_coeff'] / 1e6,
            delta_T=115,
            youngs_mod_fastener=materials_list[configuration.fastener_material]['Youngs_modulus'],
            area_sm=3.14 * configuration.D_fi * configuration.D_fi,
            youngs_mod_clam=materials_list[config.lug_material]['Youngs_modulus'],
            D_fi=configuration.D_fi,
            D_fo=configuration.D_fo,
            d_sha=configuration.fastener_minor_diameter,
            t=configuration.t_2,
            L_sha=configuration.t_3 + configuration.t_2
        )

        Thermal_loads_vehicle_wall = thermal_stress_check.calculate_in_plane_loads(
            alpha_c=materials_list[config.spacecraft_material]['thermal_expansion_coeff'] / 1e6,
            alpha_b=materials_list[configuration.fastener_material]['thermal_expansion_coeff'] / 1e6,
            delta_T=115,
            youngs_mod_fastener=materials_list[configuration.fastener_material]['Youngs_modulus'],
            area_sm=3.14 * configuration.D_fi * configuration.D_fi,
            youngs_mod_clam=materials_list[config.spacecraft_material]['Youngs_modulus'],
            D_fi=configuration.D_fi,
            D_fo=configuration.D_fo,
            d_sha=configuration.fastener_minor_diameter,
            t=configuration.t_3,
            L_sha=configuration.t_3 + configuration.t_2
        )

        configuration.thermal_loads_backplate = Thermal_loads_back_plate
        configuration.thermal_loads_vehicle_wall = Thermal_loads_vehicle_wall

        thermal_check = bearing_check.check_thickness(
            configuration.fastener_positions,
            configuration.D_fi,
            materials_list[configuration.lug_material]["bearing_stress"],
            config.external_forces * config.force_safety_factor,
            configuration.thermal_loads_backplate*config.thermal_loads_safety_factor,
            config.external_moments,
            configuration.t_2)

        # 4. THERMAL STRESS CHECK VEHICLE WALL:

        # take thermal loads, add them to original loads, and re-run bearing check to see if it passes

        thermal_check = bearing_check.check_thickness(
            configuration.fastener_positions,
            configuration.D_fi,
            materials_list[configuration.lug_material]["bearing_stress"],
            config.external_forces * config.force_safety_factor,
            configuration.thermal_loads_vehicle_wall * config.thermal_loads_safety_factor,
            config.external_moments,
            configuration.t_2)

        while thermal_check == False:
            thermal_loads_t_2 = bearing_check.calculate_t2(
                configuration.fastener_positions,
                configuration.D_fi,
                materials_list[configuration.lug_material]["bearing_stress"],
                config.external_forces * config.force_safety_factor,
                configuration.thermal_loads_vehicle_wall * config.thermal_loads_safety_factor,
                config.external_moments
            )

            configuration.t_2 = thermal_loads_t_2

            Thermal_loads_back_plate = thermal_stress_check.calculate_in_plane_loads(
                alpha_c=materials_list[config.lug_material]['thermal_expansion_coeff'] / 1e6,
                alpha_b=materials_list[configuration.fastener_material]['thermal_expansion_coeff'] / 1e6,
                delta_T=115,
                youngs_mod_fastener=materials_list[configuration.fastener_material]['Youngs_modulus'],
                area_sm=3.14 * configuration.D_fi * configuration.D_fi,
                youngs_mod_clam=materials_list[config.lug_material]['Youngs_modulus'],
                D_fi=configuration.D_fi,
                D_fo=configuration.D_fo,
                d_sha=configuration.fastener_minor_diameter,
                t=configuration.t_2,
                L_sha=configuration.t_3 + configuration.t_2
            )

            Thermal_loads_vehicle_wall = thermal_stress_check.calculate_in_plane_loads(
                alpha_c=materials_list[config.spacecraft_material]['thermal_expansion_coeff'] / 1e6,
                alpha_b=materials_list[configuration.fastener_material]['thermal_expansion_coeff'] / 1e6,
                delta_T=115,
                youngs_mod_fastener=materials_list[configuration.fastener_material]['Youngs_modulus'],
                area_sm=3.14 * configuration.D_fi * configuration.D_fi,
                youngs_mod_clam=materials_list[config.spacecraft_material]['Youngs_modulus'],
                D_fi=configuration.D_fi,
                D_fo=configuration.D_fo,
                d_sha=configuration.fastener_minor_diameter,
                t=configuration.t_3,
                L_sha=configuration.t_3 + configuration.t_2
            )

            configuration.thermal_loads_backplate = Thermal_loads_back_plate
            configuration.thermal_loads_vehicle_wall = Thermal_loads_vehicle_wall

            thermal_check = bearing_check.check_thickness(
                configuration.fastener_positions,
                configuration.D_fi,
                materials_list[configuration.lug_material]["bearing_stress"],
                config.external_forces * config.force_safety_factor,
                configuration.thermal_loads_vehicle_wall * config.thermal_loads_safety_factor,
                config.external_moments,
                configuration.t_2)


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
mass_list = np.argsort(mass_list)

print(vars(configurations[mass_list[0]]))
print(vars(configurations[mass_list[1]]))
print(vars(configurations[mass_list[2]]))
print(vars(configurations[mass_list[3]]))
print(vars(configurations[mass_list[4]]))
