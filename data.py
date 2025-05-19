import math

class Data:
    def __init__(self, day:int, gmt:int, hour:float, longitude:float, latitude:float, module_azimuth:float, module_tilt:float):
        self.day = day
        self.gmt = gmt
        self.hour = hour
        self.longitude = longitude
        self.latitude = latitude
        self.module_azimuth = module_azimuth
        self.module_tilt = module_tilt

        self.data_B = (360/365)*(self.day-81)
        self.eot = 9.87 * math.sin(math.radians(2 * self.data_B)) - 7.53 * math.cos(math.radians(self.data_B)) - 1.5 * math.sin(math.radians(self.data_B))
        self.lstm = 15 * self.gmt
        self.tc = 4 * (self.longitude - self.lstm) + self.eot
        self.lst = self.hour + (self.tc / 60)
        self.hra = 15 * (self.lst - 12)

        self.dec_ang = 23.45 * math.sin(math.radians(self.data_B))
        self.ev_ang = math.degrees(math.asin(math.sin(math.radians(self.dec_ang))*math.sin(math.radians(self.latitude)) + math.cos(math.radians(self.dec_ang))*math.cos(math.radians(self.latitude))*math.cos(math.radians(self.hra))))
        self.zenith_ang = 90 - self.ev_ang
        
        self.azi_ang_mor = 168.4387025  # CALCULATE THIS VALUE
        self.az_ang_past12 = 360 - self.azi_ang_mor
        self.az_ang = self.azi_ang_mor if self.hour < 12.1 else self.az_ang_past12

        self.air_mass = 1 / (math.cos(math.radians(self.zenith_ang)) + 0.50572 * (96.07995 - self.zenith_ang) ** -1.6364)
        self.s_incident = 1.353 * (0.7**(self.air_mass**0.678)) # Implemet faster power
        self.fraction = 0.867551136 # CALCULATE THIS VALUE
        self.s_module = self.s_incident * self.fraction


    def print_data(self):
        print(f"Day: {self.day}")
        print(f"GMT: {self.gmt}")
        print(f"Hour: {self.hour}")
        print(f"Longitude: {self.longitude}")
        print(f"Latitude: {self.latitude}")
        print(f"Module Azimuth: {self.module_azimuth}")
        print(f"Module Tilt: {self.module_tilt}")
        print(f"EOT: {self.eot}")
        print(f"LSTM: {self.lstm}")
        print(f"TC: {self.tc}")
        print(f"LST: {self.lst}")
        print(f"HRA: {self.hra}")
        print(f"dec_ang: {self.dec_ang}")
        print(f"ev_ang: {self.ev_ang}")
        print(f"zenith_ang: {self.zenith_ang}")
        print(f"azi_ang_mor: {self.azi_ang_mor}")
        print(f"az_ang_past12: {self.az_ang_past12}")
        print(f"az_ang: {self.az_ang}")
        print(f"air_mass: {self.air_mass}")
        print(f"s_incident: {self.s_incident}")
        print(f"fraction: {self.fraction}")
        print(f"s_module: {self.s_module}")

# Example usage
data = Data(2, 2, 13, 27.095316, 38, 180, 33)
data.print_data()