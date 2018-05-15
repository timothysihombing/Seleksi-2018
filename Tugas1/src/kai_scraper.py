from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

def get_url_info():
    dept = input("Departure : ")
    arr = input("Arrival : ")
    date = input("Date : ")
    type_train = input("Type Train : ")
    if (type_train != "oneway"):
        ret_date = input("Return date : ")
    adult = input("Adult : ")
    infant = input("Infant : ")
    if (type_train != "oneway"):
        url = ("https://m.tiket.com/kereta-api/cari?d=" + dept + "&dt=STATION&a=" + arr + "&at=STATION&date=" + date +"&typetrain=" + type_train + "&ret_date=" + ret_date + "&adult=" + adult + "&infant=" + infant)
    else:
        url = ("https://m.tiket.com/kereta-api/cari?d=" + dept + "&dt=STATION&a=" + arr + "&at=STATION&date=" + date +"&typetrain=" + type_train + "&adult=" + adult + "&infant=" + infant)
    return url

def scrape_small_picture():
    url = "https://m.tiket.com/kereta-api/cari?d=SEMARANG&dt=CITY&a=BD&at=STATION&date=2018-05-23&typetrain=roundtrip&ret_date=2018-05-30&adult=1&infant=0"
    result = []
    page = urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    data_names = ['data-origin_station', 'data-destination_station', 'data-departure_time', 'data-train_class', 'data-price', 'data-duration', 'data-train_name']

    rows = soup.find_all("tr", {'class' : 'main-row '})
    for row in rows:
        row_datas = [row.get(data) for data in data_names]
        result.append(row_datas)
    return result

def make_dict(datas):
    result = dict()
    result['result'] = []
    for data in datas:
        if (data[3] == 'roundtrip'):
            ticket = dict()
            ticket["departure"] = data[0]
            ticket["arrival"] = data[1]
            ticket["date"] = data[2]
            ticket["type_train"] = data[3]
            ticket["ret_date"] = data[4]
            ticket["adult"] = data[5]
            ticket["infant"] = data[6]
        else:
            ticket = dict()
            ticket["departure"] = data[0]
            ticket["arrival"] = data[1]
            ticket["date"] = data[2]
            ticket["type_train"] = data[3]
            ticket["adult"] = data[4]
            ticket["infant"] = data[5]
        result['result'].append(ticket)
    return result

# main
dicts = make_dict(scrape_small_picture())
print(dicts)

with open('data.json', 'w') as outfile:
    json.dump(dicts, outfile)
