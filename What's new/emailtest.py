import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# basic information
sender = "발송메일주소@gmail.com"
receiver = "수신메일주소@naver.com"
password = "구글앱비밀번호"

# 메일콘텐츠 설정
message = MIMEMultipart('alternative')
message['Subject'] = "메일전송 테스트"
message['From'] = sender
message['To'] = receiver

# Email Body
html = '<h3>hello Email!</h3>'
body = MIMEText(html, 'html')
message.attach(body)

# Send Email
stmp = smtplib.SMTP_SSL('smtp.gmail.com')
stmp.login(sender, password)
stmp.sendmail(sender, receiver, message.as_string())
stmp.quit()