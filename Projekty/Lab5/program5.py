import requests
from bs4 import BeautifulSoup
import json

url = 'https://zeriun.cc/seriale'
res = requests.get(url)

print(res.status_code)

soup = BeautifulSoup(res.text, 'html.parser')

main_div = soup.find('ul', id='list')
# print(main_div)

film_data = main_div.find_all('div', class_='info')

films = {}

for film in film_data:
    name = film.find('h2', class_='title').text
    print(name)

    genre = film.find('div', class_='genres').text
    print(genre)

    country = film.find('div', class_='countries').text
    print(country)

    date = film.find('div', class_='date').text
    print(date)

    rate = film.find('div', class_='rate').text
    print(rate)

    films[name] = {
        'genre': genre,
        'country': country,
        'date': date,
        'rate': rate
    }


with open('films.json', 'w') as file:
    json.dump(films, file, indent=4)



