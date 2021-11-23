import json

dicto = {"LAST_LOAD_FILE" : None}

data = json.dumps(dicto)

with open("config.json", 'w') as f:
    f.write(data)