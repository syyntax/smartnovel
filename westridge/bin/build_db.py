from pymysql import connect
from json import loads
from os.path import abspath, join, dirname


class connection(object):
    def __init__(self, host, user, passwd, db, port):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port


def create_db(connection, db_name="westridge"):
    # Make the connection to the database
    return None


# MAIN
script_path = dirname(abspath(__file__))
conn_json = loads(open(abspath(join(script_path, '..', 'data', 'config.json' \
    )), 'r').read())
host = conn_json["mysql"]["host"][0]
port = conn_json["mysql"]["port"][0]
user = conn_json["mysql"]["user"][0]
passwd = conn_json["mysql"]["passwd"][0]
db = conn_json["mysql"]["db"][0]

conn = connection(host=host, user=user, passwd=passwd, db=db, port=port)
