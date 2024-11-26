import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

recipients = ["1599zzang@naver.com"]

message = MIMEMultipart();
message['Subject'] = '메일 전송 테스트'
message['From'] = "zx6849@naver.com"
message['To'] = ",".join(recipients)

content = """
    <html>
    <body>
        <h2>{title}</h2>
        <p>hello world</p>
    </body>
    </html>
""".format(
title = '나은이 보고싶다'
)

mimetext = MIMEText(content,'html')
message.attach(mimetext)

email_id = 'zx6849@naver.com'
email_pw = ''

server = smtplib.SMTP('smtp.naver.com',587)
server.ehlo()
server.starttls()
server.login(email_id,email_pw)
server.sendmail(message['From'],recipients,message.as_string())
server.quit()