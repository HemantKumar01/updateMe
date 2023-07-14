import requests
from bs4 import BeautifulSoup
import json
import sys

headers = {
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0",
}
initialWebpage = ""  # tocompare
title = ""
urlData = {
    "url": "",
    "title": "",
}

urlData["url"] = input("ENTER URL:")
page = requests.get(urlData["url"], headers=headers)

if page.status_code == 200:
    print("website scraped successfully...")
else:
    print("website not found!")
    sys.exit()

initialWebpage = BeautifulSoup(page.content, "html.parser")
title = initialWebpage.find("title").text
urlData["title"] = title

urlDataFile = open("./urls.json", "r")
urlDataFileData = json.loads(urlDataFile.read())
if urlData in urlDataFileData["urls"]:
    print("website already on watch")
    sys.exit()
urlDataFileData["urls"].append(urlData)
urlDataJSON = json.dumps(urlDataFileData)


with open(
    f"./reference_files/comparison{len(urlDataFileData['urls'])}.html",
    "w",
    encoding="utf-8",
) as htmlFile:
    htmlFile.write(initialWebpage.prettify())

urlDataFile = open("./urls.json", "w")
urlDataFile.write(urlDataJSON)
urlDataFile.close()


print(
    f""""{title}"" named website is set to comaparison.html.
it will be referenced daily for comparison and we will notify you about any update in it"""
)
