import mariadb
import random
from time import sleep

def clean(cur,conn):
    cur.close()
    conn.close()
    return

def predict(n):
    fr0=1
    fr1=4
    fr2=10

    n0=fr0*fr1*fr2/fr0
    n1=fr0*fr1*fr2/fr1
    n2=fr0*fr1*fr2/fr2

    pr0 = n0/(n0+n1+n2)
    pr1 = n1/(n0+n1+n2)
    #pr2 = n2/(n0+n1+n2)
    
    k = random.random()
    if k<pr0:
        e = "0"
    elif k<(pr0+pr1):
        e="1"
    else:
        e="2"

    return e

def status_updater():
    while True:
        try:
            conn = mariadb.connect(
                user="fcelaya",
                password="passtest",
                host='localhost',
                port=3306,
                database='prl'
            )
        except mariadb.Error as e:
            print(f"Got following error connecting to MariaDB: {e}")
        
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT DISTINCT(device_id) FROM devices;")
        except mariadb.Error as e:
            print(f"Error: {e}")
        devices_list = []
        for device in cur:
            devices_list.append(device[0])

        for device in devices_list:
            try:
                cur.execute(f"""SELECT heart_rate FROM health WHERE id=(SELECT MAX(id) FROM health WHERE device_id="{device}" and heart_rate is not NULL);""")
                hr = cur.fetchall()
            except mariadb.Error as e:
                print(f"Error: {e}")
            if len(hr)==0:
                hr=[[65]]

            hr = hr[0][0]
            emergency = predict(hr)

            try:
                cur.execute(f"""UPDATE devices SET emergency={emergency} WHERE device_id="{device}";""")
                conn.commit()
            except mariadb.Error as e:
                print(f"Error: {e}")
            
        cur.close()
        conn.close()
        sleep(10)
    
    return

if __name__=="__main__":
    print(status_updater())