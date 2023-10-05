import requests
import re
from bs4 import BeautifulSoup

#Sites a serem utilizados:
#1 - Amazon - https://www.amazon.com.br/s?k=eletrodomesticos&ref=nb_sb_ss_ts-doa-p_2_6
#2 - Magazine Luiza - https://www.magazineluiza.com.br/eletrodomesticos/l/ed/
#3 - Kabum - https://www.kabum.com.br/eletrodomesticos 

response = requests.get("https://www.magazineluiza.com.br/eletrodomesticos/l/ed/")

raw_magalu = BeautifulSoup(response.text, 'html.parser')

products = raw_magalu.find_all('li', {'class': 'sc-APcvf eJDyHN'})

for product in products:
    image = product.find('img', {'data-testid': 'image'})
    title = product.find('h2', {'class': 'sc-eWzREE uaEbk'}).text
    raw_price = product.find('p', {'class':'sc-kpDqfm efxPhd sc-eXsaLi dBQBbm'}).text
    link = product.find('a', {'class': 'sc-eBMEME uPWog sc-gppfCo egZavq sc-gppfCo egZavq'})
    
    price = str(raw_price.replace('R$',''))
    format_price = float(price.replace('.','').replace(',','.'))
    
    data_magalu = {
        'image': image.attrs['src'],
        'title': title,
        'price': format_price,
        'link':'https://www.magazineluiza.com.br' + link.attrs['href']
        }
    break

print(data_magalu)