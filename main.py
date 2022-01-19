import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from csv import writer


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

def find_year(direction, columns):
    year = [col for col in columns if direction in col.text][0].text
    return year.split()[-1]

URL = url_formater(day=10)
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
departs = soup.find(class_='fly5-depart').find_all(class_='fly5-result')
fly_backs = soup.find(class_="fly5-return").find_all(class_='fly5-result')

info_table = soup.find(class_="fly5-query").find_all(class_="col-5")
departing_year = find_year("Departing", info_table)
returning_year = find_year("Returning", info_table)
#
with open('flights_data.csv', 'w', encoding='utf8', newline='') as fl:
    the_writer = writer(fl, delimiter=';')
    header = ['outbound_departure_airport', 'outbound_arrival_airport', 'outbound_departure_time', 'outbound_arrival_time',
              'inbound_departure_airport', 'inbound_arrival_airport', 'inbound_departure_time', 'inbound_arrival_time', 'total_price', 'taxes']
    the_writer.writerow(header)

for depart in departs:
    for fly_back in fly_backs:
        print(depart.find("td", {"data-title": "Departs"}).find(class_="fltime").text, end="")
        print(depart.find("td", {"data-title": "Departs"}).find(class_="fldate").text, end="")
        departure_airport = depart.find("td", {"data-title": "Departs"}).select("br")[0].next_sibling
        print(departure_airport[1:4], end="")
        print(departing_year, end="")
        print()
        # print(depart.find(class_="flprice").text + " + " + fly_back.find(class_="flprice").text)




# print(departs)