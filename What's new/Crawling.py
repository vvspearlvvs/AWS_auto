import datetime
import feedparser
from googletrans import Translator
import pandas as pd

# crawling
url = "https://aws.amazon.com/about-aws/whats-new/recent/feed/"
trans = Translator()

def classify(term):
    category_list = term.split(",")
    for i in category_list:
        if category_list in "general":
            service_list = category_list.split("general:products")[1]
        elif category_list in "marketing":
            category = "marketing"
    print(category_list)

def crawling_aws(url,trans):

    document_list =[]
    feed = feedparser.parse(url)

    #print(len(feed['entries']))
    #print(feed.entries[0].title)

    for i in range(len(feed.entries)):
        aws_document = {}
        published = str(feed.entries[i].published).replace("+0000","")
        published_date = datetime.datetime.strptime(published,'%a, %d %b %Y %H:%M:%S ')
        now_date=datetime.datetime.now()

        #메일전송일자 기준 일주일치만
        if (now_date-published_date).days <=7:
            kor_title= trans.translate(feed.entries[i].title,src="en",dest="ko")

            if feed.entries[i].tags:
                tags_list = feed.entries[i].tags
                term = tags_list[0]['term']
                #classify(term)
            else:
                term = "null"

            aws_document['date'] = str(published_date)
            #aws_document['index'] = term
            aws_document['ko_title'] = kor_title.text
            aws_document['en_title'] = feed.entries[i].title
            aws_document['link'] = feed.entries[i].link

            document_list.append(aws_document)

    return document_list

def get_crawling_aws():
    document_list = crawling_aws(url,trans)
    return document_list
