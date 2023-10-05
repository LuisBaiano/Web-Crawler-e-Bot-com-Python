import requests
import re
import time
from bs4 import BeautifulSoup

#Sites a serem utilizados:
#1 - Amazon - https://www.amazon.com.br/s?k=eletrodomesticos&ref=nb_sb_ss_ts-doa-p_2_6
#2 - Magazine Luiza - https://www.magazineluiza.com.br/eletrodomesticos/l/ed/
#3 - Kabum - https://www.kabum.com.br/eletrodomesticos 


class Crawler: 
    def request_data(self, url: str):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    
    def extract_from_kabum(self):
        raw_kabum = self.request_data('https://www.kabum.com.br/eletrodomesticos')
        products = raw_kabum.find_all('div', {'class': 'productCard'})
        
        all_data_kabum = []
        
        for product in products:
            image = product.find('img', {'class': 'imageCard'})
            title = product.find('span', {'class': 'nameCard'})
            raw_price = product.find('span', {'class': 'priceCard'}).text
            link = product.find('a', {'class': 'productLink'})
            
            price = str(raw_price.replace('R$',''))
            format_price = float(price.replace('.','').replace(',','.'))
            
            data_kabum = {
                'image': image.attrs['src'],
                'title': title.text,
                'price': format_price,
                'link': 'https://www.kabum.com.br' + link.attrs['href']
            }
            break
            all_data_kabum.append(data_kabum)
        
        print(data_kabum)

    def extract_from_amazon(self):
        try: raw_amazon = self.request_data('https://www.amazon.com.br/s?k=eletrodomesticos&ref=nb_sb_ss_ts-doa-p_2_6')
        except: 
            time.sleep(2)
            raw_amazon = self.request_data('https://www.amazon.com.br/s?k=eletrodomesticos&ref=nb_sb_ss_ts-doa-p_2_6')
        
        products = raw_amazon.find_all('div', {'class': 'sg-col-4-of-20'})
        
        all_data_amazon = []

        for product in products:
            image = product.find('img', {'class': 's-image'})
            title = product.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'}).text
            raw_price = product.find('span', {'class':'a-offscreen'}).text
            link = product.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
            
            price = str(raw_price.replace('<span class="a-offscreen">','').replace('R$',''))
            format_price = float(price.replace('.','').replace(',','.'))
            
            data_amazon = {
                'image': image.attrs['src'],
                'title': title,
                'price': format_price,
                'link':'https://www.amazon.com.br' + link.attrs['href']
                }
            break
            all_data_amazon.append(data_amazon)
            
        print(data_amazon)

    def extract_from_magalu(self):
        raw_magalu = self.request_data('https://www.magazineluiza.com.br/eletrodomesticos/l/ed/')
        products = raw_magalu.find_all('li', {'class': 'sc-APcvf eJDyHN'})
        all_data_magalu = []

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
            all_data_magalu.append(data_magalu)
        
        print(data_magalu)

if __name__ == '__main__':
    crawler = Crawler()
    crawler.extract_from_kabum()
    crawler.extract_from_amazon()
    crawler.extract_from_magalu()
