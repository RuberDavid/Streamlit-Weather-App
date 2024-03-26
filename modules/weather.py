import openmeteo_requests
import typing
import requests_cache
import pandas as pd
import datetime
from retry_requests import retry

# Set up the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below



params = {
    "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain",
                "snowfall", "weather_code"],
    "timezone": "auto",
    "forecast_days": 1
}


def get_current_weather(location : dict) -> dict:
    """

    Parameters
    ----------
    location : dict
               Latitude and longitude as floats
    Returns
    -------
    dict
        current weather variables
    """

    url = 'https://api.open-meteo.com/v1/forecast'
    other_params = {
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain",
                    "snowfall", "weather_code"],
        "timezone": "auto",
        "forecast_days": 0
    }
    params = location | other_params

    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()

    weather = dict(current_temperature_2m=current.Variables(0).Value(),
                   current_relative_humidity_2m=current.Variables(1).Value(),
                   current_apparent_temperature=current.Variables(2).Value(),
                   current_is_day=current.Variables(3).Value(), current_precipitation=current.Variables(4).Value(),
                   current_rain=current.Variables(5).Value(), current_snowfall=current.Variables(6).Value(),
                   current_weather_code=current.Variables(7).Value())
    # TODO: get units and format accordingly
    return weather


def ge_last_month_weather(location:dict):
    """

    Parameters
    ----------
    location : dict

    Returns
    (min, max, avg): tuple
                    minimum, maximum and average temperatures from last month

    -------

    """
    today = pd.to_datetime('today') - datetime.timedelta( days = 3 )

    url = "https://archive-api.open-meteo.com/v1/archive"

    # sometimes there is no available data for the past three days
    today = today - datetime.timedelta(days=3)
    today_30 = today - datetime.timedelta(days=30)

    other_params = {
        "start_date": str(today_30.year) + '-' + '{:02d}'.format(today_30.month) + '-' + '{:02d}'.format(today_30.day),
        "end_date": str(today.year) + '-' + '{:02d}'.format(today.month) + '-' + '{:02d}'.format(today.day),
        "daily": ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean"],
        "timezone": "auto"
    }

    params = location | other_params
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    daily = response.Daily()

    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_mean = daily.Variables(2).ValuesAsNumpy()


    daily_data = {"date": pd.date_range( start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                                         end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                                         freq=pd.Timedelta(seconds=daily.Interval()),
                                         inclusive="left")
                  }

    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["temperature_2m_mean"] = daily_temperature_2m_mean

    df_daily = pd.DataFrame(data=daily_data)

    return df_daily['temperature_2m_max'].min(), df_daily['temperature_2m_max'].max(), df_daily['temperature_2m_max'].mean()




if __name__ == '__main__':

    location = {
        'latitude': 52.52,
        'longitude': 13.41
    }
    myweather = get_current_weather(location)
    print(myweather)
    print(get_last_month_weather(location))


