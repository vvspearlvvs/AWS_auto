import feedparser
import time
import datetime
import sys
import gspread
import boto3
from oauth2client.service_account import ServiceAccountCredentials

# Google Spreadsheets API
scope = ['https://spreadsheets.google.com/feeds']
# Google API Service Account JSON
json_file_name = 'skillful-camp-274901-c41cf52b57ab.json'
# Google Credential
auth = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
# service = build('sheets','v4',credentials=auth)
gc = gspread.authorize(auth)

# Google Sheet URL and ID
#spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1Ip2l2xorVG9gBj-OqKMrJ19hYC5nEbrvJtHdbc-qd7A/edit#gid=0'
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1My1cGdwfzRaavftxOOkCLGYDyfFdVOSPzURHeqJ_oyg/edit#gid=0' #test
samplesheet_id = '812426504'
# AWS Translate
client = boto3.client('translate')
# AWS What's New List URL
url = "https://aws.amazon.com/about-aws/whats-new/recent/feed/"
date = datetime.datetime.today().strftime("%Y%m")

# strftime ()은 시간을 문자열로 변환
# strptime은 날짜 문자열을 날짜 / 시간 객체로 변환

while True:
    #last_modified 값 파일에서 불러오기
    try :
        file = open("modified.txt",'r')
        last_modified = file.readline()
        print("1.일자" + last_modified)
        last_modified_date = datetime.datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z ')
        file.close()

    except FileNotFoundError as e:
        print("modifed 파일이 없습니다. 현재 날짜 기준으로 크롤링 합니다.",format(e))
        last_modified_date = datetime.datetime.today()

    except ValueError as e:
        print("modifed 값이 정확하지 않습니다. 현재 날짜 기준으로 피드를 조회합니다.")
        last_modified_date = datetime.datetime.now() - datetime.timedelta(days=3)
        print(last_modified_date)

    #last_modified 값으로 요청
    feed = feedparser.parse(url, modified=last_modified)

    # 변경 사항 없으면 304
    if feed.get('status') == 304:
        print ("새로운 피드가 존재하지 않습니다.")
        sys.exit()

    else:
        doc = gc.open_by_url(spreadsheet_url)
        date = datetime.datetime.today().strftime("%m")
        month = (date + '월')
        try :
            title_data = doc.worksheet(month).col_values(3)
            cell_num = len(title_data) + 1
        except :
            doc.duplicate_sheet(samplesheet_id,0,None,month)
            cell_num = 5

        # 비교위해 news published 포맷 변경
        for i in range(len(feed.entries)) :
            published = str(feed.entries[i].published).replace("+0000","")
            published_date = datetime.datetime.strptime(published,'%a, %d %b %Y %H:%M:%S ')
            # published와 last_modified 비교하여 이전 마지막 수정일 보다 나중에 published된 news 식별
            if published_date > last_modified_date :
                print ("New Feed !!--> ", feed.entries[i].title)
                # aws translate response
                title = client.translate_text(
                    Text=feed.entries[i].title,
                    SourceLanguageCode='en',
                    TargetLanguageCode='ko'
                )
                # print (title['TranslatedText'])
                # Google Sheet Update cell
                doc.worksheet(month).update_cell(cell_num,5,'=HYPERLINK("{}", "{}")'.format(feed.entries[i].link,title['TranslatedText']))
                doc.worksheet(month).update_cell(cell_num,6,str(published_date))
                cell_num = cell_num + 1
            else :
                pass

        #현재 last_modified 값 txt 파일 쓰기
        with open('modified.txt', 'w') as m:
            last_modified = feed.get('modified', '')
            m.write(last_modified + "\n")
            print("3.업데이트 된 modified 값 " + last_modified)
        m.close()
