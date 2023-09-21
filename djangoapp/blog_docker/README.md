# Function Based Views vs. Class Based Views 

- **Function Based View** -> São funçoes
- **Class Based Views** -> São classes (OOP)

## Quando usar:

Basicamente usamos a **Function Based View** quando temos views mais simples, com pouca lógica e sem muitos códigos repetidos. E usamos a **Class Based Views** quando temos vies mais complexas que podem se beneficiar dos conceitos de OOP.

Tem vários tipos de **Class Based Views** que já vem prontas no Djando que podem ser utilizadas na sua classe. Ler mais [aqui](https://docs.djangoproject.com/pt-br/4.2/ref/class-based-views/).

## Como usar:

- Criar a classe
- Alterar a url.py para importar a classe
` path('', PostListView.as_view(), name = 'index'), `