'''Counting Email in a Database'''

import sqlite3

conn=sqlite3.connect("Accessing Databases\databases\orgdb.sqlite")
cur=conn.cursor()

cur.execute("DROP TABLE IF EXISTS Counts")

cur.execute("CREATE TABLE Counts (org TEXT, count INTEGER)")

fname = "Accessing Databases\InputFiles\mbox.txt"

fh=open(fname)
commit_count=0
for line in fh:
    if not line.startswith("From ") :
        continue
    line=line.rstrip()
    pieces=line.split()
    pieces=pieces[1].split("@")
    org=pieces[1]

    cur.execute("SELECT count FROM Counts WHERE org=?",(org,))

    row=cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO Counts (org,count) VALUES (?,1)",(org,))

    else:
        cur.execute("UPDATE Counts SET count=count+1 WHERE org=?",(org,))

conn.commit()



sqlstr="SELECT org,count from Counts ORDER BY count DESC LIMIT 10"

for row in cur.execute(sqlstr):
    print(str(row[0]),row[1])

cur.close()

    

    
    