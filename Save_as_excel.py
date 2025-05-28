import sqlite3
import pandas as pd

def create_db():
    try:
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS course(Cid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, duration TEXT, charges TEXT, description TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS student(roll INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, gender TEXT, dob TEXT, contact TEXT, admission TEXT, course TEXT, state TEXT, city TEXT, pin TEXT, address TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS result(rid INTEGER PRIMARY KEY AUTOINCREMENT, roll TEXT, name TEXT, course TEXT, CA1 TEXT, CA2 TEXT, CA3 TEXT, CA4 TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT, f_name TEXT, l_name TEXT, contact TEXT, email TEXT, question TEXT, answer TEXT, password TEXT)")
        con.commit()
        print("Database created successfully!")
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
    finally:
        if con:
            con.close()

def export_to_excel(table_name, file_name):
    try:
        con = sqlite3.connect("rms.db")
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", con)
        df.to_excel(file_name, index=False)
        print(f"Exported {table_name} table to {file_name} successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if con:
            con.close()

# Create the SQLite database if not exists
create_db()

# Example usage:
export_to_excel("course", "course_data.xlsx")
export_to_excel("student", "student_data.xlsx")
export_to_excel("result", "result_data.xlsx")
export_to_excel("employee", "employee_data.xlsx")
