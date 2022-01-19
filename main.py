import requests
from bs4 import BeautifulSoup
from csv import writer
from helper import find_year, url_formater, form_flight_data

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
            flight_info = []
            dep_flight = form_flight_data(depart, departing_year)
            flight_info.extend(dep_flight)
            ret_flight = form_flight_data(fly_back, returning_year)
            flight_info.extend(ret_flight)
            flight_price = float(depart.find(class_="flprice").text) + float(fly_back.find(class_="flprice").text)
            flight_taxes = 12.0
            tax = "{:.2f}".format(flight_taxes)
            price =  "{:.2f}".format(flight_price)
            flight_info.append(price)
            flight_info.append(tax)
            the_writer.writerow(flight_info)

