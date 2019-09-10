import requests
from bs4 import BeautifulSoup
import csv

# url сайта
url = 'https://search.arch.be/fr/rechercher-des-personnes/resultats/start/0'
# ответ сервера
result = requests.get(url)
# ответ в текст
source = result.text
# Объект СУПа
soup = BeautifulSoup(source, 'html.parser')
# тот же процесс с url знака лупы
loop_url = 'https://search.arch.be'
loop_url += soup.find('div', class_='borderBL').find('td', class_='detailresult').find('a', class_='modal').get(
    'href')  # ссылкa лупы
loop_url += '?tmpl=component'
loop_result = requests.get(loop_url)
loop_source = loop_result.text
loop_soup = BeautifulSoup(loop_source, 'html.parser')
# Скрейп всей инфы
project = loop_soup.find('table', class_='akte detailtable').find('td').get_text()

type_act = loop_soup.find('table', class_='akte detailtable').find('td').find_next('td').get_text()

common = loop_soup.find('table', class_='akte detailtable').find('td').find_next('td').find_next('td').get_text()

description = loop_soup.find('table', class_='akte detailtable').find('td').find_next('td').find_next('td').find_next(
    'td').get_text()

date_of_the_act = loop_soup.find('table', class_='akte detailtable').find('td').find_next('td').find_next(
    'td').find_next('td').find_next('td').get_text().strip()

data = {'project': project,
        'type_act': type_act,
        'common': common,
        'description': description,
        'date_of_the_act': date_of_the_act}

filename = 'belgium.csv'

# csvwriter = csv.writer(codecs.open("some.csv", "w", "utf-8"))

with open(filename, 'a', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow((data['project'],
                     data['type_act'],
                     data['common'],
                     data['description'],
                     data['date_of_the_act']))
