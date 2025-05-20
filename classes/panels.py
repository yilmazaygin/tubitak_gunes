class Panles:
    """
    Class to represent solar panels and calculate their constant efficiency.
    Attributes:
        module_eff (float): Efficiency of the solar module.
        dim_x (float): Dimension of the solar module in x direction.
        dim_y (float): Dimension of the solar module in y direction.
        panel_amount (int): Number of solar panels.
    """
    def __init__(self, module_eff:float, dim_x:float, dim_y:float, panel_amount:int):
        """
        Initialize the solar panel attributes.
        """
        self.module_eff = module_eff
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.panel_amount = panel_amount

    def get_constant_eff(self) -> float:
        """
        Calculate the constant efficiency of the solar panels.
        Returns:
            float: Constant efficiency of the solar panels.
        """
        return self.module_eff * self.dim_x * self.dim_y * self.panel_amount