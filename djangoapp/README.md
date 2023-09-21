# Para fazer o deploy:

## 1 - Configurando o .env:

Precisa de uma forma de carregar o .env dentro do servidor quando subir a aplicação.
O pacote [python-dotenv](https://pypi.org/project/python-dotenv/) é responsável por carregar o arquivo .env.

- precisa importar no **settings.py**
- precisa importar no **/wsgi.py**


## 2 - Trazendo uma camada extra de segurança:
Podemos usar o [django-axes](https://django-axes.readthedocs.io/en/latest/2_installation.html) para proteger melhor a área de admin do projeto.