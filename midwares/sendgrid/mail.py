import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.message import Message

import email.header
import email.utils

def send_via_smpt():
    from_addr = "alex.chenhui@gmail.com"
    to_addr = "chenhui_bupt@126.com"
    password = SENDGRID_API_KEY ="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"
    smtp_server = "smtp.sendgrid.net"
    username = "apikey"
    subject = "Sending with SendGrid is Fun"

    msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    from_addr   = "<"+from_addr+">"
    from_name = "Hui Chen"
    From        = email.header.Header(from_name,"utf-8",80,"From","\t")
    From.append(from_addr,"ascii")
    msg["From"]     = From

    server = smtplib.SMTP(smtp_server, 587)
    server.set_debuglevel(1)
    server.login(username, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

send_via_smpt()
