import feedparser
import datetime
from pymongo import MongoClient

host = "localhost"
port = "27017"

url = "https://aws.amazon.com/about-aws/whats-new/recent/feed/"

def connect_DB(host,port):
    mongo = MongoClient(host, int(port))
    print("DB Connect Success")

    return mongo

def crawling_rss(url,collection):

    document_list =[]
    feed = feedparser.parse(url)

    #print(len(feed['entries']))
    #print(feed.entries[0])

    for i in range(len(feed.entries)) :
        aws_document = {}
        published = str(feed.entries[i].published).replace("+0000","")
        published_date = datetime.datetime.strptime(published,'%a, %d %b %Y %H:%M:%S ')

        if feed.entries[i].tags:
            tags_list = feed.entries[i].tags
            term = tags_list[0]['term']
        else:
            term = "null"

        aws_document['date'] = str(published_date)
        aws_document['index'] = term
        aws_document['title'] = feed.entries[i].title
        aws_document['link'] = feed.entries[i].link

        document_list.append(aws_document)

    return document_list

def main():
    mongo_client = connect_DB(host,port)
    database = mongo_client.get_database('mydb')
    collection =database.get_collection('aws')
    '''
    collection.drop()
    print("before : select")
    result = collection.find()
    for i in result:
        print(i)
    '''

    document_list = crawling_rss(url,collection)
    for document in document_list:
        collection.insert_one(document)

    print("after : select")
    result = collection.find()
    for i in result:
        print(i)

if __name__ == '__main__':
    main()
