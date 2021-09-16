import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def send_email(uuid, body, to_email):
    from_email = 'phq.9.thesis@gmail.com'

    msg = MIMEMultipart("alternative")
    msg['Subject'] = 'Test mail sender'
    msg['From'] = from_email
    msg['To'] = to_email

    html = """\
        <html>
        <body>
        <img src="cid:image">
        </body>
        </html>
        """
    html_body = MIMEText(html, 'html')

    file_pic = open('/images/' + uuid + '.png', 'rb')
    image = MIMEImage(file_pic.read())
    file_pic.close()

    image.add_header('Content-ID', '<image>')

    msg.attach(html_body)
    msg.attach(image)

    s = smtplib.SMTP("mail", 25)
    s.ehlo()
    s.sendmail(from_addr=from_email, to_addrs=to_email, msg=msg.as_string())
    s.quit()
