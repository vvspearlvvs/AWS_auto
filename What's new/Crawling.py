import datetime
import feedparser
from googletrans import Translator
import pandas as pd

# crawling
url = "https://aws.amazon.com/about-aws/whats-new/recent/feed/"
trans = Translator()

def classify(term):
    index_documnet ={}
    service_list =[]
    marketing_list=[]
    try:
        category_list = term.split(",")
        for category in category_list:
            if "general" in category:
                service_list.append(category.split("general:products/")[1])
                index_documnet['service'] = service_list
            elif "marketing" in category:
                marketing_list.append(category.split("marketing:marchitecture/")[1])
                index_documnet['marketing'] = marketing_list
            else:
                index_documnet['else']=category
    except:
        index_documnet = {}
    return index_documnet

def crawling_aws(url,trans):

    document_list =[]
    feed = feedparser.parse(url)

    #print(len(feed['entries']))
    #print(feed.entries[0].title)

    for i in range(len(feed.entries)):
        aws_document = {}
        published = str(feed.entries[i].published).replace("+0000","") #str
        published_date = datetime.datetime.strptime(published,'%a, %d %b %Y %H:%M:%S ') #datetime
        now_date=datetime.datetime.now()
        diffday = (now_date-published_date).days #메일전송일자 기준 일주일치만

        if diffday <=7:
            kor_title= trans.translate(feed.entries[i].title,src="en",dest="ko")

            if feed.entries[i].tags:
                tags_list = feed.entries[i].tags
                term = tags_list[0]['term']

            else:
                term = "null"

            sub_index = classify(term)

            aws_document['date'] = published_date.strftime("%Y.%m.%d")
            aws_document['index'] = sub_index
            aws_document['ko_title'] = kor_title.text
            aws_document['en_title'] = feed.entries[i].title
            aws_document['link'] = feed.entries[i].link

            document_list.append(aws_document)

    return document_list

def get_crawling_aws():
    document_list = crawling_aws(url,trans)
    return document_list
