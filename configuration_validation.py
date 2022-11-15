from configuration import Configuration


class ConfigurationValidator:
    """
    Validate a single configuration
    """
    def __init__(self, validators: list):
        self.validators = validators

    def validate_configuration(self, configuration: Configuration):
        """
        Currently returns False as soon as one check fails, which makes it faster but less insightful when debugging
        """
        for validator in self.validators:
            if not validator.run_check(configuration):
                return False
        return True
