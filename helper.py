from datetime import datetime, timedelta
from time import strptime

def find_year(direction, columns):
    year = [col for col in columns if direction in col.text][0].text
    return year.split()[-1]

def url_formater(day=0):
    """Returns URL string"""
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

def time_creation(time, date, year):
    """Returns date string fir csv file"""
    time = time[:-2] + " " + time[-2:]
    hours_and_mins = datetime.strftime(datetime.strptime(time, "%I:%M %p"), "%H:%M")
    month_and_day = date.replace(",", "").split()
    month = strptime(month_and_day[2],'%b').tm_mon
    flight_time = datetime.now().replace(year=int(year), month=month, day=int(month_and_day[1]),
                                      hour=int(hours_and_mins.split(":")[0]),
                                      minute=int(hours_and_mins.split(":")[1]), second=0)
    return flight_time.strftime("%a %b %d %X GTM %Y")

def form_flight_data(flight_data, flight_year):
    """returns oney way flight data"""
    dep_fl_time = flight_data.find("td", {"data-title": "Departs"}).find(class_="fltime").text[1:-1]
    dep_fl_date = flight_data.find("td", {"data-title": "Departs"}).find(class_="fldate").text

    arr_fl_time = flight_data.find("td", {"data-title": "Arrives"}).find(class_="fltime").text[1:-1]
    arr_fl_date = flight_data.find("td", {"data-title": "Arrives"}).find(class_="fldate").text

    departure_airport = flight_data.find("td", {"data-title": "Departs"}).select("br")[0].next_sibling[1:4]
    arrives_airport = flight_data.find("td", {"data-title": "Arrives"}).select("br")[0].next_sibling[1:4]
    dep_time = time_creation(dep_fl_time, dep_fl_date, flight_year)
    arr_time = time_creation(arr_fl_time, arr_fl_date, flight_year)

    return [departure_airport, arrives_airport, dep_time, arr_time]

def form_round_trip_data(depart, fly_back, departing_year, returning_year):
    """Returns round trip flight data, with all flights"""
    flight_info = []
    dep_flight = form_flight_data(depart, departing_year)
    flight_info.extend(dep_flight)
    ret_flight = form_flight_data(fly_back, returning_year)
    flight_info.extend(ret_flight)
    return flight_info

def get_price_and_tax(price_data):
    """returns flight total price and total tax"""
    elements = price_data.find_all(class_="fly5-bkdown")
    total_price = 0
    total_tax = 0
    for element in elements:
        amount = element.find_all(class_="num")
        total_tax += float(amount[1].text.replace(",", ""))
        total_price += float(amount[2].text.replace(",", ""))
    tax = "{:.2f}".format(total_tax)
    price = "{:.2f}".format(total_price)
    return [price, tax]

def find_lowest_price_id(pacs_ids):
    """check if not soldout too"""
    for pac in pacs_ids:
        select_btn = pac.find(class_="select-flight")
        if select_btn is None:
            continue
        return pac.get('id')
    return  None