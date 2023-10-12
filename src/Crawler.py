import requests
from bs4 import BeautifulSoup
import time
import schedule
from datetime import datetime
from database import Database
from dotenv import load_dotenv
import os

# Sites a serem utilizados:
# 1 - Kabum - https://www.kabum.com.br/eletrodomesticos?page_number=1&page_size=20&facet_filters=&sort=most_searched
# 2 - Amazon - https://www.amazon.com.br//s?k=eletrodomesticos&qid=1697052859&ref=sr_pg_2&page=1
# 3 - Magazine Luiza - https://www.magazineluiza.com.br/eletrodomesticos/l/ed/?page=2

class Crawler:

    #Função responsável por inicializar o banco de dados
    def __init__(self):
        load_dotenv()
        self.db = Database()

    #  Função responsável por realizar uma solicitação HTTP para a URL especificada, após isso, a resposta da página é analisada com BeautifulSoup.
    # Se ocorrer algum erro, é definido um tempo de espera de 3 segundos para realizar outra solicitação.   
    def request_data(self, url: str, retry: bool = False) -> BeautifulSoup:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except Exception as try_again:
            if not retry:
                time.sleep(3)
                return self.request_data(url, True)
            else:
                raise try_again

    @staticmethod

    #Função responsável por formatar o preço extraido
    def format_price(price: str) -> float:
        return float(price.replace('R$', '').replace('.', '').replace(',', '.'))

    # As Funções 'extract_from_{x}' são responsáveis por extrair os dados dos produtos de cada site e armazená-los no banco de dados,
    #elas extraem as informações: título, imagem, preço e link e insere no banco de dados através do 'self.db.insert(dados)'.
    
    # Função para extrair os dados do site Kabum.
    def extract_from_kabum(self, page: int = 1, retry: bool = False) -> None:
        request = self.request_data(
            os.getenv('KABUM') + f'/eletrodomesticos?page_size=20&facet_filters=&sort=most_searched&page_number={page}'
        )

        products = request.find_all('div', {'class': 'productCard'})
        if products is None:
            if not retry:
                time.sleep(3)
                self.extract_from_kabum(retry=True)
        else:
            for product in products:
                title = product.find('span', {'class': 'nameCard'}).text
                image = product.find('img', {'class': 'imageCard'})
                link = os.getenv('KABUM') + str(product.find('a', {'class': 'productLink'}).attrs['href'])
                second_request = self.request_data(link)
                price = second_request.find("h4", {"class": "finalPrice"}).text
                price = self.format_price(price)

                data_kabum = {
                    'title': title,
                    'image': image,
                    'price': price,
                    'link': link,
                    'date': datetime.now()
                }

                self.db.insert(data_kabum)
                print(data_kabum)

    #Função para extrair os dados do site Amazon.
    def extract_from_amazon(self, page: int = 1, retry: bool = False) -> None:
        request = self.request_data(
            os.getenv('AMAZON') + f'/s?k=eletrodomesticos&qid=1697052859&ref=sr_pg_2&page={page}'
        )
        products = request.find_all("div", {"class": "s-card-container"})

        if products is None:
            if not retry:
                time.sleep(3)
                self.extract_from_amazon(retry=True)
        else:
            for product in products:
                title = product.find("span", {"class": "a-size-base-plus a-color-base a-text-normal"}).text
                link = os.getenv('AMAZON') + product.find("a", {
                    "class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"}
                    ).attrs["href"]
                image = product.find("img", {"class": "s-image"}).attrs["src"]
                
                span_price = product.find("span", {"class": "a-price"})
                price = span_price.find("span", {"class": "a-offscreen"}).text
                price = self.format_price(price)

                data_amazon = {
                    'title': title,
                    'image': image,
                    'price': price,
                    'link': link,
                    'date': datetime.now()
                }
                self.db.insert(data_amazon)
                print(data_amazon)

    #Função para extrair os dados do site Magazine Luiza.
    def extract_from_magalu(self, page: int = 1, retry: bool = False) -> None:
        request = self.request_data(
            os.getenv('MAGALU') + f'/eletrodomesticos/l/ed/?page={page}'
        )
        products = request.find_all('li', {'class': 'sc-APcvf eJDyHN'})
        if products is None:
            if not retry:
                time.sleep(3)
                self.extract_from_magalu(retry=True)
        else: 
            for product in products:
                title = product.find('h2', {'class': 'sc-eWzREE uaEbk'}).text
                image = product.find('img', {'data-testid': 'image'}).attrs['src']
                link = os.getenv('MAGALU') + product.find('a', {'class': 'sc-eBMEME uPWog sc-gppfCo egZavq sc-gppfCo egZavq'}).attrs["href"]
                price = product.find('p', {'class':'sc-kpDqfm eCPtRw sc-hoLEA kXWuGr'}).text
                price = self.format_price(price)

                data_magalu = {
                    'title': title,
                    'image': image,
                    'price': price,
                    'link': link,
                    'date': datetime.now()
                }
                self.db.insert(data_magalu)
                print(data_magalu)

    #Função responsável por chamar os metodos de extração para cada um dos sites e por realizar um laço for que recebe os dados dos produtos
    #que é executada conforme o número de paginas defindas para a extração, indo de 1 ao valor de 'num_pages'.
    def execute(self, num_pages: int = 2):
        for page in range(1, num_pages):
            self.extract_from_kabum(page)
            self.extract_from_amazon(page)
            self.extract_from_magalu(page)

if __name__ == "__main__":
    #Inicialização do Crawler
    crawler = Crawler()
    #Execução da extração de dados dos sites
    crawler.execute(2)

    #Função responsável por fazer a extração periódica dos dados
    def do_request():
        print("\n Execute request. Time: {}".format(str(datetime.now())))
        crawler.execute()

    #Re-executando a função 'do_request' a cada 'x' minutos para evitar sobrecarga de solicitações
    schedule.every(2).minutes.do(do_request)

    #Laço while utilizado para garantir que as requisições agendadas sejam executadas
    while True:
        schedule.run_pending()
