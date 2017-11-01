import mongoengine

host = "ds237445.mlab.com"
port = 37445
db_name = "lenkeo"
user_name = "admin"
password = "iamyouradminhahaha"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())
