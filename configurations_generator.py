from configuration import Configuration


class ConfigurationsGenerator:
    """
    Generate different configurations to evaluate for the validator
    """
    def generate_configurations(self) -> list[Configuration]:
        """
        This function generates a list of all configurations that matches the requirements for forces.
        :return: A list of all the configurations.
        """
        configurations = [
            Configuration(
                flange_width=1,
                flange_spacing=1,
                flange_thickness=1,
                back_plate_thickness=1,
                space_craft_thickness=1,
                flange_hole_diameter=1,
                fastener_diameter=1,
                fastener_top_distance=1,
                fastener_side_distance=1
            )
        ]
        """
        CODE GOES BELOW
        """

        """
        CODE GOES ABOVE
        """
        return configurations
