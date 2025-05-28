import sqlite3

def create_db():
    con = sqlite3.connect(database="rms.db")
    cur = con.cursor()
    try:
        # Cid->Course id
        cur.execute("CREATE TABLE IF NOT EXISTS course(Cid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, duration TEXT, charges TEXT, description TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS student(roll INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, gender TEXT, dob TEXT, contact TEXT, admission TEXT, course TEXT, state TEXT, city TEXT, pin TEXT, address TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS result(rid INTEGER PRIMARY KEY AUTOINCREMENT, roll TEXT, name TEXT, course TEXT, CA1 TEXT, CA2 TEXT, CA3 TEXT, CA4 TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT, f_name TEXT, l_name TEXT, contact TEXT, email TEXT, question TEXT, answer TEXT, password TEXT)")
        con.commit()
        print("Database created successfully!")
    except sqlite3.Error as e:
        print("Error creating database:", e)
    finally:
        con.close()

create_db()

import sqlite3
con=sqlite3.connect(database="rms.db")
cur=con.cursor()