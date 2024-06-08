import time

import requests
import selectorlib
import smtplib, ssl
import os


URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/39.0.2171.95 '
        'Safari/537.36'}


def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.mail.yahoo.com"
    port = 465
    username = "anayvalath@yahoo.com"
    password = os.getenv("EMAIL-PASSWORD")
    receiver = "anayvalath@yahoo.com"

    email_message = f"From: {username}\nTo: {receiver}\nSubject: New event\n\n"
    email_message += message

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.set_debuglevel(1)
            server.login(username, password)
            server.sendmail(username, receiver, email_message.encode('utf-8'))
            print("Email was sent.")
    except smtplib.SMTPException as e:
        print("Failed to send email:", e)


def store(extracts):
    with open("data.txt", "a") as file:
        file.write(extracts + "\n")


def read(extracts):
    with open("data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        content = read(extracted)
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(message="Hey, new event was found!")
        time.sleep(2)