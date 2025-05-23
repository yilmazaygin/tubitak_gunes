import math

CONSTANT_EFF = 2.866752 # This value is used in excel constantly so we can use it in the code as well, also can be calculated by the get_constant_eff method in the Panles class
    
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

"""
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
"""
