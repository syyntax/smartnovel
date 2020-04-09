import generators

class User(object):
    def __init__(self, fname, sname, mname, gender, uname, email, address, dob):
        self.fname = fname
        self.sname = sname
        self.mname = mname
        self.gender = gender
        self.uname = uname
        self.email = email
        self.address = address
        self.dob = dob


class Address(object):
    def __init__(self, streetnum, street, city, state, country, zipcode):
        self.streetnum = streetnum
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.zipcode = zipcode


def create_user(fname=None, sname=None, mname=None, gender=None, uname=None, \
    email=None, address=None, dob=None):
    gender = generators.set_gender(gender=gender)
    fname = generators.set_fname(fname=fname, gender=gender)
    sname = generators.set_sname(sname=sname)
    mname = generators.set_mname(mname=mname)
    uname = generators.set_uname(uname=uname)
    email = generators.set_email(site=None, uname=uname)
    address = create_address()
    dob = generators.set_dob(dob=dob)

    user = User(fname, sname, mname, gender, uname, email, address, dob)

    return user


def create_address(streetnum=None, street=None, city=None, state=None, \
    country="US", zipcode=None):
    streetnum = generators.set_streetnum(streetnum=streetnum)
    street = generators.set_streetname(streetname=street)
    state = generators.set_state(state=state)
    city = generators.set_city(state=state)
    zipcode = generators.get_zipcode(state=state, city=city)

    address = Address(streetnum, street, city, state, country, zipcode)

    return address


def get_details(user=None):
    if user == None:
        user = create_user()
    
    print(f'FIRST:\t\t{user.fname}\r\n' \
        f'LAST:\t\t{user.sname}\r\n' \
        f'MIDDLE:\t\t{user.mname}\r\n' \
        f'GENDER:\t\t{str.upper(user.gender)}\r\n' \
        f'USERNAME:\t{user.uname}\r\n' \
        f'EMAIL:\t\t{user.email}\r\n' \
        f'ADDRESS:\t{user.address.streetnum} {user.address.street}, ' \
            f'{user.address.city}, {user.address.state}, ' \
            f'{user.address.country} {user.address.zipcode}\r\n' \
        f'DOB:\t\t{user.dob}')
