from pymysql import connect
from json import loads
from os.path import abspath, join, dirname
from sys import exit
from main import create_address, create_user


class connection(object):
    def __init__(self, host, user, passwd, db, port):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port


def create_db(conn):
    try:
        # Make the connection to the database
        cur = conn.cursor()
        sql_list = loads(open(abspath(join(script_path, '..', 'data', \
            'tables.json')), 'r').read())
        for i in sql_list["tables"]:
            cur.execute(sql_list["tables"][i][0])
            conn.commit()

        return None
    except:
        print(f'An error occurred while creating the database tables.')
        exit
    
'''
def populate_users(conn, num_users=10):
    if conn == None:
        raise Exception(f'conn argument may not be NoneType.')
    if not type(num_users) is int:
        raise Exception(f'num_users must be an integer.')
    if num_users < 1:
        raise Exception(f'num_users argument must be no less than one.')
    try:
        cur = conn.cursor()
        for i in range(1, num_users):
            user = create_user()
            sql = f"INSERT INTO {conn_obj.db} "
'''


def populate_countries(conn):
    if conn == None:
        raise Exception(f'conn argument may not be NoneType')
    try:
        cur = conn.cursor()
        countries_list = loads(open(abspath(join(script_path, '..', 'data', \
            'countries.json')), 'r').read())
        for i in countries_list:
            sql = f"INSERT INTO countries (country_name, country_abbrev) " \
                f"VALUES ('{countries_list[i]}', '{i}');"
            cur.execute(sql)
            conn.commit()
    except:
        raise Exception(f'An error occurred while populating the countries.')


# MAIN
script_path = dirname(abspath(__file__))
conn_json = loads(open(abspath(join(script_path, '..', 'data', 'config.json' \
    )), 'r').read())
host = conn_json["mysql"]["host"][0]
port = conn_json["mysql"]["port"][0]
user = conn_json["mysql"]["user"][0]
passwd = conn_json["mysql"]["passwd"][0]
db = conn_json["mysql"]["db"][0]

conn_obj = connection(host=host, user=user, passwd=passwd, db=db, \
    port=port)

conn = connect(host=conn_obj.host, user=conn_obj.user, passwd=conn_obj.passwd, \
    db=conn_obj.db, port=conn_obj.port)

create_db(conn)
populate_countries(conn)
