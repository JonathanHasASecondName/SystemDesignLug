class Configuration:
    """
    Don't touch! A class is used to more effectively hold the information
    """
    def __init__(self,
                 flange_width,
                 flange_spacing,
                 flange_thickness,
                 back_plate_thickness,
                 space_craft_thickness,
                 flange_hole_diameter,
                 fastener_diameter,
                 fastener_top_distance,
                 fastener_side_distance
                 ):
        self.flange_width = flange_width
        self.flange_spacing = flange_spacing
        self.flange_thickness = flange_thickness
        self.back_plate_thickness = back_plate_thickness
        self.space_craft_thickness = space_craft_thickness
        self.flange_hole_diameter = flange_hole_diameter
        self.fastener_diameter = fastener_diameter
        self.fastener_top_distance = fastener_top_distance
        self.fastener_side_distance = fastener_side_distance
