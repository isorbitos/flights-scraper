import requests
import logging
from bs4 import BeautifulSoup
from csv import writer

from selenium.webdriver.common.by import By

from helper import find_year, url_formater, form_round_trip_data, get_price_and_tax, find_lowest_price_id
from seleniumwire import webdriver
import time

logging.basicConfig(filename='http_req.log', encoding='utf-8', level=logging.INFO)
with open("http_req.log", "w"):
    pass

#using BeutifulSoup
#this part can only take data from one flights selection page, taxes i saw at this moment for every flight is 6$


with open('flights_data.csv', 'w', encoding='utf8', newline='') as fl:
    the_writer = writer(fl, delimiter=';')
    header = ['outbound_departure_airport', 'outbound_arrival_airport', 'outbound_departure_time', 'outbound_arrival_time',
              'inbound_departure_airport', 'inbound_arrival_airport', 'inbound_departure_time', 'inbound_arrival_time', 'total_price', 'taxes']
    the_writer.writerow(header)
    for days_from_today in [10]:
        URL = url_formater(days_from_today)
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        departs = soup.find(class_='fly5-depart').find_all(class_='fly5-result')
        fly_backs = soup.find(class_="fly5-return").find_all(class_='fly5-result')
        info_table = soup.find(class_="fly5-query").find_all(class_="col-5")

        departing_year = find_year("Departing", info_table)
        returning_year = find_year("Returning", info_table)


        for depart in departs:
            for fly_back in fly_backs:
                flight_info = form_round_trip_data(depart, fly_back, departing_year, returning_year)

                flight_price = float(depart.find(class_="flprice").text) + float(fly_back.find(class_="flprice").text)
                flight_taxes = 12.0
                tax = "{:.2f}".format(flight_taxes)
                price =  "{:.2f}".format(flight_price)
                flight_info.append(price)
                flight_info.append(tax)
                the_writer.writerow(flight_info)



#advanced search with Selenium and BeutifulSoup to get 100% accuracy taxes and price from next page
#for this part need Cromedriver to be installed

with open('flights_data_advanced.csv', 'w', encoding='utf8', newline='') as fl:
    the_writer = writer(fl, delimiter=';')
    header = ['outbound_departure_airport', 'outbound_arrival_airport', 'outbound_departure_time',
              'outbound_arrival_time',
              'inbound_departure_airport', 'inbound_arrival_airport', 'inbound_departure_time', 'inbound_arrival_time',
              'total_price', 'taxes']
    the_writer.writerow(header)
    for days_from_today in [10, 20]:

        URL = url_formater(days_from_today)
        try:
            driver = webdriver.Chrome()
        except:
            the_writer.writerow(['for this part you need download cromedriver.exe, and put it in path'
                                 '(on window Advanced system settings-> Environment Variables -> new ->c:folders path)'])
            break
        driver.scopes = [
            '.*fly540.*',
        ]
        driver.get(URL)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        departs = soup.find(class_='fly5-depart').find_all(class_='fly5-result')
        fly_backs = soup.find(class_="fly5-return").find_all(class_='fly5-result')
        info_table = soup.find(class_="fly5-query").find_all(class_="col-5")

        departing_year = find_year("Departing", info_table)
        returning_year = find_year("Returning", info_table)

        depart_table = 1
        for depart in departs:
            dep_packs_ids = depart.find_all(class_="flpackage")
            dep_pack_id =  find_lowest_price_id(dep_packs_ids)
            if dep_pack_id is None:
                depart_table += 1
                continue
            flyback_table = 1
            for fly_back in fly_backs:
                ret_packs_ids = fly_back.find_all(class_="flpackage")
                ret_pac_id = find_lowest_price_id(ret_packs_ids)
                if dep_pack_id is None:
                    flyback_table += 1
                    continue

                flight_info = form_round_trip_data(depart, fly_back, departing_year, returning_year)

                dep_table_row = driver.find_element(By.XPATH, f'//*[@id="book-form"]/div[1]/div[2]/div[{depart_table}]')
                dep_table_row.click()
                time.sleep(2)

                dep_table_row.find_element(By.XPATH, f'//*[@id="{dep_pack_id}"]/div/div[2]/button').click()
                time.sleep(2)

                return_table_row = driver.find_element(By.XPATH, f'//*[@id="book-form"]/div[2]/div[2]/div[{flyback_table}]')
                return_table_row.click()
                time.sleep(2)

                return_table_row.find_element(By.XPATH, f'//*[@id="{ret_pac_id}"]/div/div[2]/button').click()
                time.sleep(5)

                continue_btn = driver.find_element(By.XPATH, '//*[@id="continue-btn"]')
                driver.execute_script("arguments[0].click();", continue_btn)
                time.sleep(5)

                price_info = BeautifulSoup(driver.find_element(By.ID, "breakdown").get_attribute('innerHTML'), 'html.parser')
                tax_and_price = get_price_and_tax(price_info)

                flight_info.extend(tax_and_price)

                driver.get(URL)
                time.sleep(5)
                the_writer.writerow(flight_info)
                flyback_table+=1
            depart_table+=1

        for request in driver.requests:
            if request.response:
                logging.info(request.url)
time.sleep(3)

