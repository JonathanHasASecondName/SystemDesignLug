class Configuration:
    """
    Don't touch! A class is used to more effectively hold the information
    """
    def __init__(self,
                 fastener_positions,
                 D_fo,
                 D_fi,
                 ):
        self.fastener_positions = fastener_positions
        self.D_fo = D_fo
        self.D_fi = D_fi
        self.t_2 = None
        self.t_3 = None
        self.E_b = None
        self.alpha_b = None
        self.rho_b = None


