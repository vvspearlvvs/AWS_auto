from pymongo import MongoClient
import pandas as pd

import Emailing
import Crawling

# database
host = "localhost"
port = "27017"

def connect_DB(host,port):
    mongo = MongoClient(host, int(port))
    print("DB Connect Success")
    return mongo

def insert_DB(document_list,collection):
    for document in document_list:
        collection.insert_one(document)
    return "insert success"

def select_DB(collection):
    result = collection.find()
    for i in result:
        print(i)


def main():
    mongo_client = connect_DB(host,port)
    database = mongo_client.get_database('mydb')
    collection =database.get_collection('aws')
    collection.delete_many({})

    document_list = Crawling.get_crawling_aws()
    print(document_list)

    insert_DB(document_list,collection)
    #select_DB(collection)
    '''
    document_list = Crawling.get_crawling_aws()
    df = pd.DataFrame(document_list)
    df['link'] = '<a href='+df['link']+'><div>'+df['en_title'] + '</div></a>'
    Emailing.create_body(df)
    '''

    #document_table = Crawling.get_title_table()
    #Emailing.create_table(document_table)

    #Emailing.create_html(document_list)

if __name__ == '__main__':
    main()
