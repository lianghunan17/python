# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import re
import lxml.html
import requests
from time import sleep
import smtplib
from io import StringIO
from email.mime.text import MIMEText
from email import message


# get pray time
def do_pray_time():

    islamic_finder = urllib.request.urlopen("https://www.islamicfinder.org/")

    #ここでwebサイトのhtmlを読み込む
    islamic_soup = BeautifulSoup(islamic_finder, 'html.parser')

    pray_name = [u"FAJR", u"SUNRISE", u"DHUHR",
                 u"ASR", u"MAGHRIB", u"ISHA", u"QIYAM"]

    #読み込んだhtmlのh1属性の文字列（サイトの見出しに該当）を取得
    pray_header = "//////Today Pray Time//////" + islamic_soup.h1.string + "\n"

    pray_time = pray_header

    #span要素のclass属性が"todayPrayerTime"の全てを取得
    for i, span_element in enumerate(islamic_soup.findAll("span", class_="todayPrayerTime")):

        if(span_element != None):
            #取得したspan要素の文字列（礼拝時間）を取得  
            pray_time = pray_time + \
                pray_name[i] + "   " + span_element.text + "\n"

    pray_time = pray_time + "\n\n\n"

    return pray_time


# get Iran international news site
def do_iran_news():

    res = urllib.request.urlopen("http://parstoday.com/ja")

    #ニュースサイトのhtmlを取得
    iran_international_soup = BeautifulSoup(res, 'html.parser')

    iran_news_header = '*** Iran international new site ***' + \
        "\n" + "News ParsToday" + "\n\n"

    iran_news = iran_news_header

    #li要素のclass属性で値が"item item-separator inline-30"の箇所を参照、その全てを取得
    for i, li_element in enumerate(iran_international_soup.findAll("li", class_="item item-separator inline-30")):

        #"item item-separator inline-30"の中のdiv要素及びa属性を参照
        div = li_element.find("div")
        a = li_element.find("a")
        if(div != None):

            #「div.text」で、ニュースランキングのタイトルを、「a.get("href")」で各ニュースへのリンクを取得
            iran_news = iran_news + \
                str(i+1) + "位" + " " + div.text + "\n" + a.get("href") + "\n\n"

    iran_news = iran_news + "\n\n\n"

    return iran_news


# get rokusaisha blog
def do_rokusaisha():

    res2 = urllib.request.urlopen("http://www.rokusaisha.com/index.php")

    #ブログのhtmlを取得
    rokusaisha_soup = BeautifulSoup(res2, 'html.parser')

    rokusaisha_header = "********" + rokusaisha_soup.title.string + \
        "********" + "\n" + "最新ブログ情報" + "\n\n"
    
    rokusaisha = rokusaisha_header

    #td要素のclass属性で値が"ブログタイトル"の箇所を参照、その全てを取得
    for i, td_element in enumerate(rokusaisha_soup.findAll("td", class_="ブログタイトル")):

        if(td_element != None):

            #td要素のテキスト（新着ブログのタイトル）を取得
            rokusaisha = rokusaisha + td_element.text + \
                "\n" + "http://www.rokusaisha.com/blog.php" + "\n\n"

    return rokusaisha


#send mail
def do_mail(information1, information2, information3):

    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    from_email = 'ABCD@gmail.com'  # 送信元のアドレス
    to_email = '1234@gmail.com'  # 送信先のアドレス
    username = 'ABCD@gmail.com'  # Gmailのアドレス
    password = 'abcd'  # Gmailのパスワード
    

    # メールの内容を作成
    all_information = information1 + information2 + information3

    msg = message.EmailMessage()
    msg.set_content(all_information)  # メールの本文
    msg['Subject'] = 'Today information'''  # 件名
    msg['From'] = from_email  # メール送信元
    msg['To'] = to_email  # メール送信先

    print("Running")

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.send_message(msg)
    server.quit()

    print('Sending mail is completed')

    
# main part
if __name__ == '__main__':
    do_mail(do_pray_time(), do_iran_news(), do_rokusaisha())
