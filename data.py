import math

class Data:
    def __init__(self, day: int, gmt: int, hour: float, longitude: float, latitude: float, module_azimuth: float, module_tilt: float):
        self.day = day
        self.gmt = gmt
        self.hour = hour
        self.longitude = longitude
        self.latitude = latitude
        self.module_azimuth = module_azimuth
        self.module_tilt = module_tilt

        # B değeri (güneş yılına göre)
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

        # Azimuth angle hesaplama (doğru formül)
        numerator = (
            math.sin(math.radians(self.dec_ang)) * math.cos(math.radians(self.latitude)) -
            math.cos(math.radians(self.dec_ang)) * math.sin(math.radians(self.latitude)) * math.cos(math.radians(self.hra))
        )
        denominator = math.cos(math.radians(self.ev_ang))

        cos_az_arg = numerator / denominator
        # acos argümanı [-1, 1] aralığında olmalı
        cos_az_arg = max(min(cos_az_arg, 1), -1)
        azimuth_base = math.degrees(math.acos(cos_az_arg))

        if self.hra > 0:
            self.az_ang = 360 - azimuth_base
        else:
            self.az_ang = azimuth_base

        # Sabah ve öğleden sonra azimuth açılarını da ayrı tutalım
        self.azi_ang_mor = azimuth_base  # sabah açısı (hra <= 0 için)
        self.az_ang_past12 = 360 - azimuth_base  # öğleden sonra (hra > 0 için)

        # Air mass (hava kütlesi)
        self.air_mass = 1 / (math.cos(math.radians(self.zenith_ang)) + 0.50572 * (96.07995 - self.zenith_ang) ** -1.6364)

        # S incident (güneş ışınımı)
        self.s_incident = 1.353 * (0.7 ** (self.air_mass ** 0.678))

        # Fraction (modül ve güneş açılarının çarpımı)
        self.fraction = (
            math.cos(math.radians(self.ev_ang)) *
            math.sin(math.radians(self.module_tilt) * math.cos(math.radians(self.az_ang - self.module_azimuth)))  +
            math.sin(math.radians(self.ev_ang)) *
            math.cos(math.radians(self.module_tilt))
        )

        # Module üzerindeki güneş ışınımı (negatif olmasın diye max kullandık)
        self.s_module = max(0, self.s_incident * self.fraction)

    def print_data(self):
        print(f"Day: {self.day}")
        print(f"GMT: {self.gmt}")
        print(f"Hour: {self.hour}")
        print(f"Longitude: {self.longitude}")
        print(f"Latitude: {self.latitude}")
        print(f"Module Azimuth: {self.module_azimuth}")
        print(f"Module Tilt: {self.module_tilt}")
        print(f"B (deg): {self.data_B}")
        print(f"EOT: {self.eot}")
        print(f"LSTM: {self.lstm}")
        print(f"TC: {self.tc}")
        print(f"LST: {self.lst}")
        print(f"HRA: {self.hra}")
        print(f"Declination Angle: {self.dec_ang}")
        print(f"Elevation Angle: {self.ev_ang}")
        print(f"Zenith Angle: {self.zenith_ang}")
        print(f"Azimuth Angle Morning (azi_ang_mor): {self.azi_ang_mor}")
        print(f"Azimuth Angle After 12 (az_ang_past12): {self.az_ang_past12}")
        print(f"Azimuth Angle (final az_ang): {self.az_ang}")
        print(f"Air Mass: {self.air_mass}")
        print(f"S Incident: {self.s_incident}")
        print(f"Fraction: {self.fraction}")
        print(f"S Module: {self.s_module}")

# Test
data = Data(
    day=2,
    gmt=2,
    hour=13,
    longitude=27.095316,
    latitude=38,
    module_azimuth=180,
    module_tilt=33
)

data.print_data()
