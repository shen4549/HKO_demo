# HKO_demo

## Setup guide
pip3 install -r requirements.txt

## Task 1
### *** Solution selection ***

My choice is Appium+pytest.

I think robotframework+appium actually works better when put into production, but pytest+appium is lighter and more suitable for demo.

I used robotframework in past projects.

### *** Design ***

1.Click all buttons on the page to ensure their usability and functionality

2.(Key point)Check the accuracy of key data, invoke api to get the data and compare it with the data displayed on the UI

3.Check the UI elements of the page

4.Swipe the page to check undisplayed UI elements.

### *** How to run test ***
1. cd Task1
2. python3 -m pytest  01_9days_pytest.py --html=report.html




### *** What I did in Task1 ***

1.Download apk from website.(I used Android Emulator)

2.Analyze the application to get the package name and appActivity

3.Use Appium inspector to get elements' xpath and write automation testcase

4.Debug testcase and generate test report


## Task2
### *** What I did in Task2 ***
1. Use charles capture the releated API endpoint on IOS "https://pda.weather.gov.hk/locspc/data/fnd_e.xml"
2. I used chrome to open the link 'https://www.hko.gov.hk/en/wxinfo/currwx/fnd.htm' and capture the endpoint 'https://www.hko.gov.hk/json/DYN_DAT_MINDS_FND.json'.
3. I found HKO_Open_Data_API_Documentation.pdf.

### *** How to run test ***
0. cd Task2
1. python3 task2_openapi.py
2. python3 task2_app_endpoint.py
3. python3 task2_web_endpoint.py


