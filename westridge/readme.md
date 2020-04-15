<img src="https://github.com/syyntax/smartnovel/blob/master/img/westridge_25.png" width=30%>

# Westridge University

**Westridge University** is a fictional university from which to theme CTF challenges around.

## Constructors

Script | Description
-------|-------------
`bin/generators.py` | A Python program that creates information that can be used in generating random user profiles (e.g. usernames, first and last names, physical addresses, etc.)
`bin/leetify.py` | A Python program that converts normal text into 1337-speak (used by `generators.py` to create usernames and email addresses.
`bin/main.py` | A Python program that holds the User and Address classes for creating random user profiles.
`bin/build_db.py` | A Python program that builds and populates the Westridge MySQL database.

## Getting Started
### Setup MySQL
First, create a MySQL instance (docker or VM).  If you're standing up a MySQL container in Docker, make sure to bind the container TCP port 3306 to the host TCP port 3306.
Once the image is up, console into the image and run the following command to configure MySQL:
```bash
mysql_secure_installation
```
Select "No" for each of the inquiries throughout setup:
```text
Press y|Y for Yes, any other key for No:
Using existing password for root.
Change the password for root ? ((Press y|Y for Yes, any other key for No) :
...
Remove anonymous users? (Press y|Y for Yes, any other key for No) :
...
Disallow root login remotely? (Press y|Y for Yes, any other key for No) :
...
Remove test database and access to it? (Press y|Y for Yes, any other key for No) :
```
On the last inquiry, enter **y** for **yes**
```text
Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y
```
### Create the Database
From the terminal, access MySQL and create the **westridge** database.
```bash
mysql -u root -p
```
You will enter a MySQL terminal.  Enter the following SQL to create the database.
```mysql
CREATE DATABASE westridge;
```
### Build the Database Tables
#### Configuration
Configure the <a href="data/config.json">data/config.json</a> file based on your setup.
Field|Description
-----|-----
host|The IP or domain of the MySQL server
port|The TCP port serving the MySQL server (default is **3306**)
db|The database name (default is **westridge**)
user|The user accessing the database (default is **root**)
passwd|The MySQL password for the user accessing the database (default is **smartnovelmysql**)

#### Launch Script
From the terminal, execute the script with the command below.
```bash
python3 build.py
```
