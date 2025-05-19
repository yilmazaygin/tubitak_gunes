import math

CONSTANT_EFF = 2.866752 # This value is used in excel constantly so we can use it in the code as well, also can be calculated by the get_constant_eff method in the Panles class

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
    

class MomentData:
    """
    Data class to represent solar data and perform calculations related to solar angles and energy generation.

    Attributes:
        day (int): Day of the year.
        gmt (int): GMT offset.
        hour (float): Hour of the day.
        longitude (float): Longitude of the location.
        latitude (float): Latitude of the location.
        module_azimuth (float): Azimuth angle of the solar module.
        module_tilt (float): Tilt angle of the solar module.
        constant_eff (float): Constant efficiency of the solar panels.
    """
    def __init__(self, day: int, gmt: int, hour: float, longitude: float, latitude: float, module_azimuth: float, module_tilt: float, constant_eff: float ):
        """
        Initialize the solar data attributes and perform calculations.
        """
        self.day = day
        self.gmt = gmt
        self.hour = hour
        self.longitude = longitude
        self.latitude = latitude
        self.module_azimuth = module_azimuth
        self.module_tilt = module_tilt
        self.constant_eff = constant_eff

        # B value according to the day of the year
        self.data_B = (360 / 365) * (self.day - 81)

        # EOT (Equation of Time)
        self.eot = 9.87 * math.sin(math.radians(2 * self.data_B)) - 7.53 * math.cos(math.radians(self.data_B)) - 1.5 * math.sin(math.radians(self.data_B))

        # LSTM (Local Standard Time Meridian)
        self.lstm = 15 * self.gmt

        # Time correction
        self.tc = 4 * (self.longitude - self.lstm) + self.eot

        # Local solar time
        self.lst = self.hour + self.tc / 60

        # Hour angle
        self.hra = 15 * (self.lst - 12)

        # Declination angle
        self.dec_ang = 23.45 * math.sin(math.radians(self.data_B))

        # Elevation angle
        self.ev_ang = math.degrees(math.asin(
            math.sin(math.radians(self.dec_ang)) * math.sin(math.radians(self.latitude)) +
            math.cos(math.radians(self.dec_ang)) * math.cos(math.radians(self.latitude)) * math.cos(math.radians(self.hra))
        ))

        # Zenith angle
        self.zenith_ang = 90 - self.ev_ang

        # Azimuth angle calculation
        numerator = (
            math.sin(math.radians(self.dec_ang)) * math.cos(math.radians(self.latitude)) -
            math.cos(math.radians(self.dec_ang)) * math.sin(math.radians(self.latitude)) * math.cos(math.radians(self.hra))
        )
        denominator = math.cos(math.radians(self.ev_ang))

        cos_az_arg = numerator / denominator
        # acos argument must be in the range [-1, 1]
        cos_az_arg = max(min(cos_az_arg, 1), -1)
        azimuth_base = math.degrees(math.acos(cos_az_arg))

        if self.hra > 0:
            self.az_ang = 360 - azimuth_base
        else:
            self.az_ang = azimuth_base

        # Morning and afternoon azimuth angles
        self.azi_ang_mor = azimuth_base  # Morning angle (for hra <= 0)
        self.az_ang_past12 = 360 - azimuth_base  # Afternoon angle (for hra > 0)

        # Air mass
        self.air_mass = 1 / (math.cos(math.radians(self.zenith_ang)) + 0.50572 * (96.07995 - self.zenith_ang) ** -1.6364)

        # S incident
        self.s_incident = 1.353 * (0.7 ** (self.air_mass ** 0.678))

        # Fraction 
        self.fraction = (
            (math.cos(math.radians(self.ev_ang)) *
            math.sin(math.radians(self.module_tilt) * 
            math.cos(math.radians(self.az_ang - self.module_azimuth))))  +
            (math.sin(math.radians(self.ev_ang)) *
            math.cos(math.radians(self.module_tilt)))
        )

        # Solar irradiance on the module (used max to avoid negative values)
        self.s_module = max(0, self.s_incident * self.fraction)
        
        self.generated_kw = self.s_module * self.constant_eff 

    def print_data(self):
        print("----------------")
        print(f"VALUES: Day:{self.day}, GMT:{self.gmt}, Hour:{self.hour}, Longitude:{self.longitude}, Latitude:{self.latitude}, Module Azimuth:{self.module_azimuth}, Module Tilt:{self.module_tilt}, Constant Efficiency:{self.constant_eff} \n")
        print(f"B (deg): {self.data_B}")
        print(f"EOT: {self.eot}")
        print(f"LSTM: {self.lstm}")
        print(f"TC: {self.tc}")
        print(f"LST: {self.lst}")
        print(f"HRA: {self.hra}")
        print(f"Declination Angle: {self.dec_ang}")
        print(f"Elevation Angle: {self.ev_ang}")
        print(f"Zenith Angle: {self.zenith_ang}")
        print(f"Azimuth Angle Morning: {self.azi_ang_mor}")
        print(f"Azimuth Angle After 12: {self.az_ang_past12}")
        print(f"Azimuth Angle (Final): {self.az_ang}")
        print(f"Air Mass: {self.air_mass}")
        print(f"S Incident: {self.s_incident}")
        print(f"Fraction: {self.fraction}")
        print(f"S Module: {self.s_module} kW/m2")
        print(f"Generated kW: {self.generated_kw} kW")
        print("----------------")

class Calculation:
    """
    Class to perform calculations related to solar energy generation.
    """

    def daily_kw(self, moment_data: MomentData) -> float:
        """
        Calculate the total energy generated in a day by summing the energy generated each hour,
        ignoring any hours where data retrieval fails.

        Returns:
            float: Total energy generated in a day (kW).
        """
        sum_kw = 0

        for i in range(24):
            try:
                data = MomentData(
                    day=moment_data.day,
                    gmt=moment_data.gmt,
                    hour=i,
                    longitude=moment_data.longitude,
                    latitude=moment_data.latitude,
                    module_azimuth=moment_data.module_azimuth,
                    module_tilt=moment_data.module_tilt,
                    constant_eff=moment_data.constant_eff
                )
                sum_kw += data.generated_kw
            except Exception:
                continue

        return sum_kw

    def calc_month(self, moment_data: MomentData, month: int) -> float:
        """
        Calculate the total energy generated in a given month.

        Args:
            moment_data (MomentData): Base moment data for location and configuration.
            month (int): Month number (1 to 12).

        Returns:
            float: Total energy generated in the month (kW).
        """
        days_in_month = {
            1: 31, 2: 28, 3: 31, 4: 30,
            5: 31, 6: 30, 7: 31, 8: 31,
            9: 30, 10: 31, 11: 30, 12: 31
        }

        total_kw = 0
        base_day_of_year = sum(days_in_month[m] for m in range(1, month))

        for d in range(1, days_in_month[month] + 1):
            day_of_year = base_day_of_year + d
            moment_data.day = day_of_year
            total_kw += self.daily_kw(moment_data)

        return total_kw

    def calc_year(self, moment_data: MomentData) -> float:
        """
        Calculate the total energy generated in a year.

        Args:
            moment_data (MomentData): Base moment data for location and configuration.

        Returns:
            float: Total energy generated in the year (kW).
        """
        total_kw = 0
        for day in range(1, 366):  # 1 to 365
            moment_data.day = day
            total_kw += self.daily_kw(moment_data)

        return total_kw


# Test for Data class 
data = MomentData(
    day=1,
    gmt=2,
    hour=13,
    longitude=27.095316,
    latitude=38,
    module_azimuth=180,
    module_tilt=47,
    constant_eff= CONSTANT_EFF
)

data.print_data()

# Test for Calculation class
calc = Calculation()
print(f"Total energy generated in a day: {calc.daily_kw(data)} kW")

# Test for Calculation class
calc = Calculation()

# Aylık üretim (örnek: Ocak ayı)
january_kw = calc.calc_month(data, 1)
print(f"Total energy generated in January: {january_kw:.2f} kW")

# Yıllık üretim
year_kw = calc.calc_year(data)
print(f"Total energy generated in a year: {year_kw:.2f} kW")
