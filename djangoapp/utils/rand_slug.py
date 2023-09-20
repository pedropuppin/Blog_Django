import string
from random import SystemRandom
from django.utils.text import slugify

# cria uma string de 5 letras e números random
def random_letters(k=5):
    return ''.join(SystemRandom().choices(
        string.ascii_letters + string.digits,
        k=k
    ))

# usa a função do django que transforma strings em slug
def slugify_new(text, k=5):
    return slugify(text) + random_letters(k)

# print(slugify_new('dafhkjsa'))