import mongoengine

# mongodb://<dbuser>:<dbpassword>@ds119685.mlab.com:19685/warm_winter

host = "ds119685.mlab.com"
port = 19685
db_name = "warm_winter"
user_name = "admin"
password = "admin"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())
