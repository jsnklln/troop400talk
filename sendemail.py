## This program worked for about 2 days then stopped working
## I'm doing something wrong with TLS and I can't figure
## it out.
## This code *is* useful because it's an indepth view
## into how SMTP works.
import ssl
import base64
import getpass
from socket import *

def send(s, data, show=True):
    if isinstance(data, bytes):
        if show:
            print(f"sending: {data.decode('utf-8')}")
        else:
            print(f"sending: REDACTED")
        s.send(data + b"\r\n")
    else:
        if show:
            print(f"sending: {data}")
        else:
            print(f"sending: REDACTED")
        s.send(bytes(f"{data}\r\n", 'utf-8'))

def recv(s):
    data = s.recv(4096)
    data_list = data.split(b'\r\n')
    for index, d_l in enumerate(data_list):
        data_list[index] = d_l.decode('utf-8')

    return '\n'.join(data_list)

def send_email(user, passwd):
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(("smtp.gmail.com", 587))

    # say hello
    send(c, "EHLO LOCALHOST")
    print(recv(c))

    # tell google to start encryption
    send(c, "STARTTLS")
    print(recv(c))

    # start encryption
#    sc = ssl.wrap_socket(c, ssl_version=ssl.PROTOCOL_SSLv23)
    sc = ssl.wrap_socket(c, ssl_version=ssl.PROTOCOL_TLS)

    # tell google we want to login with our username and password
    send(sc, "AUTH LOGIN")
    print(recv(sc))

    # send username
    send(sc, base64.b64encode(user.encode('utf-8')))
    print(recv(sc))

    # send password
    send(sc, base64.b64encode(passwd.encode('utf-8')), show=False)
    print(recv(sc))

    # set the from address
    send(sc, f"MAIL FROM: <{user}>")
    print(recv(sc))

    # set the to address
    send(sc, "RCPT TO: <somebody@somewhere.net>")
    print(recv(sc))

    # tell the mail daemon we're about to start the message
    send(sc, "DATA")
    print(recv(sc))

    # send the message, end with \r\n.\r\n
    send(sc, f"""Subject: blarp

    this message was sent from {gethostname()} by {getpass.getuser()}
    \r\n.""")
    print(recv(sc))

    # bye 
    send(sc, "QUIT")
    print(recv(sc))

def main():
    with open("secrets", "br") as f:
        user = f.readline().rstrip().decode('utf-8')
        passwd = f.readline().rstrip().decode('utf-8')

    send_email(user, passwd)

if __name__ == '__main__':
    main()
