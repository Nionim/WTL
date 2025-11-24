import json, os
from dotenv import load_dotenv

filename = "files.json"


load_dotenv()
root_dir = os.getenv("main_dir")

def readFile(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        return json.load(f)

def getData(key):
    data = readFile(filename)
    if key == "Main-Dir": 
        return data[key]
    
    main_dir = data['Main-Dir'].replace("\\", "/")
    normalized_key = key.replace("\\", "/")
    
    if normalized_key.startswith(main_dir + "/"):
        normalized_key = normalized_key.replace(main_dir + "/", "").replace("~/", root_dir)
        print(normalized_key)
    
    return data.get("files", {}).get(normalized_key)

def getCommands():
    data = readFile(filename)
    commands = data.get("Init-Commands", {})
    returned = []
    for c in commands:
        c = c.replace("~/", root_dir)
        returned.append(c)
    return returned