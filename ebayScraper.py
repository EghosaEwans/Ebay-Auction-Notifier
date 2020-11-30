import requests
from bs4 import BeautifulSoup
import smtplib


url = input("Enter the URL of the product you would like to be notifed of:\n ")
oneDayLeft = bool(input(
    "Would you like to be notified a day before the end of the auction:\n"))
oneHourLeft = bool(input(
    "Would you like to be notified an hour before the end of the auction:\n"))
halfHourLeft = bool(input(
    "Would you like to be notified half an hour before the end of the auction:\n"))
tenMinLeft = bool(input(
    "Would you like to be notified ten minutes before the end of the auction:\n"))
lastMinLeft = bool(input(
    "Would you like to be notified a minute before the end of the auction:\n"))
destinationEmail = input(
    "Enter the email address you would like to get notified at:\n")


def checkPrice():

    global title, price, timeLeft, oneDayLeft, oneHourLeft, halfHourLeft, tenMinLeft, lastMinLeft

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}

    page = requests.get(url, headers=headers, verify=True)

    pageData = BeautifulSoup(page.content, 'html5lib')

    title = (pageData.find(id='itemTitle').get_text()).strip()[16:]

    price = (pageData.find(id='prcIsum_bidPrice').get_text()).strip()

    timeLeft = (pageData.find(id='vi-cdown_timeLeft').get_text()).strip()

    if (oneDayLeft == True and timeLeft == "1 day 0 hours"):
        sendEmail("One Day Left!")
        oneDayLeft = False
    elif (oneHourLeft == True and "1h 0m" in timeLeft):
        sendEmail("One Hour Left!")
        oneHourLeft = False
    elif (halfHourLeft == True and timeLeft[:2] == "30m"):
        sendEmail("30 Minutes Left!")
        halfHourLeft = False
    elif (tenMinLeft == True and "0h 30m" in timeLeft):
        sendEmail("10 Minutes Left!")
        tenMinLeft = False
    elif (lastMinLeft == True and "0h 1m" in timeLeft):
        sendEmail("One Minute Left!")
        lastMinLeft = False


def sendEmail(timeAlert):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('', '')
    subject = timeAlert
    content = "Item: " + str(title) + "\n Current Bid: " + str(price) + \
        "\n Auction End in: " + str(timeLeft) + "/n Link: " + url

    message = f"Subject: {subject}\n\n{content}"

    server.sendmail('eevlachavas@gmail.com', destinationEmail, message)
    server.quit()


checkPrice()
