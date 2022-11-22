import numpy

from configurations_generator import ConfigurationsGenerator
from configurations_validation import ConfigurationsValidator


def main():
    """
    Don't touch! Basically a control file to handle all the different classes.
    """
    configuration_generator = ConfigurationsGenerator()
    configurations_validator = ConfigurationsValidator()

    configurations = configuration_generator.generate_configurations()
    configurations_validator.validate_configurations(configurations)

print("hello")
main()
