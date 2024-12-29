import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.bip.pw.edu.pl/Sklad-osobowy/Podstawowe-jednostki-organizacyjne/Wydzial-Fizyki/Pracownicy-wydzialu'
res = requests.get(url)

print(res.status_code)
#print(res.headers)
#print(res.text)

soup = BeautifulSoup(res.text, 'html.parser')

main_div = soup.find('div', class_ = 'class-folder')
#print(main_div)

# for name in main_div.find_all('h2'):
#     print(name.text.strip().replace('\n', ''))
#     print('--------')
employee_contact_data = {}
employee_data = main_div.find_all('div', class_ = 'class-pracownik')

for employee in employee_data:
    name = employee.find('a').text.strip().replace('\n', '').replace('  ', ' ') 
    
    phone = employee.find('b', text = 'tel. miejski:')
    if phone is not None:
        phone = phone.next_sibling.strip()
                              
    email = employee.find('b', text = 'e-mail:')
    if email is not None:
        email = email.find_next_siblings(string=True)
        email = '.'.join(email[:-1]).strip()
    

    employee_contact_data[name] = {
        'phone': phone,
        'email': email
    }
    
    print(employee_contact_data)

with open('contacts.json', 'w') as file:
    json.dump(employee_contact_data, file, indent=4)