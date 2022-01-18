import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


def url_formater(day=0):
    depart_time = datetime.today() + timedelta(days=day)
    return_time = depart_time + timedelta(days=7)

    dep_weekday = depart_time.strftime("%a")
    dep_month = depart_time.strftime("%b")
    dep_month_day = depart_time.strftime("+%d").replace('+0', '+')
    dep_year = depart_time.strftime("%Y")

    ret_weekday = return_time.strftime("%a")
    ret_month = return_time.strftime("%b")
    ret_month_day = return_time.strftime("+%d").replace('+0', '+')
    ret_year = return_time.strftime("%Y")

    URL = f"https://www.fly540.com/flights/nairobi-to-mombasa?isoneway=0&currency=USD&depairportcode=NBO&arrvairportcode=MBA&date_from=" \
          f"{dep_weekday}%2C{dep_month_day}+{dep_month}+{dep_year}" \
          f"&date_to={ret_weekday}%2C{ret_month_day}+{ret_month}+{ret_year}&adult_no=1&children_no=0&infant_no=0&searchFlight=&change_flight="
    return URL

URL = url_formater(day=10)
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
departs = soup.find(class_='fly5-depart').find_all(class_='fly5-result')
fly_backs = soup.find(class_="fly5-return").find_all(class_='fly5-result')

for depart in departs:
    for fly_back in fly_backs:
        print(depart.find(class_="flprice").text + " + " + fly_back.find(class_="flprice").text)




# print(departs)