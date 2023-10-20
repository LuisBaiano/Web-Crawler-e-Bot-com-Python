import tweepy
import os
import gdown
import time
from dotenv import load_dotenv

#Classe onde o Bot é definido e executado
class BOT:
    def __init__(self):
        load_dotenv()
        # Obtenção das chaves e tokens da API do Twitter / X a partir das variáveis de ambiente
        Consumer_Key = os.getenv('CONSUMER_KEY')
        Secret_Key = os.getenv('CONSUMER_KEY_SECRET')
        Secret_Access = os.getenv('ACCESS_SECRET_TOKEN')
        Access_Token = os.getenv('ACCESS_TOKEN')
        Bearer_Token = os.getenv('BEARER_TOKEN')
        
        self.client = tweepy.Client(
            consumer_key=Consumer_Key,
            consumer_secret=Secret_Key,
            access_token=Access_Token,
            access_token_secret=Secret_Access,
            bearer_token=r"{}".format(Bearer_Token),
        )
        #criação das instâncias para a autenticação da API do Twitter / X
        auth = tweepy.OAuth1UserHandler(Consumer_Key, Secret_Key)
        auth.set_access_token(
            Access_Token,
            Secret_Access
        )
        self.api = tweepy.API(auth)

    #Método utilizado criar e postar conteúdo no Twitter / X
    def content(self, data: dict):
        try:
            image_link = data["image"]

            media = None
            #Download da imagem do produto e upload para o Twitter/ X
            if image_link != "":
                path = "tmp/{}.jpg".format(str(round(time.time() * 1000)))
                gdown.download(image_link, path)
                media = self.api.media_upload(filename=path)
                #Remove a imagem que foi salva na pasta "/tmp/" 
                temp_img = path
                os.remove(temp_img)

            # Verifica se o preço anterior é diferente de 0 (preço anterior não cadastrado) e 
            #cria o texto do tweet com informações sobre o produto
            if data['old_price'] != 0:
                post = "{}\n\nPreço Anterior: R$ {}\n\nPreço Atual: R$ {}\n\nLink: {}".format(
                    data["title"], data["old_price"], data["price"], data["link"]
                )
            else:
                post = "{}\n\nPreço Atual: R$ {}\n\nLink: {}".format(
                    data["title"], data["price"], data["link"]
                )

            #Posta o tweet com a imagem
            if media is not None:
                self.client.create_tweet(text=post, media_ids=[media.media_id])
            #Posta o tweet sem imagem
            else:
                self.client.create_tweet(text=post)

            return True
        except Exception as e:
            print(str(e))
            return False