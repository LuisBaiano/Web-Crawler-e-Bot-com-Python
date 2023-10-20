# Projeto de Web Crawler com Bot em Python

Projeto de Atividade Complementar da Disciplina EAD: fundamentos e praticas - ECOMP - UEFS  que tem como objetivo a construção de um Web Crawling. Ele possui scripts para extrair informações dos sites Kabum, Amazon e Magazine Luiza.

## Sumário



### Pré-requisitos

Para a devida construção e execução do projeto, é necessária a instalação dos seguintes recursos:

* Python 3.10+
* pip

### Bibliotecas utilizadas

* beautifulsoup4
* datetime
* dnspython
* gdown
* os
* pymongo
* python-dotenv
* requests
* schedule
* time
* tweepy

  As bibliotecas e suas dependências podem ser instaladas da seguinte maneira:

  ```
  pip install -r requirements.txt
  ```

### Informações para execução do Crawler:

1. Instale os **pré-requisitos**
2. Clone o repositório

   ```
   git clone https://github.com/LuisBaiano/Web-Crawler-e-Bot-com-Python.git
   ```
3. Instale as **bibliotecas** e suas dependências
4. Crie um arquivo ***.env***  igual ao **.env.example** preechido com as chaves de acesso da sua API do **Twitter/X** e com o link de acesso para o seu banco de dados do **MongoDB**
5. Entre na pasta src com **cd *Web-Crawler-e-Bot-com-Python\src***
6. Execute o arquivo ***Crawler.py***
