from moment_data import MomentData

class GeneratedKw:
    """
    Calculates and summarizes solar energy generation (in kW) for daily, monthly, and yearly periods
    using the MomentData class. Provides methods to compute total, maximum, and average generated kW,
    as well as best-performing days and hours. Includes formatted output for results.
    """
    def daily_kw(self, day: int, gmt: int, longitude: float, latitude: float, module_azimuth: float, module_tilt: float, constant_eff: float) -> dict:
        """
        Calculates solar energy generation statistics for a specific day.

        Args:
            day (int): Day of the year (1-365).
            gmt (int): GMT offset.
            longitude (float): Longitude of the location.
            latitude (float): Latitude of the location.
            module_azimuth (float): Azimuth angle of the solar module.
            module_tilt (float): Tilt angle of the solar module.
            constant_eff (float): Constant efficiency factor.

        Returns:
            dict: Dictionary containing daily generation statistics, including:
            - TotalKw Generated (float): Total kW generated during the day.
            - MaxKw In An Hour (float): Maximum kW generated in any hour.
            - Hour Produced Max Kw (int): Hour when maximum kW was generated.
            - Hours Generated Energy (list): List of hours with energy generation.
            - Total Percentage Of Energy Created  Hours / Total Hours (float): Fraction of hours with energy generation.

        """
        day_dict = {
                "Data": "Daily Data",
                "Day": day,
                "TotalKw Generated": 0,
                "MaxKw In An Hour": 0,
                "Hour Produced Max Kw": 0,
                "Hours Generated Energy": [],
                "Total Percentage Of Energy Created  Hours / Total Hours": 0,
                }

        for i in range(24):
            try:
                data = MomentData(
                    day=day,
                    gmt=gmt,
                    hour=i,
                    longitude=longitude,
                    latitude=latitude,
                    module_azimuth=module_azimuth,
                    module_tilt=module_tilt,
                    constant_eff=constant_eff
                )
                if data.generated_kw > day_dict["MaxKw In An Hour"]:
                    day_dict["MaxKw In An Hour"] = data.generated_kw
                    day_dict["Hour Produced Max Kw"] = i
        
                if data.generated_kw > 0:
                    day_dict["Hours Generated Energy"].append(i)

                day_dict["TotalKw Generated"] += data.generated_kw

            except Exception:
                continue
    
        day_dict["Total Percentage Of Energy Created  Hours / Total Hours"] = len(day_dict["Hours Generated Energy"]) / 24

        return day_dict

    def monthly_kw(self, gmt:int, longitude: float, latitude: float, module_azimuth: float, module_tilt: float, constant_eff: float, month: int) -> dict:
        """
        Calculates solar energy generation statistics for a specific month.

        Args:
            gmt (int): GMT offset.
            longitude (float): Longitude of the location.
            latitude (float): Latitude of the location.
            module_azimuth (float): Azimuth angle of the solar module.
            module_tilt (float): Tilt angle of the solar module.
            constant_eff (float): Constant efficiency factor.
            month (int): Month of the year (1-12).

        Returns:
            dict: Dictionary containing monthly generation statistics, including:
            - Total Kw Generated (float): Total kW generated during the month.
            - Best Day (dict): Day with the highest total kW and its value.
            - Best Hour (dict): Day, hour, and kW value of the highest hourly generation.
            - Average Daily Kw (float): Average daily kW generation for the month.
        """
        days_in_month = {
            1: 31, 2: 28, 3: 31, 4: 30,
            5: 31, 6: 30, 7: 31, 8: 31,
            9: 30, 10: 31, 11: 30, 12: 31
        }
        
        month_data = {
            "Data": "Monthly Data",
            "Month": month,
            "Total Days": days_in_month[month],
            "Total Kw Generated": 0,
            "Best Day": {"Day":0, "Kw":0},
            "Best Hour": {"Day": 0, "Hour": 0, "Kw": 0},
            "Average Daily Kw": 0,
        }

        base_day_of_year = sum(days_in_month[m] for m in range(1, month))
        for d in range(1, days_in_month[month] + 1):
            day_of_year = base_day_of_year + d
            daily_data = self.daily_kw(day_of_year, gmt, longitude, latitude, module_azimuth, module_tilt, constant_eff)

            month_data["Total Kw Generated"] += daily_data["TotalKw Generated"]

            if daily_data["TotalKw Generated"] > month_data["Best Day"]["Kw"]:
                month_data["Best Day"]["Kw"] = daily_data["TotalKw Generated"]
                month_data["Best Day"]["Day"] = d

            if daily_data["MaxKw In An Hour"] > month_data["Best Hour"]["Kw"]:
                month_data["Best Hour"]["Kw"] = daily_data["MaxKw In An Hour"]
                month_data["Best Hour"]["Day"] = d
                month_data["Best Hour"]["Hour"] = daily_data["Hour Produced Max Kw"]

        month_data["Average Daily Kw"] = month_data["Total Kw Generated"] / days_in_month[month]
        return month_data
    
    def yearly_kw(self, gmt:int, longitude: float, latitude: float, module_azimuth: float, module_tilt: float, constant_eff: float) -> dict:
        """
        Calculates solar energy generation statistics for an entire year.

        Args:
            gmt (int): GMT offset.
            longitude (float): Longitude of the location.
            latitude (float): Latitude of the location.
            module_azimuth (float): Azimuth angle of the solar module.
            module_tilt (float): Tilt angle of the solar module.
            constant_eff (float): Constant efficiency factor.

        Returns:
            dict: Dictionary containing yearly generation statistics, including:
            - Total Kw Generated (float): Total kW generated during the year.
            - Best Month (dict): Month with the highest total kW and its value.
            - Best Day (dict): Month, day, and kW value of the highest daily generation.
            - Best Hour (dict): Month, day, hour, and kW value of the highest hourly generation.
            - Average Daily Kw (float): Average daily kW generation for the year.
            - Average Monthly Kw (float): Average monthly kW generation for the year.
        """
        year_data = {
            "Data": "Yearly Data",
            "Total Kw Generated": 0,
            "Best Month": {"Month": 0, "Kw": 0},
            "Best Day": {"Month": 0, "Day": 0, "Kw": 0},
            "Best Hour": {"Month": 0, "Day": 0, "Hour": 0, "Kw": 0},
            "Average Daily Kw": 0,
            "Average Monthly Kw": 0,
        }

        for month in range(1, 13):
            monthly_data = self.monthly_kw(gmt, longitude, latitude, module_azimuth, module_tilt, constant_eff, month)
            year_data["Total Kw Generated"] += monthly_data["Total Kw Generated"]

            if monthly_data["Total Kw Generated"] > year_data["Best Month"]["Kw"]:
                year_data["Best Month"]["Kw"] = monthly_data["Total Kw Generated"]
                year_data["Best Month"]["Month"] = month

            if monthly_data["Best Day"]["Kw"] > year_data["Best Day"]["Kw"]:
                year_data["Best Day"]["Kw"] = monthly_data["Best Day"]["Kw"]
                year_data["Best Day"]["Month"] = month
                year_data["Best Day"]["Day"] = monthly_data["Best Day"]["Day"]

            if monthly_data["Best Hour"]["Kw"] > year_data["Best Hour"]["Kw"]:
                year_data["Best Hour"]["Kw"] = monthly_data["Best Hour"]["Kw"]
                year_data["Best Hour"]["Month"] = month
                year_data["Best Hour"]["Day"] = monthly_data["Best Hour"]["Day"]
                year_data["Best Hour"]["Hour"] = monthly_data["Best Hour"]["Hour"]

        year_data["Average Daily Kw"] = year_data["Total Kw Generated"] / 365
        year_data["Average Monthly Kw"] = year_data["Total Kw Generated"] / 12

        return year_data

    def formatted_print(self, data:dict) -> None:
        """
        Nicely prints the contents of a dictionary, including nested dictionaries, for displaying
        solar generation statistics in a readable format.

        Args:
            data (dict): Dictionary containing generation statistics (daily, monthly, or yearly).

        Returns:
            None
        """
        print("\n----------------")
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"{key}: {value}")
        print("----------------")

"""
# Test
data = MomentData(
    day=1,
    gmt=2,
    hour=13,
    longitude=27.095316,
    latitude=38,
    module_azimuth=180,
    module_tilt=47,
    constant_eff= 2.866752
)


generated_kw = GeneratedKw()
generated_kw.formatted_print(generated_kw.daily_kw(1, 2, 27.095316, 38, 180, 47, 2.866752))
generated_kw.formatted_print(generated_kw.monthly_kw(2, 27.095316, 38, 180, 47, 2.866752, 1))
generated_kw.formatted_print(generated_kw.yearly_kw(2, 27.095316, 38, 180, 47, 2.866752))
"""