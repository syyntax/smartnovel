<img src="https://github.com/syyntax/smartnovel/blob/master/westridge_25.png" width=30%>

# Westridge University

**Westridge University** is a fictional university from which to theme CTF challenges around.

## Constructors

Script | Description
-------|-------------
`bin/generators.py` | A Python program that creates information that can be used in generating random user profiles (e.g. usernames, first and last names, physical addresses, etc.)
`bin/leetify.py` | A Python program that converts normal text into 1337-speak (used by `generators.py` to create usernames and email addresses.
`bin/main.py` | A Python program that holds the User and Address classes for creating random user profiles.
`bin/build_db.py` | A Python program that builds and populates the Westridge MySQL database.

### Generate a Random User Profile

Use the `main.py` program to generate a random user profile.
```bash
python3 -i main.py
```
```python
user = create_user()
```
