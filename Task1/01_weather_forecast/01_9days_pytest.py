import requests
import pytest,time
from datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import logging
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别
    format='%(asctime)s - %(levelname)s - %(message)s'  # 设置日志格式
)
capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='emulator-5554',
    appPackage='hko.MyObservatory_v1_0',
    appActivity='.AgreementPage',
    language='en',
    noReset=True
)

appium_server_url = 'http://localhost:4723'

# Suite setup
@pytest.fixture(scope="class")
def setup_class() -> webdriver.Remote:
    driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
    driver.implicitly_wait(10)
    driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageView[@content-desc="Next page"]').click()
    driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageView[@content-desc="Next page"]').click()
    driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageView[@content-desc="Close"]').click()
    wait = WebDriverWait(driver, 5)
    wait.until(expected_conditions.presence_of_element_located(
        (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Local Weather selected"]')))
    # self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Local Weather selected"]')
    yield driver
    print("tear down")
    driver.quit()

def take_screenshot(driver, test_name):
    """使用测试用例名称保存截图"""
    screenshot_file = f"screenshots/{test_name}.png"
    driver.get_screenshot_as_file(screenshot_file)
    print(f"Screenshot saved as {screenshot_file}")

# 通过APP的APi 获取数据进行对比
def get_nine_days_data()-> dict[str,str]:
    headers={"Host":"pda.weather.gov.hk","user-agent":"locspc 7.7.2","UIDeviceType":"14.5"}
    url = f"https://pda.weather.gov.hk/locspc/data/fnd_e.xml"
    r = requests.get(url=url, headers=headers,verify=False)
    return r.json()
nine_days_data = get_nine_days_data()

class TestAppium:
    # 测试进入该页面的入口
    def test_entrance_of_9days_forecast(self,setup_class) -> None:
        driver = setup_class
        driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Navigate up"]').click()
        driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/title" and @text="Forecast & Warning Services"]').click()
        driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/title" and @text="9-Day Forecast"]').click()
        wait = WebDriverWait(driver,5)
        wait.until(expected_conditions.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@text="Weather Forecast"]')))
        take_screenshot(driver,"test_entrance_of_9days_forecast")

    # 测试切换tab Local Forecast
    def test_tab_of_Local_Forecast(self,setup_class) -> None:
        driver = setup_class
        driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Local Forecast"]').click()
        icon = driver.find_element(AppiumBy.ID, 'hko.MyObservatory_v1_0:id/local_forecast_Icon')
        assert icon.is_displayed() == True
        text = driver.find_element(by=AppiumBy.ID, value='local_forecast_details').text

    # 测试切换tab Extended Outlook
    def test_tab_of_Extended_Outlook(self,setup_class) -> None:
        driver = setup_class
        driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Extended Outlook"]').click()
        max_image = driver.find_element(AppiumBy.ID, 'hko.MyObservatory_v1_0:id/extended_outlook_max_temp_layout')
        assert max_image.is_displayed() == True
        min_image = driver.find_element(AppiumBy.ID, 'hko.MyObservatory_v1_0:id/extended_outlook_min_temp_layout')
        assert min_image.is_displayed() == True
        mslp_image = driver.find_element(AppiumBy.ID, 'hko.MyObservatory_v1_0:id/extended_outlook_mslp_layout')
        assert mslp_image.is_displayed() == True

    # 测试切换tab 9days_forecast
    def test_tab_of_9days_forecast(self,setup_class) -> None:
        driver = setup_class
        driver.find_element(by=AppiumBy.XPATH, value='//android.widget.LinearLayout[@content-desc="9-Day Forecast"]').click()
        icon = driver.find_element(AppiumBy.ID, 'hko.MyObservatory_v1_0:id/mainAppSevenDayGenSit')
        assert icon.is_displayed() == True

    # 测试 9days summary content
    def test_app_seven_day_gen(self,setup_class)-> None:
        driver = setup_class
        SevendayText = driver.find_element(by=AppiumBy.ID, value='mainAppSevenDayGenSit')
        # 获取APi返回的数据
        mainAppSevenDayGenSit_data = nine_days_data['general_situation']
        # 获取Ui数据
        mainAppSevenDayGenSit_content = SevendayText.text
        logging.info("API Data："+mainAppSevenDayGenSit_data)
        logging.info("APP Data："+mainAppSevenDayGenSit_content)
        assert mainAppSevenDayGenSit_data == mainAppSevenDayGenSit_content

    # 测试今日的日期
    def test_today_date(self,setup_class):
        driver = setup_class
        # 获取今天的Ui日期数据
        today_date_ui = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/sevenday_forecast_date"]').text
        # 获取今天的APi日期数据
        today_date_api = nine_days_data['forecast_detail'][0]['forecast_date']
        # 将字符串转换为日期对象
        date_obj = datetime.strptime(today_date_api, "%Y%m%d")
        # 格式化输出
        formatted_date = date_obj.strftime("%d %b")
        assert today_date_ui == formatted_date

    # 测试今天的各种数据，和APi数据对比
    def test_today_information(self,setup_class)-> None:
        driver = setup_class
        # 获取UI的temp
        today_temp_ui = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/sevenday_forecast_temp"]').text
        # 获取UI的wind
        today_wind_ui = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/sevenday_forecast_wind"]').text
        # 获取UI的desc
        today_desc_ui = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/sevenday_forecast_details"]').text
        # 获取UI的rh
        today_rh_ui = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/sevenday_forecast_rh"]').text
        # 获取UI的psr
        today_psr_ui = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/psrText"]').text
        logging.info(f"ui data: {today_temp_ui},{today_wind_ui},{today_desc_ui},{today_rh_ui}")
        # 获取API的各种数据
        today_data = nine_days_data['forecast_detail'][0]
        today_wind_api = today_data['wind_info']
        today_desc_api = today_data['wx_desc']
        today_psr_api = today_data['psr']
        today_rh_api = f"{today_data['min_rh']} - {today_data['max_rh']}%"
        today_temp_api = f"{today_data['min_temp']} - {today_data['max_temp']}°C"

        # 对比UI和API的数据
        assert today_temp_ui == today_temp_api
        assert today_wind_ui == today_wind_api
        assert today_desc_ui == today_desc_api
        assert today_rh_ui == today_rh_api
        assert today_psr_ui == today_psr_api

    # 滑动页面滑到最后一天，测试滑动功能
    def test_swipe_to_last_day(self,setup_class):
        driver = setup_class
        # 获取屏幕尺寸
        size = driver.get_window_size()
        width = size['width']
        height = size['height']

        # 计算起始和结束坐标
        x = width * 0.5
        start_y = height * 0.9  # 从中间滑动
        end_y = height * 0.5
        # 执行滑动操作
        time.sleep(2)
        driver.swipe(x, start_y, x, end_y, 200)
        driver.swipe(x, start_y, x, end_y, 200)
        driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/sevenday_forecast_temp"])[3]')

    # 测试最后一天的数据
    def test_last_day_information(self,setup_class)-> None:
        driver = setup_class
        last_day_temp_ui = driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/sevenday_forecast_temp"])[3]').text
        last_day_wind_ui = driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/sevenday_forecast_wind"])[3]').text
        last_day_desc_ui = driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/sevenday_forecast_details"])[3]').text
        last_day_rh_ui = driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/sevenday_forecast_rh"])[3]').text
        logging.info(f"ui data: {last_day_temp_ui},{last_day_wind_ui},{last_day_desc_ui},{last_day_rh_ui}")
        last_day_data = nine_days_data['forecast_detail'][8]
        last_day_wind_api = last_day_data['wind_info']
        last_day_desc_api = last_day_data['wx_desc']
        last_day_rh_api = f"{last_day_data['min_rh']} - {last_day_data['max_rh']}%"
        last_day_temp_api = f"{last_day_data['min_temp']} - {last_day_data['max_temp']}°C"
        assert last_day_temp_ui == last_day_temp_api
        assert last_day_wind_ui == last_day_wind_api
        assert last_day_desc_ui == last_day_desc_api
        assert last_day_rh_ui == last_day_rh_api

    # 测试更新时间
    def test_update_time(self,setup_class):
        driver = setup_class
        update_time_ui = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/mainAppSevenDayUpdateTime"]').text
        next_update_time_ui = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="hko.MyObservatory_v1_0:id/next_update_time"]').text
        update_time_api = nine_days_data['updatedatetime']
        next_update_datetime_api = nine_days_data['next_updatedatetime']
        assert update_time_ui == update_time_api
        assert next_update_time_ui == next_update_datetime_api

    #测试Refresh button
    def test_refresh(self,setup_class)-> None:
        driver =setup_class
        refresh_button = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Refresh"]')
        refresh_button.click()
        time.sleep(5)

    # 测试bookmark button
    def test_bookmark(self,setup_class)-> None:
        driver = setup_class
        Bookmark_not_added = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Bookmark not added"]')
        # mark
        Bookmark_not_added.click()
        time.sleep(5)
        Bookmark_added = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Bookmark added"]')
        assert Bookmark_added.is_displayed() == True

        # cancel mark
        Bookmark_added.click()
        Bookmark_not_added = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Bookmark not added"]')
        assert Bookmark_not_added.is_displayed() == True

    # 测试more_option button
    def test_more_option(self,setup_class):
        driver = setup_class
        more_options = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageView[@content-desc="More options"]')
        more_options.click()
        remarks = driver.find_element(by=AppiumBy.ID, value='hko.MyObservatory_v1_0:id/title')
        remarks.click()
        webview = driver.find_element(by=AppiumBy.XPATH,value ='//android.view.ViewGroup[@resource-id="hko.MyObservatory_v1_0:id/toolbar"]/android.widget.TextView[@text="Remarks"]')
        driver.press_keycode(4)

if __name__ == '__main__':
    pytest.main()