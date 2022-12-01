import numpy as np

from configurations_generator import generate_configurations
from validation_checks import bearing_check
from validation_checks import pull_push_through_check
from validation_checks import thermal_stress_check
from materials_list import materials_list
import config

configurations = generate_configurations()

for configuration in configurations:
    # 1. BEARING CHECK
    configuration.t_2 = bearing_check.calculate_t2(
        configuration.fastener_positions,
        configuration.D_fi,
        materials_list[configuration.lug_material]["bearing_stress"],
        config.external_forces,
        config.external_moments
    )
    configuration.t_3 = bearing_check.calculate_t2(
        configuration.fastener_positions,
        configuration.D_fi,
        materials_list[config.spacecraft_material]["bearing_stress"],
        config.external_forces,
        config.external_moments
    )
    # 2. PULL/PUSH THROUGH CHECK:
    pull_push_through_check_t2 = pull_push_through_check.calculate_t2(
        configuration.fastener_positions,
        configuration.D_fi,
        materials_list[configuration.lug_material]['shear_stress'],
        config.external_forces,
        np.array([0, config.w/2, 0]),
        config.external_moments
    )
    if pull_push_through_check_t2 > configuration.t_2:
        configuration.t_2 = pull_push_through_check_t2
    pull_push_through_check_t3 = pull_push_through_check.calculate_t2(
        configuration.fastener_positions,
        configuration.D_fi,
        materials_list[config.spacecraft_material]['shear_stress'],
        config.external_forces,
        np.array([0, config.w/2, 0]),
        config.external_moments
    )
    if pull_push_through_check_t3 > configuration.t_3:
        configuration.t_3 = pull_push_through_check_t3

    print(configuration.t_2, configuration.t_3)

    # 3. COMPLIANCE CHECK:

    # 4. THERMAL STRESS CHECK:
