import mongoengine

#mongodb://<dbuser>:<dbpassword>@ds241055.mlab.com:41055/projectlenkeo

host = "ds241055.mlab.com"
port = 41055
db_name = "projectlenkeo"
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
