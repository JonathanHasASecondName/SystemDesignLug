class Configuration:
    """
    Don't touch! A class is used to more effectively hold the information
    """
    def __init__(self,
                 fastener_positions,
                 D_fo,
                 D_fi,
                 thread_depth,
                 fastener_material,
                 lug_material,
                 H_bolt
                 ):
        self.fastener_positions = fastener_positions
        self.D_fo = D_fo
        self.D_fi = D_fi
        self.H_bolt = H_bolt
        self.thread_depth = thread_depth
        self.t_2 = None
        self.t_3 = None
        self.E_b = None
        self.alpha_b = None
        self.rho_b = None
        self.fastener_material = fastener_material
        self.lug_material = lug_material
        self.mass = None



