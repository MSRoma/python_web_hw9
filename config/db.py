import configparser
import pathlib

from mongoengine import connect
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# uri = "mongodb+srv://tesmail:<password>@cluster0.zahkpmq.mongodb.net/?retryWrites=true&w=majority"

file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')  # ../config.ini
config = configparser.ConfigParser()
config.read(file_config)

user = config.get('DB', 'USER')
password = config.get('DB', 'PASS')
db_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')


#URI = f"mongodb+srv://{user}:{password}@{db_name}.{domain}"
URI = f"mongodb+srv://{user}:{password}@{domain}/{db_name}?retryWrites=true&w=majority"

# ### for mongoengine MongoClient
def mongoclient():
    client = MongoClient(URI, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return client
#print(f"""mongodb+srv://{user}:{password}@{domain}/{db_name}?retryWrites=true&w=majority""")

# ### for mongoengine connect
def mongoconect():
    connect(host=f"""mongodb+srv://{user}:{password}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)

if __name__ == "__main__":
    mongoclient()
    mongoconect()