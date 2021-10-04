import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(result, to_email):
    from_email = 'phq.9.thesis@gmail.com'

    msg = MIMEMultipart("alternative")
    msg['Subject'] = 'PHQ-9 Result UUID ['+result.uuid+']'
    msg['From'] = from_email
    msg['To'] = to_email

    text = '[Result]' + '\n' + \
        '--Emote--' + '\n' + \
        result.stringEmote + '\n' + \
        '--ClickTime--' + '\n' + \
        result.ClickTime + '\n' + \
        '--Behavior--' + '\n' + \
        result.Behavior + '\n' + \
        '--GroupsTest--' + '\n' + \
        result.GroupsTest + '\n'

    text_message = MIMEText(text, "plain")
    msg.attach(text_message)
    s = smtplib.SMTP("smtp", 25)
    s.ehlo()
    s.sendmail(from_addr=from_email, to_addrs=to_email, msg=msg.as_string())
    s.quit()
