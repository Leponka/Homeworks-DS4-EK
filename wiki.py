import pandas as pd
import requests

url = 'https://ru.wikipedia.org/wiki/Список_стран_по_населению'
response = requests.get(url)
import bs4
from bs4 import BeautifulSoup
obj = BeautifulSoup(response.content, features="lxml")

table = obj.body.find('table', {'class': "standard sortable"})
position = []
link = []
link_flag = []
country = []
population = []
percentage = []

string = table.tbody.find_all('tr')

string_range = range(2, len(string))
for st in string_range:
        position.append(string[st].find_all("td")[0].text)
       # link_flag.append(string[st].find_all("td")[1].href)
        link.append(string[st].find_all("td")[1].span.a.get('href'))
        country.append(string[st].find_all("td")[1].span.text)
        population.append(string[st].find_all("td")[2].text)
        percentage.append(string[st].find_all("td")[4].text)

country_pop_info = pd.DataFrame(
    {'position': position, 'country': country, 'population': population, 'link': link ,
     'percentage of total': percentage   }) #, 'link_flag': link_flag})

country_pop_info.link = 'https://ru.wikipedia.org//'+country_pop_info.link
count_of_country = len(country_pop_info)

