import json

filename = "files.json"

def readFile(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        return json.load(f)

def getData(key):
    data = readFile(filename)
    if key == "Main-Dir": return data[key]
    return data.get("files", {}).get(key)