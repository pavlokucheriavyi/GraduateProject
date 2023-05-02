import requests
import json
import lxml
from bs4 import BeautifulSoup as bs

l = requests.get(
    'https://raw.githubusercontent.com/Adushar/UkraineCitiesAndVillages/main/CitiesAndVillages%20-%2014%20March.json')
x = json.loads(l.text)
result_list = []
for i in x:
    my_dict = dict()
    my_dict['region'] = i['region']
    my_dict['object_name'] = i['object_name']
    my_dict['object_category'] = i['object_category']
    result_list.append(my_dict)

cities_list = [
    'Київ КИЇВСЬКА ОБЛАСТЬ',
    "Черкаси ЧЕРКАСЬКА ОБЛАСТЬ",
    "Ужгород ЗАКАРПАТЬСКА ОБЛАСТЬ",
    "Львів ЛЬВІВСЬКА ОБЛАСТЬ",
    "Рівне РІВНЕНЬСКА ОБЛАСТЬ",
    "Луцьк ВОЛИНСЬКА ОБЛАСТЬ",
    "Тернопіль ТЕРНОПІЛЬСКА ОБЛАСТЬ",
    "Хмельницький ХМЕЛЬНИЦЬКА ОБЛАСТЬ",
    "Житомир ЖИТОМИРСЬКА ОБЛАСТЬ",
    "Київ КИЇВСЬКА ОБЛАСТЬ",
    "Кропивницький КРОПИВНИЦЬКА ОБЛАСТЬ",
    "Полтава ПОЛТАВСЬКА ОБЛАСТЬ",
    "Дніпро ДНІПРОПЕТРОВСЬКА ОБЛАСТЬ",
    "Чернігів ЧЕРНІГІВСЬКА ОБЛАСТЬ",
    "Суми СУМСЬКА ОБЛАСТЬ",
    "Харків ХАРКІВСЬКА ОБЛАСТЬ",
    "Одеса ОДЕСЬКА ОБЛАСТЬ",
    "Херсон ХЕРСОНСЬКА ОБЛАСТЬ",
    "Миколаїв МИКОЛАЇВСЬКА ОБЛАСТЬ",
    "Запоріжжя ЗАПОРІЖСЬКА ОБЛАСТЬ"
]

final_list = []

for i in result_list:
    if i['region'] == 'АВТОНОМНА РЕСПУБЛІКА КРИМ' or i['region'] == 'М.СЕВАСТОПОЛЬ':
        continue
    x = i['object_category'] + ' ' + i['object_name'].capitalize() + ' ' + i['region']
    if i['object_category'] == 'Місто' or i['object_category'] == 'СМТ':
        final_list.append(x)

for i in cities_list:
    final_list.append('Місто ' + i)

final_list.reverse()
export_json = json.dumps(final_list, ensure_ascii=False)


def get_vidd(city):
    url = 'https://novaposhta.ua/office/list/city/' + city
    r = requests.get(url)
    soup = bs(r.text, 'lxml')
    address_list = []

    all_address = soup.select('a.address')

    for item in all_address:
        address_list.append(item.select_one('span').get_text())

    all_vidd = soup.select('a.office_link.office_li')
    vidd_list = []
    vidd_list_2 = []

    for item in all_vidd:
        vidd_list.append(item.select_one('span').get_text())

    for item in vidd_list:
        app_str = ''
        xym = item.split(' ')
        for sym in xym:
            if sym != '':
                app_str = app_str + sym + ' '
        vidd_list_2.append(app_str.strip())

    export_list = []

    num = 0

    for item in vidd_list_2:
        full_add = item + '   ' + address_list[num] + '$'
        num += 1
        export_list.append(full_add)

    return export_list
