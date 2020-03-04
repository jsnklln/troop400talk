## This code, which was stolen from the Internet
## works.  It uses the python smtp lib which handles
## TLS correctly.
import smtplib, ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "me@minecraft.net"
receiver_email = "somebody@turing.org"
message = """\
Subject: Hi there

This message is sent from Python."""

with open("secrets", "br") as f:
    user = f.readline().rstrip().decode('utf-8')
    passwd = f.readline().rstrip().decode('utf-8')

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.set_debuglevel(1)
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.login(user, passwd)
    server.sendmail(sender_email, receiver_email, message)

