import json
import  re
import requests
import logging

log = logging.getLogger(__name__)

def parse_response(url):
    try:
        return json.loads(requests.get(url).text[4:])
    except:
        log.error(f"JSON Parse error for  url: {url}")
        return {}


def parse_place(j):
    
    tags = []
    labels = {"black": False, "women": False, "lgbtq": False, "veteran": False}
    
    if not j or not j[6] or not j[6][100] or not j[6][13]:
        return tags, labels, []
    
    def update_labels(d):
        labels["black"] = labels["black"] or "is_black_owned" in d
        labels["women"] = labels["women"] or "is_owned_by_women" in d
        labels["lgbtq"] = labels["lgbtq"] or "welcomes_lgbtq" in d
        labels["veteran"] = labels["veteran"] or "is_owned_by_veterans" in d

    def explore_tags(d):
        if not d:
            return
        if type(d) is str and d.startswith("/geo/type/establishment"):
            tags.append(d)
            update_labels(d)
        if not (type(d) is list):
            return
        for i in range(len(d)):
            explore_tags(d[i])

    explore_tags(j[6][100]) #part of response  that has geo establishment  types
    descriptors = j[6][13]

    return tags, labels, descriptors

def parse_author_id(r):
    author_field = r[0]
    if author_field and type(author_field) is list and len(author_field) > 0:
        return re.search(r'(?<=maps/contrib/)[\d]+', author_field[0]).group()
    return None

def parse_author_name(r):
    author_field = r[0]
    if author_field and type(author_field) is list and len(author_field) > 1:
        return author_field[1]
    return None

def parse_review_list(j):
    if not j[2]:
        return []
    return [{
        "author_id": parse_author_id(r),
        "author_name": parse_author_name(r),
        "timeframe": r[1],
        "text": r[3],
        "rating": r[4]
        } for r in j[2]]

if __name__  == '__main__':
    with open("jsontext2.txt") as f:
        d = json.load(f)
        print(parse_review_list(d))