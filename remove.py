import json
import os


print(
    "exact URLs of sites as set in reference is present at urls.json. open with code and press CTRL+S to show it."
)
rem_url = input("URL OF SITE TO BE REMOVED: ")

data = json.load(open("urls.json"))["urls"]


for i in range(len(data)):
    if data[i]["url"] == rem_url:
        del data[i]
        os.remove(f"./reference_files/comparison{i+1}.html")
        for j in range(i + 1, len(data) + 1):
            os.rename(
                f"./reference_files/comparison{j+1}.html",
                f"./reference_files/comparison{j}.html",
            )
        break

json.dump({"urls": data}, open("urls.json", "w"), indent=4)
print("URL Removed Completely.")
