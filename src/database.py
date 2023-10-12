from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

class Database:
	#Função responsável por carrega as variáveis de ambiente a partir de um arquivo .env
    def __init__(self):
        load_dotenv()
        self.offers = self.connect()

	#Função responsável por realizar a conexão com o banco de dados MongoDB usando a URI no arquivo .env
    def connect(self):
        client = MongoClient(os.getenv('DB_URI'))
        db = client['Web-Crawler']
        return db.offers

	#Função responsável por realizar uma consulta na coleção 'offers' para encontrar o documento mais recente com o mesmo título
    def insert(self, data: dict):
        query = {'title': data['title']}
        result = self.offers.find_one(query, sort=[('date', -1)])

		# Condicional If que verifica se não existe um documento com o mesmo título ou se o preço é diferente, após isso, os dados são inseridos na coleção 'offers'.
        if (result is None) or (result['price'] > data['price'] or result['price'] < data['price']):
            return self.offers.insert_one(data)

if __name__ == "__main__":
    db = Database()
    data = {'title': 'Purificador de água Consul, Refrigerado, com Proteção Antibactérias, Cinza, Bivolt - CPB34AFVNA', 'image': 'https://images.kabum.com.br/produtos/fotos/163461/purificador-de-agua-consul-refrigerado-com-protecao-antibacterias-cinza-bivolt-cpb34afvna_1626273185_m.jpg', 'price': 589.9, 'link': 'https://www.kabum.com.br/produto/163461/purificador-de-agua-consul-refrigerado-com-protecao-antibacterias-cinza-bivolt-cpb34afvna'}
    # Insere os dados no banco de dados
    db.insert(data)
