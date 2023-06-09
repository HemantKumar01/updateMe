import requests
from bs4 import BeautifulSoup
import json
import sys
from lxml.html.diff import htmldiff
from os import environ as env
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


headers = {
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0",
}


def sendEmail(From, message, subject):
    print("sending email...")
    load_dotenv("./auth.env")

    # creates SMTP session
    s = smtplib.SMTP("smtp.gmail.com", 587)

    # start TLS for security
    s.starttls()

    email = env["EMAIL"]
    password = env["PASSWORD"]

    # Authentication
    s.login(email, password)

    To = env["TOEMAIL"]

    # sending the mail
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = From
    msg["To"] = To

    text = "there are updates in website at {url}.\n Unable to show diff kindly visit website to see changes yourself;"

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(message, "html")

    msg.attach(part1)
    msg.attach(part2)

    s.sendmail(From, To, msg.as_string())
    # terminating the session
    s.quit()


def showDiff(pathA: str, pathB: str, url: str, fileIndex: int):
    print("starting comparison for:", url, "...")
    doc1 = open(pathA, "r", encoding="utf-8")
    doc2 = open(pathB, "r", encoding="utf-8")
    doc1Content = doc1.read()
    doc2Content = doc2.read()
    doc1.close()
    doc2.close()
    diff = htmldiff(doc1Content, doc2Content)
    soup = BeautifulSoup(diff, "lxml")
    additions = soup.find_all("ins")
    deletions = soup.find_all("del")
    if len(additions) > 0 or len(deletions) > 0:
        message = (
            """
        <html>
        <head><title>Update Me System</title>
        <style>
        ins{
            display:block;
            padding:0;
            margin:3px;
            color:black;
            font-weight:bold;
            font-size:16px;
            background: #16ff1633;
            text-decoration:underline;
        }
        ins::before{
            content:"+ : ";
        }
        del{
            display:block;
            padding:0px;
            margin:3px;
            color:white;
            background:rgba(255,0,0,0.33);
            font-weight:bold;
            font-size:16px;
        }
        del::before{
            content:"- : ";
        }
        </style>
        </head>
        <body>"""
            + (
                (
                    """<h1 style="color:green; text-decoration:underline;">Additions<h1>"""
                    + " ".join(([str(x) for x in additions]))
                )
                if len(additions) > 0
                else """ \n"""
            )
            + (
                (
                    """<h1 style="color:red; text-decoration:underline;">Deletions<h1>"""
                    + " ".join(([str(x) for x in deletions]))
                )
                if len(deletions) > 0
                else """ \n"""
            )
            + """</body>
        </html>"""
        )
        with open(f"./comparison{fileIndex}.html", "w", encoding="utf-8") as localFile:
            print(f"updating local comparison{fileIndex}.html file for next time")
            localFile.write(doc2Content)

        sendEmail("UpdateMe System", message, f"Update in website at {url}:")
    else:
        print("NO UPDATES")

    print("\n")


urlDataFile = open("./urls.json", "r")
urlData = urlDataFile.read()
urlDataFile.close()
urlData = json.loads(urlData)
if len(urlData["urls"]) == 0:
    print("no website set for comparison. first run $: python scrape.py")
    sys.exit()

for i in range(len(urlData["urls"])):
    website = urlData["urls"][i]
    print("getting {}...".format(website["url"]))
    page = requests.get(website["url"], headers=headers)
    formattedPage = BeautifulSoup(page.content, "html.parser")
    htmlNewFile = open(f"./new{i+1}.html", "w", encoding="utf-8")
    htmlNewFile.write(formattedPage.prettify())
    htmlNewFile.close()

    showDiff(f"./comparison{i+1}.html", f"./new{i+1}.html", website["url"], i + 1)
