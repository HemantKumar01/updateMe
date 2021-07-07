import sys
import json
import os

if (len(sys.argv) < 2):
    print(
        f"no argument found! type 'python {sys.argv[0]} -help' for the list of args")
    sys.exit()

command = sys.argv[1]


if command not in ('-reset', '-show', '-help', '?'):
    print(
        f"invalid arg! type 'python {sys.argv[0]} -help' for the list of commands")
    sys.exit()

if(command in ('?', '-help')):
    print(f'''------------{sys.argv[0]} help--------------

arguments-
-----------
-reset : re-inits the urls.json(all data) and clears all websites which are in queue to be watched for updates;
-show : shows urls.json (all data about stored website);
-help :show all commands;
? : short form for -help
''')

if(command == '-reset'):
    data = open("urls.json", "w")
    data.write('{"urls":[]}')
    test = os.listdir("./")
    for item in test:
        if item.endswith(".html"):
            os.remove(os.path.join("./", item))
    print("data re-initialized; reset complete")
elif(command == '-show'):
    data = open("urls.json", "r").read()
    print("SHOWING urls.json - \n")
    print(json.loads(data))
