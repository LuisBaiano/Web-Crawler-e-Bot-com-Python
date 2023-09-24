import requests
from bs4 import BeautifulSoup

#Sites a serem utilizados:
#1 - Amazon - https://www.amazon.com.br/s?k=eletrodomesticos&ref=nb_sb_ss_ts-doa-p_2_6
#2 - Magazine Luiza - https://www.magazineluiza.com.br/eletrodomesticos/l/ed/

response = requests.get("https://www.amazon.com.br/s?k=eletrodomesticos&ref=nb_sb_ss_ts-doa-p_2_6")

soup = BeautifulSoup(response.text, 'html.parser')

title = soup.find('p', {'data-testid':'price-value'})

print(soup)


