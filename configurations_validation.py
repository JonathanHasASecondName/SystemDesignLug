from configuration import Configuration

from configuration_validation import ConfigurationValidator
from validation_checks.bearing_check import BearingChecker
from validation_checks.pull_push_through_check import PullPushThroughChecker
from validation_checks.thermal_stress_check import ThermalStressChecker


class ConfigurationsValidator:
    """
    Validate a list of configurations
    """
    def __init__(self):
        self.configuration_validator = ConfigurationValidator([BearingChecker(),
                                                               PullPushThroughChecker(),
                                                               ThermalStressChecker()])

    def validate_configurations(self, configurations: list[Configuration]):
        results = []
        for configuration in configurations:
            results.append(self.configuration_validator.validate_configuration(configuration))
        print(results)