import json
import os

rem_url = input("URL OF SITE TO BE REMOVED: ")

data = json.load(open("urls.json")).urls


for i in range(len(data)):
    if data[i].url == rem_url:
        del data[i]
        os.remove(f"comparison{i+1}.html")
        for j in range(i, len(data) + 1):
            os.rename(f"comparison{j+1}.html", f"comparison{j}.html")
        break
