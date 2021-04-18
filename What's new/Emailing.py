import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pretty_html_table import build_table

# basic information
sender = "gg66477@gmail.com"
receiver = "gg6647@naver.com"
password = "kzruxledhcemeueu"


def create_body(data):
    output=build_table(data,'orange_dark')
    send_email(output)
    return "메일전송 성공"

def send_email(content):

    # 메일콘텐츠 설정
    message = MIMEMultipart('alternative')
    message['Subject'] = "메일전송 테스트"
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
