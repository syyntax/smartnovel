from pymysql import connect
from hashlib import sha1
from json import loads
from os.path import abspath, join, dirname
from random import randint
from sys import exit
from main import create_address, create_user
from datetime import datetime


class connection(object):
    def __init__(self, host, user, passwd, db, port):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port


def execute_sql(conn, sql):
    cursor = conn.cursor()

    try:
       cursor.execute(sql)
    except:
        raise Exception(f'An error occurred while executing the SQL:\n\n' \
        f"{sql}")
    finally:
        conn.commit()
        return cursor.fetchone()


def get_passwd_sha1(passwd=None):
    if passwd == None:
        passwd = ''
        counter = randint(10, 16)
        char_set = ['ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' \
            '1234567890!@#$%^&*']
        while counter > 0:
            passwd += (char_set[0][randint(0, len(char_set) - 1)] + \
                str(randint(1, 1000000)))
            counter -= 1
    try:
        digest = sha1()
        digest.update(str.encode(f'{passwd}'))
        return digest.hexdigest()
    except:
        raise Exception(f'An error occurred while generating the hash.')


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
        del countries_list
    except:
        raise Exception(f'An error occurred while populating the countries.')


def populate_states(conn):
    if conn == None:
        raise Exception(f'conn argument may not be NoneType')
    try:
        cur = conn.cursor()
        states_list = loads(open(abspath(join(script_path, '..', 'data', \
            'state_abbrev.json')), 'r').read())
        for i in states_list:
            sql = f"INSERT INTO states (state_full, state_abbrev, country_id)" \
            f" VALUES ('{i}', '{states_list[i]}', 199);" #199 = US
            cur.execute(sql)
            conn.commit()
        del states_list
    except:
        raise Exception(f'An error occurred while populating the states.')


def populate_users(conn, num_users=10, role=None):
    if conn == None:
        raise Exception(f'conn argument may not be NoneType.')
    if not type(num_users) is int:
        raise Exception(f'num_users must be an integer.')
    if num_users < 1:
        raise Exception(f'num_users argument must be no less than one.')
    try:
        for i in range(1, num_users + 1):
            user = create_user()

            # Get the state_id of the user object's state
            state_sql = "SELECT state_id FROM states WHERE state_abbrev = " \
                f"'{user.address.state}';"
            a = execute_sql(conn, state_sql)
            state_id = int(a[0])

            # Create the user record
            sql = "INSERT INTO users (username, first, last, middle, email, " \
                "street, city, state_id, zip, gender, dob) VALUES (" \
                f"'{user.uname}', '{user.fname}', '{user.sname}', " \
                f"'{user.mname}', '{user.email}', '{user.address.streetnum} " \
                f"{user.address.street}', '{user.address.city}', {state_id}, " \
                f"'{user.address.zipcode}', '{user.gender}', '{user.dob}');"
            execute_sql(conn, sql)

            # Get the user id
            user_sql = "SELECT user_id FROM users WHERE username = " \
                f"'{user.uname}';"
            a = execute_sql(conn, user_sql)
            user_id = a[0]

            # Create the user's password
            sql = "INSERT INTO passwords (password, user_id) VALUES (" \
                f"'{get_passwd_sha1()}', '{user_id}');"
            execute_sql(conn, sql)

            # Create the user's role
            try:
                if role == None:
                    roles_json = loads(open(abspath(join(script_path, '..', 'data', \
                        'roles.json')), 'r').read())
                    roles_list = roles_json['roles']
                    roles_prob_list = []
                    for i in roles_list:
                        for x in range(0, roles_list[i]['ratio']):
                            roles_prob_list.append(i)
                    
                    # Get the role id
                    role_sql = "SELECT role_id FROM roles WHERE role_name = " \
                        f"'{roles_prob_list[randint(0, len(roles_prob_list) - 1)]}'"
                    a = execute_sql(conn, role_sql)
                    role_id = a[0]

                    # Create the user's assigned role record
                    sql = "INSERT INTO roles_assigned (role_id, user_id) VALUES (" \
                        f"{role_id}, {user_id});"
                    execute_sql(conn, sql)
                else:
                     # Create the user's assigned role record
                    sql = "INSERT INTO roles_assigned (role_id, user_id) VALUES (" \
                        f"{role}, {user_id});"
                    execute_sql(conn, sql)
            except:
                raise Exception(f'An error occurred while assigning the ' \
                f'user\'s role: {role}.')
            
            finally:
                pass

    except:
        raise Exception("An error occurred while populating the users.")
    
    finally:
        pass


def populate_roles(conn):
    if conn == None:
        raise Exception(f'conn argument may not be NoneType.')
    roles_json = loads(open(abspath(join(script_path, '..', 'data', \
        'roles.json')), 'r').read())
    try:
        roles_list = roles_json['roles']
        for i in roles_list:
            sql = f"INSERT INTO roles (role_name) VALUES ('{i}');"
            execute_sql(conn, sql)
    except:
        raise Exception(f'An error occurred while populating the roles.')


def populate_degree_types(conn):
    if conn == None:
        raise Exception(f'conn argument may not be NoneType.')
    try:
        degree_types_json = loads(open(abspath(join(script_path, '..', \
            'data', 'degree_types.json')), 'r').read())['degree_types']
        for degree in degree_types_json:
            for area in degree_types_json[degree]:
                for program in degree_types_json[degree][area]:
                    sql = f"INSERT INTO degree_types (degree_type_name, " \
                        f"ttl_sem_hrs) VALUES ('{degree}s of {area} in " \
                        f"{program}', " \
                        f"{degree_types_json[degree][area][program]});"
        
                    execute_sql(conn, sql)
    except:
        raise Exception(f'An error occurred while populating the degree types.')


def populate_terms(conn):
    if conn == None:
        raise Exception(f'conn argument may not be NoneType.')
    try:
        terms_json = loads(open(abspath(join(script_path, '..', 'data', \
            'terms.json')), 'r').read())['Terms']
        for term in terms_json:
            start = terms_json[term]["start_date"]
            end = terms_json[term]["end_date"]
            term_name = "term"
            description = "description"
            sql = f"INSERT INTO terms (term_name, start_date, end_date, " \
            f"description) VALUES ('{terms_json[term][term_name]}', " \
            f"'{datetime(start[0], start[1], start[2])}', " \
            f"'{datetime(end[0], end[1], end[2])}', " \
            f"'{terms_json[term][description]}');"
            
            execute_sql(conn, sql)
    except:
        raise Exception(f'An error occurred while populating the terms.')
    finally:
        pass


def populate_courses(conn):
    if conn == None:
        raise Exception(f'conn argument may not be NoneType.')
    try:
        courses_json = loads(open(abspath(join(script_path, '..', 'data', \
            'catalog.json')), 'r').read())
        for category in courses_json:
            for course in courses_json[category]:
                for description in courses_json[category][course]:
                    sql = f'INSERT INTO courses (title, level, ' \
                        f'description, long_description, sem_hours) VALUES ' \
                        f'(\"{course}\", \"0\", \"{course} - {description}\",' \
                        f' \"\", 3)'';'
                    
                    execute_sql(conn, sql)
    except:
        raise Exception(f'An error occurred while populating the courses.')
    finally:
        pass


def populate_term_courses(conn, number=1000):
    if conn == None:
        raise Exception(f'conn argument may not be NoneType.')
    try:
        term_sql = "SELECT term_id FROM terms;"
        course_sql = "SELECT course_id FROM courses;"
        instructor_sql = "SELECT user_id FROM roles_assigned WHERE role_id = " \
            "2 OR role_id = 3 OR role_id = 4 OR role_id = 5;"
        cur = conn.cursor()
        
        #Store SELECT results for terms
        cur.execute(term_sql)
        terms = cur.fetchall()

        #Store SELECT results for courses
        cur.execute(course_sql)
        courses = cur.fetchall()

        #Store SELECT results for instructors
        cur.execute(instructor_sql)
        instructors = cur.fetchall()
        
        for i in range(0, number):
            sql = f'INSERT INTO term_courses (term_id, course_id, ' \
                f'instructor) VALUES (' \
                f'{terms[randint(0, len(terms) - 1)][0]}, ' \
                f'{courses[randint(0, len(courses) - 1)][0]}, ' \
                f'{instructors[randint(0, len(instructors) - 1)][0]});'

            execute_sql(conn, sql)

    except:
        raise Exception(f'An error occurred while populating the term courses.')
    finally:
        pass


def populate_enrollments(conn):
    if conn == None:
        raise Exception(f'conn argument may not be NoneType.')
    try:
        termcrses_sql = "SELECT term_crs_id FROM term_courses;"
        users_sql = "SELECT users.user_id FROM users INNER JOIN " \
        "roles_assigned ON users.user_id = roles_assigned.user_id WHERE " \
        "roles_assigned.role_id = 1;"
        cur = conn.cursor()

        #Store SELECT results for term courses
        cur.execute(termcrses_sql)
        termcrses = cur.fetchall()

        #Store SELECT results for users
        cur.execute(users_sql)
        users = cur.fetchall()

        # Iterate through each term course, assigning students at random
        for i in termcrses:
            tmp_users = list(users) # create a tmp users list to reduce duplicates
            num_students = randint(10, 20)
            for student in range(0, num_students):
                student_id = tmp_users[randint(0, len(tmp_users) - 1)]
                sql = f'INSERT INTO enrollments (user_id, term_crs_id, ' \
                f'payment_status_id) VALUES ({student_id[0]}, {i[0]}, 2);'
                tmp_users.remove(student_id)

                execute_sql(conn, sql)
                #print(f'{sql}')
    except:
        raise Exception(f'An error occurred while populating the enrollments.')
    
    finally:
        pass


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

#create_db(conn)
#populate_countries(conn)
#populate_states(conn)
#populate_roles(conn)
#populate_users(conn, 400, 1)
#populate_degree_types(conn)
#populate_terms(conn)
#populate_courses(conn)
#populate_term_courses(conn, 1000)
#populate_enrollments(conn)
