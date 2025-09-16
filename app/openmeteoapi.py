import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

import logging
logger = logging.getLogger(__name__)

class OpenMeteo():
    
    def __init__(self, temperature_unit: str = "fahrenheit", wind_speed_unit: str = "mph", precipitation_unit: str = "inch"):
        # Setup the Open-Meteo API client with cache and retry on error
        self.cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        self.retry_session = retry(self.cache_session, retries = 5, backoff_factor = 0.2)
        self.openmeteo = openmeteo_requests.Client(session = self.retry_session)
        self.url = "https://api.open-meteo.com/v1/forecast"
        
        # Units setup
        self.temperature_unit = temperature_unit
        self.wind_speed_unit = wind_speed_unit
        self.precipitation_unit = precipitation_unit
        
    def params(self, latitute: float, longitute: float):
        return {
            "latitude": latitute,
            "longitude": longitute,
            "temperature_unit": self.temperature_unit,
            "wind_speed_unit": self.wind_speed_unit,
            "precipitation_unit": self.precipitation_unit,
        }
        
    def current_info_one_location(self, latitute: float, longitute: float):
        variables = {
            "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "apparent_temperature", "wind_speed_10m"],
        }
        
        params = self.params(latitute, longitute)
        params.update(variables)
        
        try:
            responses = self.openmeteo.weather_api(self.url, params=params)
            if responses:
                response = responses[0].Current()
                
                current_info = {}
                for idx, info in enumerate(params["current"]):
                    current_info[info] = response.Variables(idx).Value()
                return current_info
        except Exception as e:
            logger.error(f"[OpenMeteo API] Error has occured: {str(e)}")
        
if __name__ == "__main__":
    
    openmeteo = OpenMeteo()
    current_info = openmeteo.current_info_one_location(41.85, -87.65)
    
    print(current_info)
        
    