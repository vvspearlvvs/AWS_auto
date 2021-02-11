import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date,datetime, timedelta

# basic information
sender = "gg66477@gmail.com"
receiver = "gg6647@naver.com"
password = "앱 패스워드"

year = str(datetime.today().year)
month = str(datetime.today().month)
day = str(datetime.today().day)


def get_week_no():
    target=datetime.now() #datetime
    firstday = target.replace(day=1)
    if firstday.weekday() == 6:
        origin = firstday
    elif firstday.weekday() < 3:
        origin = firstday - timedelta(days=firstday.weekday() + 1)
    else:
        origin = firstday + timedelta(days=6-firstday.weekday())
    return (target - origin).days // 7 + 1

def create_html(document_list):
    html =''
    html += '<!DOCTYPE html> ' \
            '<html>' \
            '<body>' \
            '<h2 style="font-family:Sans-Serif;text-align:center"><strong>AWS Weekly Whats New &#127752;</strong</h2>' \
            '<hr style="border:0;border-top:solid 1px #e2e2e2;width:90%;margin:20px auto" class="horizontal-line">'
    for content in document_list:
        html+='<div style="margin-top:20px">' \
              '<h5 style="font-family:Sans-Serif;text-align:left;width:90%;margin:20px auto">'+"["+content['date']+"] "
        if 'service' in content['index']:
            for service in content['index']['service']:
                html+="#"+service
        elif 'marketing' in content['index']:
            html+="#marketing"
        else:
            html+="#else"

        html+='<br>'+content['ko_title'] +\
                  '<a href="'+content['link']+'"style="color:#FF9900;text-decoration: none;"> 더보기</a></h5>'\
                  '</div></body></html>'
    send_email(html)
    print("메일body : html형식")

def create_body(dataframe):
    content= dataframe.to_html(escape=False)
    send_email(content)
    return "메일body : dataframe형식"

def send_email(content):
    # 메일콘텐츠 설정
    message = MIMEMultipart('alternative')
    message['Subject'] = "["+month+"월 "+str(get_week_no())+"주차] AWS What's New 소식"
    message['From'] = sender
    message['To'] = receiver

    # Email Body
    body = MIMEText(content, 'html')
    message.attach(body)

    # Send Email
    stmp = smtplib.SMTP_SSL('smtp.gmail.com')
    stmp.login(sender, password)
    stmp.sendmail(sender, receiver, message.as_string())
    stmp.quit()
