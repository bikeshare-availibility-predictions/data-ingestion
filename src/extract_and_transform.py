import pandas as pd
import requests
from datetime import datetime
import os 

    
class BikeShareDataSourceConfig():
    def __init__(self) -> None:
        self.WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


class BikeShareDataSource:
    """Extract and Transform bikeshare related information from the API."""

    def __init__(self, config: BikeShareDataSourceConfig) -> None:
        BIKE_BASE_ENDPOINT = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/" 
        self.config = config
        self.ENDPOINTS = {
            "station_information": BIKE_BASE_ENDPOINT + "station_information",
            "station_status": BIKE_BASE_ENDPOINT + "station_status",
            "weather_info": "https://api.openweathermap.org/data/2.5/weather?lat=43.6532&lon=-79.3832&appid=" + self.config.WEATHER_API_KEY
        }

    def _fetch_station_status(self) -> list[dict]:
        """Return a sorted list (by station_id) containing station status for all stations."""
        response = requests.get(self.ENDPOINTS["station_status"])
        response_data: dict = response.json()
        return response_data["data"]["stations"]

    def _fetch_station_information(self) -> list[dict]:
        """Return a sorted list (by station_id) containing station information for all stations."""
        response = requests.get(self.ENDPOINTS["station_information"])
        response_data: dict = response.json()
        return response_data["data"]["stations"]

    def _fetch_weather_information(self) -> tuple[int, int]:
        """Return (current temperature in Celcius, current weather type encoded according to the scheme)"""
        response = requests.get(self.ENDPOINTS["weather_info"])
        response_data: dict = response.json()
        return response_data["main"]["temp"] - 273.15, response_data["weather"][0]["id"]
    
    def fetch_bike_data(self) -> pd.DataFrame:
        """Return combined station information, status, and current query time"""
        station_status = self._fetch_station_status()
        station_information = self._fetch_station_information()
        current_temperature, current_weather = self._fetch_weather_information()
        query_time = datetime.now()

        id = []
        time = []
        num_bikes = []
        num_docks = []
        latitude = []
        longitude = []
        temperature = []
        weather_status = []
        status_i = 0
        information_i = 0
        while status_i < len(station_status) and information_i < len(station_information):
            status_station_id = int(station_status[status_i]["station_id"])
            information_station_id = int(station_information[information_i]["station_id"])
            if status_station_id < information_station_id:
                status_i += 1
            elif information_station_id < status_station_id:
                information_i += 1
            else:
                id.append(station_status[status_i]["station_id"])
                time.append(query_time)
                num_bikes.append(station_status[status_i]["num_bikes_available"])
                num_docks.append(station_status[status_i]["num_docks_available"])
                latitude.append(station_information[information_i]["lat"])
                longitude.append(station_information[information_i]["lon"])
                temperature.append(current_temperature)
                weather_status.append(current_weather)       
                status_i += 1
                information_i += 1
    
        df = pd.DataFrame({
            'StationID': id,
            'Time': time,
            'NumBikes': num_bikes,
            'NumDocks': num_docks,
            'Latitude': latitude,
            'Longitude': longitude,
            'Temperature': temperature,
            'WeatherStatus': weather_status
        })

        return df
