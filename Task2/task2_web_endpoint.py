# -*- coding: utf-8 -*-
import requests
"""
capture endpoint from web
https://www.hko.gov.hk/json/DYN_DAT_MINDS_FND.json
"""


def get_the_day_after_tomorrow_relative_humidity() -> str:
    """
    :return: Extract the relative humidity (e,g, 60 - 85%) for the day after tomorrow
    """
    url = f"https://www.hko.gov.hk/json/DYN_DAT_MINDS_FND.json"
    r = requests.get(url=url)
    print(r.json())
    if r.status_code == 200:
        # get 9-day Weather Forecast data list
        DYN_DAT_MINDS_FND = r.json()['DYN_DAT_MINDS_FND']
        # get max relative humidity of the day after tomorrow
        forecast_maxrh = DYN_DAT_MINDS_FND['Day3MaxRH']['Value_Eng']
        # get min relative humidity of the day after tomorrow
        forecast_minrh = DYN_DAT_MINDS_FND['Day3MinRH']['Value_Eng']
        return f"{forecast_minrh}-{forecast_maxrh}%"
    else:
        return f"Get Response Error, status code:{r.status_code},res:{r.content}"


if __name__ == '__main__':
    res = get_the_day_after_tomorrow_relative_humidity()
    print(res)