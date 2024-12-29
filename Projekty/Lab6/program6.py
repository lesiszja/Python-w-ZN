from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
grimcoven_data = {}     #słownik na dane gier
url = 'https://gamefound.com/pl/projects/awaken-realms/grimcoven'       #adres strony

options = Options()     #opcje przeglądarki
#options.add_argument('--headless')     #opcja headless

service = Service('webdriver/chromedriver.exe')     #ścieżka do chromedrivera

driver = webdriver.Chrome(service=service, options=options)     #uruchomienie przeglądarki
driver.get(url)     #przejście na stronę

# zamknięcie okna z informacją o ciasteczkach
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.gfu-floating-message.gfu-floating-notification-box.gfu-floating-notification-box--fixed._pa-0._ma-0._bgc--transparent._bxsh--none.gfu-floating-notification-box--left > div > div.gfu-media > div > div > div > button')))
button.click()

# przewinięcie strony w dół
driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)

# kliknięcie w przycisk "Nagrody"
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#project-navigation > div > div > nav > div > a:nth-child(2) > div > span')))
button.click()

# przewinięcie strony w dół
for _ in range (2):
    driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

print('-----------------')

# funkcja do ekstrakcji danych gier
def extract_game_data(css_selector):
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))   #znalezienie przycisku z grą
    button.click()

    WebDriverWait(driver, 10).until(    #czekanie na załadowanie danych
        EC.presence_of_element_located((By.CSS_SELECTOR, '#modals > div > div.gfu-modal__body.gfu-modal__body--wide > div.gfu-modal__content > div > div > div.gfu-product.gfu-product--modal > div > div:nth-child(2) > div.gfu-product-set-items._cf > div:nth-child(1) > div > div.gfu-media__body > div.gfu-product-set-item__name.gfu-hd.gfu-hd--h4.gfu-hd--decorative._pl-2 > a'))
    )

    main_div = driver.find_element(By.CSS_SELECTOR, 'div.gfu-product-set-items')    #znalezienie diva z danymi gier
    game_data = main_div.find_elements(By.CSS_SELECTOR, 'a')[1::2]  #znalezienie danych gier co 2 element
    name = driver.find_element(By.CSS_SELECTOR, '#modals > div > div.gfu-modal__body.gfu-modal__body--wide > div.gfu-modal__content > div > div > div.gfu-product.gfu-product--modal > div > div.gfu-product__row > div.gfu-product__info.gfu-1of1.gfu-1of2--m > div > div:nth-child(1) > h1').text.strip()   #znalezienie nazwy gry
    grimcoven_data[name] = []   #dodanie nazwy gry do słownika

    for game in game_data:  #iteracja po danych gier
        #print(game.text.strip())
        game_text = game.text.strip().replace('\n', '').replace('  ', ' ')  
        grimcoven_data[name].append(game_text)  #dodanie danych do słownika

    # zamknięcie okna z grą
    close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#modals > div > div.gfu-modal__body.gfu-modal__body--wide > div._flex._jc-sb > div > a > span.gfu-modal-navigation__icon._fa._fa--times._ml-1._fr')))
    close_button.click()

selectors = [   #selektory do przycisków z grami
    '#reward-box-57661 > div.gfu-card__wrap > div.gfu-card__body > div > div.gfu-reward-card__content.gfu-box__content > h3 > a',
    '#reward-box-54847 > div.gfu-card__wrap > div.gfu-card__body > div > div.gfu-reward-card__content.gfu-box__content > h3 > a',
    '#reward-box-56247 > div.gfu-card__wrap > div.gfu-card__body > div > div.gfu-reward-card__content.gfu-box__content > h3 > a',
    '#reward-box-57660 > div.gfu-card__wrap > div.gfu-card__body > div > div.gfu-reward-card__content.gfu-box__content > h3 > a',
    '#reward-box-56250 > div.gfu-card__wrap > div.gfu-card__body > div > div.gfu-reward-card__content.gfu-box__content > h3 > a'
]

for selector in selectors:  #iteracja po selektorach
    extract_game_data(selector)

#time.sleep(20)

print(grimcoven_data)   #wyświetlenie danych gier
with open('grimcoven.json', 'w') as file:      #zapisanie danych do pliku json
    json.dump(grimcoven_data, file, indent=4)   


driver.close()

#z przycisku