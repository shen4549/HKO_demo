# -*- coding: utf-8 -*-
import requests
"""
Use open api
https://data.weather.gov.hk/weatherAPI/doc/HKO_Open_Data_API_Documentation.pdf
"""


def get_the_day_after_tomorrow_relative_humidity(datatype: str, lang: str) -> str:
    """
    lang:en,tc,sc
    datatype:fnd  9-day Weather Forecast
    :return: Extract the relative humidity (e,g, 60 - 85%) for the day after tomorrow
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType={datatype}&lang={lang}"
    r = requests.get(url=url)
    # print(r.json())
    if r.status_code == 200:
        # get 9-day Weather Forecast data list
        weather_forecast = r.json()['weatherForecast']
        # get the day after tomorrow data
        the_day_after_tomorrow = weather_forecast[2]
        # print(theDayAfterTomorrow)
        # get min relative humidity of the day after tomorrow
        forecast_minrh = the_day_after_tomorrow['forecastMinrh']['value']
        # get max relative humidity of the day after tomorrow
        forecast_maxrh = the_day_after_tomorrow['forecastMaxrh']['value']
        return f"{forecast_minrh}-{forecast_maxrh}%"
    else:
        return f"Get Response Error, status code:{r.status_code},res:{r.content}"


if __name__ == '__main__':
    res = get_the_day_after_tomorrow_relative_humidity("fnd", "en")
    print(res)