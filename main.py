import numpy

from configurations_generator import ConfigurationsGenerator
from configurations_validation import ConfigurationsValidator


def main():
    configuration_generator = ConfigurationsGenerator()
    configurations_validator = ConfigurationsValidator()

    configurations = configuration_generator.generate_configurations()
    configurations_validator.validate_configurations(configurations)


main()
