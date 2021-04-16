import feedparser
import datetime

url = "https://aws.amazon.com/about-aws/whats-new/recent/feed/"

feed = feedparser.parse(url)
#print(len(feed['entries']))
#print(feed.entries[1])

for i in range(len(feed.entries)) :
    published = str(feed.entries[i].published).replace("+0000","")
    published_date = datetime.datetime.strptime(published,'%a, %d %b %Y %H:%M:%S ')

    if feed.entries[i].tags:
        tags_list = feed.entries[i].tags
        term = tags_list[0]['term']
    else:
        term = "null"
    print(feed.entries[i].title)
    print(feed.entries[i].link)
    print(str(published_date))
    print(term)
