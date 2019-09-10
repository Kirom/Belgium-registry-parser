import requests
from bs4 import BeautifulSoup
import csv

# url сайта
url = 'https://search.arch.be/fr/rechercher-des-personnes/resultats/q/zoekwijze/s/start/0?M=0&V=0&O=0&persoon_0_periode_geen=0&akte_type=STBO'
# ответ сервера
result = requests.get(url)
# ответ в текст
source = result.text
# Объект СУПа
soup = BeautifulSoup(source, 'html.parser')
# тот же процесс с url знака лупы
loop_url = 'https://search.arch.be'
loop_url += soup.select('#right > div > div > div > table > tbody > tr:nth-child(1) > td.detailresult > a')[0].get(
    'href')  # ссылкa лупы
loop_url += '?tmpl=component'
loop_result = requests.get(loop_url)
loop_source = loop_result.text
loop_soup = BeautifulSoup(loop_source, 'html.parser')
# Скрейп всей инфы
project = loop_soup.select('#akte > table:nth-child(3) > tbody > tr:nth-child(1) > td > a')[0].get_text()

type_act = loop_soup.select('#akte > table:nth-child(3) > tbody > tr:nth-child(2) > td > a')[0].get_text()

common = loop_soup.select('#akte > table:nth-child(3) > tbody > tr:nth-child(3) > td')[0].get_text()
if common == '':
    common = 'None'
description = loop_soup.select('#akte > table:nth-child(3) > tbody > tr:nth-child(4) > td')[0].get_text()

date_of_the_act = loop_soup.select('#akte > table:nth-child(3) > tbody > tr:nth-child(5) > td')[0].get_text().strip()

name = loop_soup.select('#akte > table:nth-child(6) > tbody > tr > td')[0].get_text()

data = {'project': project,
        'type_act': type_act,
        'common': common,
        'description': description,
        'date_of_the_act': date_of_the_act,
        'name': name}

filename = 'belgium.csv'

# csvwriter = csv.writer(codecs.open("some.csv", "w", "utf-8"))

with open(filename, 'a', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow((data['project'],
                     data['type_act'],
                     data['common'],
                     data['description'],
                     data['date_of_the_act'],
                     data['name']))
# selector builder
for i in range(1, 51):
    selector = '#right > div > div > div > table > tbody > tr:nth-child('
    selector += f'{i}'
    selector += ') > td.detailresult > a'
    loop_url = 'https://search.arch.be'
    loop_url += soup.select('#right > div > div > div > table > tbody > tr:nth-child(1) > td.detailresult > a')[0].get(
        'href')  # ссылкa лупы
    loop_url += '&tmpl=component'
    loop_result = requests.get(loop_url)
    loop_source = loop_result.text
    loop_soup = BeautifulSoup(loop_source, 'html.parser')
