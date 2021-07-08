import json

def recurse_print(d):
    if not (type(d) is list):
        if type(d) is str and d.startswith("/geo/type/establishment"):
            print(d)
        return
    
    for i in range(len(d)):
        if d[i]:
            recurse_print(d[i])

with open("jsontext.txt") as f:
    d = json.load(f)
    recurse_print(d[6][100])