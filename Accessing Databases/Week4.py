''''This application will read roster data in JSON format, parse the file, and then produce an SQLite database that contains a User, Course, and Member table 
and populate the tables from the data file.'''

import json
import sqlite3

conn=sqlite3.connect("Accessing Databases\databases\coursedb.sqlite")

cur=conn.cursor()
cur.executescript(''' 
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)

''')

fname="Accessing Databases\InputFiles\roster_data.json"

data=open(fname).read()
json_data=json.loads(data)

for entry in json_data:
    user_name=entry[0]
    course_title=entry[1]
    role=entry[2]

    if user_name is None or course_title is None : 
        continue

    cur.execute('INSERT OR IGNORE INTO User(name) VALUES(?)',(user_name,))
    cur.execute('SELECT id FROM User WHERE name= ?',(user_name,))
    user_id= cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Course(title) VALUES(?)',(course_title,))
    cur.execute('SELECT id FROM Course WHERE title= ?',(course_title,))
    course_id= cur.fetchone()[0]

    cur.execute('INSERT OR REPLACE INTO Member(user_id,course_id,role) VALUES(?,?,?)',(user_id,course_id,role))

conn.commit()