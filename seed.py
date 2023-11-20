from config.models import Author , Quote
from mongoengine.errors import NotUniqueError
from config.db import mongoconect
import json
from pathlib import Path

#path = Path('python_web16_hw9' / 'python_web16_hw9' / 'spiders') / 'python_web16_hw9' / 'python_web16_hw9' / 'spiders'/)


author_data = 'python_web16_hw9/python_web16_hw9/spiders/authors.json'
quote_data = 'python_web16_hw9/python_web16_hw9/spiders/quotes.json'

def data_load(data):
    with open(data, encoding='utf-8') as fd:
        data_json = json.load(fd)
    return(data_json)


def qoute(data_q):
    for el in data_load(data_q):
            try:
                author, *_ = Author.objects(fullname=el.get('author'))
                quote = Quote(quote=el.get('quote'), tags=el.get('tags'), author=author)
                quote.save()
            except ValueError:
                print("Автора не існує в таблиці авторів")

def author(data_a):
    for el in data_load(data_a):
            try:
                author = Author(fullname=el.get('fullname'), born_date=el.get('born_date'),
                                born_location=el.get('born_location'), description=el.get('description'))
                author.save()
            except NotUniqueError:
                print(f"Автор вже існує {el.get('fullname')}")

if __name__ == "__main__":
    mongoconect()
    author(author_data)
    qoute(quote_data)
