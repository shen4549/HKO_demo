# -*- coding: utf-8 -*-
import requests
"""
capture endpoint from app
https://www.hko.gov.hk/locspc/data/find_e.xml
"""


def get_the_day_after_tomorrow_relative_humidity() -> str:
    """
    """
    headers={"Host":"pda.weather.gov.hk","user-agent":"locspc 7.7.2","UIDeviceType":"14.5"}
    url = f"https://pda.weather.gov.hk/locspc/data/fnd_e.xml"
    r = requests.get(url=url, headers=headers,verify=False)
    # print(r.json())
    if r.status_code == 200:
        # get 9-day Weather Forecast data list
        forecast_detail = r.json()['forecast_detail']
        the_day_after_tomorrow = forecast_detail[2]
        # get max relative humidity of the day after tomorrow
        forecast_maxrh = the_day_after_tomorrow['max_rh']
        # get min relative humidity of the day after tomorrow
        forecast_minrh = the_day_after_tomorrow['min_rh']
        return f"{forecast_minrh}-{forecast_maxrh}%"
    else:
        return f"Get Response Error, status code:{r.status_code},res:{r.content}"


if __name__ == '__main__':
    res = get_the_day_after_tomorrow_relative_humidity()
    print(res)