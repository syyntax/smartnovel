from random import randint
from json import loads
from os.path import abspath, join, dirname
from re import match, compile
from sys import exit
from datetime import datetime
from leetify import leetify

script_path = dirname(abspath(__file__))
reg_state = compile("^[a-zA-Z]{2}$")  # Regex for state abbreviations
reg_address = compile("^[0-9]{1,5}$")


def json_load(read_file, criteria=None):
    json_string = read_file
    data_store = loads(json_string)
    return list(data_store[criteria])


def set_gender(gender=None):
    if gender == None:
        genders = ('m', 'f')
        return genders[randint(0, 1)]
    else:
        return gender


def set_fname(gender=None, fname=None):
    if gender == None:
        gender = set_gender()
    
    if fname == None:
        try:
            fname_list = json_load(open(abspath(join(script_path, '..', \
                'data', 'names.json')), 'r').read(), str.lower(gender))
            fname_picked = fname_list[randint(0, len(fname_list) - 1)]
            del fname_list
            return fname_picked
        except:
            print('Oops! There are only two genders!')
            exit
            pass
    else:
        return str.upper(fname)


def set_sname(sname=None):
    if sname == None:
        try:
            sname_list = json_load(open(abspath(join(script_path, '..', \
                'data', 'names.json')), 'r').read(), 'surnames')
            sname_picked = sname_list[randint(0, len(sname_list) - 1)]
            del sname_list
            return sname_picked
        except:
            print('Oops! An error occurred when setting the last name.')
            exit
            pass
    else:
        return str.upper(sname)


def set_mname(mname=None):
    if mname == None:
        mname_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return mname_string[randint(0, len(mname_string) - 1)]
    elif mname == "None":
        return ''
    else:
        return str.upper(mname)


def set_uname(uname=None, leetify_set=None):
    separator = ('.', '_', '')
    num_odds = randint(0, 2) # Odds that the username will end in numbers
    num_range = (1, 9999) # Number range to use if username ends in numbers
    if uname == None:
        try:
            uname_list = json_load(open(abspath(join(script_path, '..', \
                'data', 'usernames.json')), 'r').read(), 'normal')
            uname1_picked = uname_list[randint(0, len(uname_list) - 1)]
            uname2_picked = uname_list[randint(0, len(uname_list) - 1)]
            uname_picked = f'{uname1_picked}' \
                f'{separator[randint(0, len(separator) - 1)]}' \
                f'{uname2_picked}'
            del uname_list
            if leetify_set == None:
                leetify_rand = randint(0, 1)
                if leetify_rand == 0:
                    uname_picked = leetify(uname_picked, 4)
            elif leetify == True:
                uname_picked = leetify(uname_picked, 4)
            if num_odds == 1:
                uname_picked += f'{randint(num_range[0], num_range[1])}'
            return uname_picked
        except:
            print("Oops! An error occurred when setting the username.")
            exit
            pass
    else:
        return uname


def set_email(site=None, uname=None):
    if site == None:
        try:
            email_list = json_load(open(abspath(join(script_path, '..', \
                'data', 'sites.json')), 'r').read(), 'sites')
            if uname == None:
                uname = set_uname()
            email_picked = email_list[randint(0, len(email_list) - 1)]
            email_picked = f'{uname}@{email_picked}'
            del email_list
            return email_picked
        except:
            print("Oops! An error occurred when setting the email address.")
            exit
            pass
    else:
        return f'{uname}@{site}'            


def set_streetnum(streetnum=None):
    if streetnum == None:
        try:
            return randint(10, 4999)
        except:
            print("Oops! An error occurred when setting the street number.")
            exit
            pass
    else:
        if match(reg_address, streetnum):
            return streetnum


def set_streetname(streetname=None):
    if streetname == None:
        try:
            mods_list = ['']
            # The odds that a street name will have a mod (i.e. N, S, etc.)
            mods_odds = randint(0, 10)
            streetname_list = json_load(open(abspath(join(script_path, '..', \
                'data', 'streets.json')), 'r').read(), 'names')
            if mods_odds == 1:
                mods_list = json_load(open(abspath(join(script_path, '..', \
                    'data', 'streets.json')), 'r').read(), 'mods')
            streetname_picked = streetname_list[randint(0, \
                len(streetname_list) - 1)]
            try:
                mods_picked = f'{mods_list[randint(0, len(mods_list) - 1)]}'
            except:
                print("Oops! An error occurred with the mods.")
                pass
            types_list = json_load(open(abspath(join(script_path, '..', \
                'data', 'streets.json')), 'r').read(), 'types')
            types_picked = types_list[randint(0, len(types_list) - 1)]
            del streetname_list
            del types_list
            if len(mods_list) > 1:
                return f'{mods_picked} {streetname_picked} {types_picked}'
            else:
                return f'{streetname_picked} {types_picked}'
        except:
            print("Oops! An error occurred when setting the street name.")
            exit
            pass


def set_state(state=None):
    if state == None:
        try:
            states_list = json_load(open(abspath(join(script_path, '..', \
                'data', 'states.json')), 'r').read(), 'states')
            state_picked = states_list[randint(0, len(states_list) - 1)]
            return state_picked
        except:
            print("Oops! An error occurred when setting the state.")
            exit
            pass
    else:
        return state


def set_city(city=None, state=None):
    if city == None:
        try:
            if state == None:
                try:
                    state = set_state()
                except:
                    print('Oops! An error occurred when setting the city\'s' \
                        'state.')
            else:
                if match(reg_state, state):
                    pass
                else:
                    print('Oops! That\'s not a valid state!')
                    exit
            cities_list = loads(open(abspath(join(script_path, '..', \
                'data', 'states.json')), 'r').read())
            cities_state_list = list(cities_list['states'][state]['cities'] \
                .keys())
            city_picked = cities_state_list[randint(0, len(cities_state_list) \
                - 1)]
            del cities_list
            del cities_state_list
            return f'{city_picked}'
        except:
            print('Oops! An error occurred when setting the city.')
    
    else:
        return city


def get_zipcode(state, city):
    zips_list = loads(open(abspath(join(script_path, '..', 'data', \
        'states.json')), 'r').read())
    zipcode = zips_list['states'][state]['cities'][city][randint(0, \
        len(zips_list['states'][state]['cities'][city]) - 1)]
    
    return zipcode


def set_dob(dob=None, start=1980, end=2002):
    if dob == None:
        dob = datetime(randint(1980, 2002), randint(1, 12), randint(1, 28))
        return dob
    else:
        return dob
