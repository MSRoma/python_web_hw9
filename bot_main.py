from bson.objectid import ObjectId
#import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config.db import mongoclient

# ######### підключення до бази MongoDb  ###########

client = mongoclient()
db = client["python_web16"]

# ######### функція пошуку за ім'ям автора ###########
def find_author(fullname):
    authors_res = {}
    quotes_res = []
    authors_result = db.authors.find({"fullname": fullname},{ "_id": 1, "fullname": 1, "born_date": 1, "born_location": 1 })
    for el in authors_result:
        authors_res.update(el)
    quotes_result = db.quotes.find({"author": ObjectId(authors_res['_id'])},{"quote": 1})
    for el in quotes_result:
        quotes_res.append(el['quote'])
    authors_res.update({'quote': quotes_res})
    return print_f(authors_res)

# ######### функція пошуку за тегом ###########
def find_tag(tags):
    res = {}
    for i in tags:
        quotes_res = {}
        author_res = {} 
        quotes_result = db.quotes.find({"tags": i},{"author": 1,"quote": 1})
        for el in quotes_result:
            quotes_res.update(el)
            authors_result = db.authors.find({"_id": ObjectId(quotes_res['author'])},{"fullname": 1, "born_date": 1, "born_location": 1 })    
            for h in authors_result:
                author_res.update(h)
                author_res.update({'quote': quotes_res['quote']})
            res.update({i: author_res})   
    return res

# ######### функція друку результата ###########
def print_f(result):
        print("============================================")
        print(f"Author: {result['fullname']}")
        print(f"Born data: {result['born_date']}")
        print(f"Born location: {result['born_location']}")
        print(f"Quotes: {result['quote']}")
        print("============================================")

if __name__ == '__main__':
    while True:
        print("Введіть 'name:і'мя автора' для пошуку інформації про  автора")
        print("Введіть 'tag:тег,тег,тег' для пошуку фраз від автора ")
        print("Введіть 'exit' для виходу")
        data = input(">>> ")
        split_data = data.split(":")
        try:
            if split_data[0] == 'exit':
                break
            elif split_data[0] == "tag":
                    s = split_data[1].split(",")
                    f = find_tag(s)
                    for i in f:
                        print_f(f[i])     
            elif split_data[0] == "name":
                    s = split_data[1]
                    find_author(s)
            else:
                print("Перевірте правильність вводу!")
        except  IndexError:
             print("Hе вірно введена команда")
        except  KeyError:
             print("Hе вірно введена команда")
        except  NameError:
             print("Hе вірно введена команда")


