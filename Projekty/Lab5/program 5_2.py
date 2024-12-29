import requests
from bs4 import BeautifulSoup
import json

url = 'https://boardgamegeek.com/browse/boardgame'      #adres strony z rankingiem gier planszowych
res = requests.get(url)                            #pobranie strony

print(res.status_code)                           #sprawdzenie statusu połączenia

soup = BeautifulSoup(res.text, 'html.parser')       #parsowanie strony

main_div = soup.find('div', class_='legacy')            #znalezienie odpowiedniego diva
#print(main_div)


game_data = main_div.find_all('div', class_='table-responsive')         
#print(film_data)
boardgames_data = {}                        #słownik na dane gier

for game in game_data:                #iteracja po danych gier
    titles = game.find_all('a', class_='primary')       #znalezienie tytułów gier
    ranks = game.find_all('td', class_='collection_rank')       #znalezienie rankingu gier
    ratings = game.find_all('td', class_='collection_bggrating')[::3]       #znalezienie ocen gier co 3 element
    years = game.find_all('span', class_='smallerfont')     #znalezienie roku wydania gier
    description = game.find_all('p', class_='smallefont')       #znalezienie opisu gier
    

    for title, rank, ratings,years,description in zip(titles, ranks, ratings,years,description):        #iteracja po danych gier
        name = title.text.strip()       
        year = years.text.strip()
        rank = rank.text.strip()
        desc= description.text.strip()
        ratings = ratings.text.strip()
        print(rank, name,year, ratings, desc)
        boardgames_data[name] = {    #dodanie danych do słownika
                'rank': rank,
                'name': name,
                'year': year,
                'rating': ratings,
                'description': desc  
            }

with open('boardgames.json', 'w') as file:      #zapisanie danych do pliku json
    json.dump(boardgames_data, file, indent=4)

#Z przycisku