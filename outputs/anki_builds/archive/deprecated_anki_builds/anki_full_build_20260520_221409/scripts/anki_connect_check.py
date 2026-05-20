#!/usr/bin/env python3
import json, urllib.request
URL="http://127.0.0.1:8765"
def call(action, **params):
    data=json.dumps({"action":action,"version":6,"params":params}).encode()
    req=urllib.request.Request(URL,data=data,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=5) as r:
        return json.loads(r.read())
for action in ["version","deckNames","modelNames"]:
    print(action, call(action))
print("RuankaoTopicCard fields:", call("modelFieldNames", modelName="RuankaoTopicCard"))
