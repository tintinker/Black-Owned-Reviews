import json

def condition(obj):
    return "162" in str(obj)

def recurse_print(d, prev_keys):
    
    if condition(d):
        print("found", prev_keys)

    if not (type(d) is list):
        return
    
    for i in range(len(d)):
        if d[i]:
            recurse_print(d[i], prev_keys + [i])

with open("jsontext.txt") as f:
    d = json.load(f)
    recurse_print(d, [])