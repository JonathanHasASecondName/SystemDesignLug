from configuration import Configuration


class ConfigurationValidator:
    """
    Don't touch! This file validates a single configuration. It creates a list of validators in the __init__ function
    and runs the tests of these validators in validate_configuration().
    """
    def __init__(self, validators: list):
        self.validators = validators

    def validate_configuration(self, configuration: Configuration):
        """
        This function validates a single configuration.
        Currently, it returns False as soon as one check fails, which makes it faster but less insightful when debugging
        """
        for validator in self.validators:
            if not validator.run_check(configuration):
                return False
        return True
