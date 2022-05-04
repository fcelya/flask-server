import mariadb
import sys

try:
    conn = mariadb.connect(
        user="fcelaya",
        password="passtest",
        host='localhost',
        port=3306,
        database='testdb'
    )
except mariadb.Error as e:
    print(f"Got following error connecting to MariaDB: {e}")
    sys.exit(1)

cur = conn.cursor()
id = 1
try:
    cur.execute("SELECT * FROM tabletest WHERE id=?",(id,))
except mariadb.Error as e:
    print(f"Error: {e}")
for (id,name,age) in cur:
    print(id,name,age)

conn.close()