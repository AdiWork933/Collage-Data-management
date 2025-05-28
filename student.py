from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import os
import re
class StudentClass:
    def __init__(self, window):
        self.window = window
        self.window.title("Student Result Management System")
        self.window.geometry("1200x480+80+170")
        self.window.config(bg="white")
        self.window.focus_force()
        self.window.resizable(False, False)

        #   VARIABLE TYPE DECLEARAION

        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_course = StringVar()
        self.var_a_date = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()

        #   TITLE

        title = Label(self.window, text="Manage Student Details", font=("goudy old style", 20, "bold"), bg="#033054", fg="white")
        title.place(x=10, y=15, width=1180, height=35)

        #   COLOUMN 1

        lbl_roll = Label(self.window, text="Roll NO", font=("goudy old style", 15, "bold"), bg="white")
        lbl_roll.place(x=10, y=60)
        lbl_name = Label(self.window, text="Name", font=("goudy old style", 15, "bold"), bg="white")
        lbl_name.place(x=10, y=100)
        lbl_Email = Label(self.window, text="Email", font=("goudy old style", 15, "bold"), bg="white")
        lbl_Email.place(x=10, y=140)
        lbl_gender = Label(self.window, text="Gender", font=("goudy old style", 15, "bold"), bg="white")
        lbl_gender.place(x=10, y=180)
        lbl_state = Label(self.window, text="State", font=("goudy old style", 15, "bold"), bg="white")
        lbl_state.place(x=10, y=220)
        lbl_address = Label(self.window, text="Address", font=("goudy old style", 15, "bold"), bg="white")
        lbl_address.place(x=10, y=260)

        self.txt_roll = Entry(self.window, textvariable=self.var_roll, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_roll.place(x=150, y=60, width=200)
        self.txt_name = Entry(self.window, textvariable=self.var_name, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_name.place(x=150, y=100, width=200)
        self.txt_email = Entry(self.window, textvariable=self.var_email, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_email.place(x=150, y=140, width=200)
        self.txt_address = Text(self.window, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_address.place(x=150, y=260, width=530, height=100)
        self.txt_state = Entry(self.window, textvariable=self.var_state, font=("goudy old style", 15, "bold"),bg="lightyellow")
        self.txt_state.place(x=150, y=220, width=150)
        self.txt_gender = ttk.Combobox(self.window, textvariable=self.var_gender,values=("select","male","Female","Other"), font=("goudy ols style", 15, "bold"),state='readonly',justify=CENTER)
        self.txt_gender.place(x=150, y=180, width=200)
        self.txt_gender.current(0) #print select

        #   COLOUMN 2

        lbl_dob = Label(self.window, text="D.O.B", font=("goudy old style", 15, "bold"), bg="white")
        lbl_dob.place(x=360,y=60)
        lbl_contact = Label(self.window, text="Contact", font=("goudy old style", 15, "bold"), bg="white")
        lbl_contact.place(x=360, y=100)
        lbl_addmission = Label(self.window, text="Addmission", font=("goudy old style", 15, "bold"), bg="white")
        lbl_addmission.place(x=360,y=140)
        lbl_course = Label(self.window, text="Course", font=("goudy old style", 15, "bold"), bg="white")
        lbl_course.place(x=360,y=180)
        lbl_city = Label(self.window, text="City", font=("goudy old style", 15, "bold"), bg="white")
        lbl_city.place(x=310,y=220)
        lbl_pin = Label(self.window, text="Pin", font=("goudy old style", 15, "bold"), bg="white")
        lbl_pin.place(x=530, y=220)

        self.txt_dob = Entry(self.window, textvariable=self.var_dob, font=("goudy old style", 15, "bold"),bg="lightyellow")
        self.txt_dob.place(x=480, y=60, width=200)
        self.txt_contact = Entry(self.window, textvariable=self.var_contact, font=("goudy old style", 15, "bold"),bg="lightyellow")
        self.txt_contact.place(x=480, y=100, width=200)
        self.txt_addmission = Entry(self.window, textvariable=self.var_a_date, font=("goudy old style", 15, "bold"),bg="lightyellow")
        self.txt_addmission.place(x=480, y=140, width=200)
        self.txt_city = Entry(self.window, textvariable=self.var_city, font=("goudy old style", 15, "bold"),bg="lightyellow")
        self.txt_city.place(x=380, y=220, width=150)
        self.txt_pin = Entry(self.window, textvariable=self.var_pin, font=("goudy old style", 15, "bold"),bg="lightyellow")
        self.txt_pin.place(x=580, y=220, width=100)

        #   COMBO BOX

        self.course_list=[]#function call
        self.fetch_course()
        self.txt_course = ttk.Combobox(self.window, textvariable=self.var_course,values=self.course_list,font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_course.place(x=480, y=180, width=200)
        self.txt_course.set("Select")  # print select

        #   BUTTON

        self.btn_add = Button(self.window, text="Save", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.add)
        self.btn_add.place(x=120, y=400)
        self.btn_update = Button(self.window, text="Update", font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2", command=self.update)
        self.btn_update.place(x=220, y=400)
        self.btn_delete = Button(self.window, text="Delete", font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2", command=self.delete)
        self.btn_delete.place(x=340, y=400)
        self.btn_clear = Button(self.window, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=450, y=400)
        self.btn_hom = Button(self.window, text="Home", font=("goudy old style", 15, "bold"), bg="#FDFF5A", cursor="hand2", command=self.os)
        self.btn_hom.place(x=550, y=400)

        #   SEARCH PANNEL

        self.var_search = StringVar()
        lbl_Search_roll = Label(self.window, text="ROll No", font=("goudy old style", 15, "bold"), bg="white")
        lbl_Search_roll.place(x=720, y=60)
        self.txt_search_roll = Entry(self.window, textvariable=self.var_search, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_search_roll.place(x=850, y=60, width=180)
        lbl_Search = Button(self.window, text="Search", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2", command=self.search)
        lbl_Search.place(x=1070, y=60, width=120, height=28)

        #   CONTENT & SCROLL BARR

        self.C_Frame = Frame(self.window, bd=2, relief="ridge")
        self.C_Frame.place(x=720, y=100, width=470, height=340)
        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)
        self.Coursetable = ttk.Treeview(self.C_Frame, columns=("roll", "name", "email", "gender", "dob","contact","admission","course","state","city","pin","address"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        self.Coursetable.heading("roll", text="Roll No.")
        self.Coursetable.heading("name", text="Name")
        self.Coursetable.heading("email", text="Email")
        self.Coursetable.heading("gender", text="Gender")
        self.Coursetable.heading("dob", text="D.O.B")
        self.Coursetable.heading("contact", text="Contact")
        self.Coursetable.heading("admission", text="Admission")
        self.Coursetable.heading("course", text="Course")
        self.Coursetable.heading("state", text="State")
        self.Coursetable.heading("city", text="City")
        self.Coursetable.heading("pin", text="PIN")
        self.Coursetable.heading("address", text="Address")
        self.Coursetable["show"] = 'headings'

        #   SIZE DECLEARATION OF THE COLOUMN

        self.Coursetable.column("roll", width=100)
        self.Coursetable.column("name", width=100)
        self.Coursetable.column("email", width=100)
        self.Coursetable.column("gender", width=100)
        self.Coursetable.column("dob", width=100)
        self.Coursetable.column("contact", width=100)
        self.Coursetable.column("admission", width=100)
        self.Coursetable.column("course", width=100)
        self.Coursetable.column("state", width=100)
        self.Coursetable.column("city", width=100)
        self.Coursetable.column("pin", width=100)
        self.Coursetable.column("address", width=200)
        self.Coursetable.pack(fill=BOTH, expand=1)
        self.Coursetable.bind("<ButtonRelease-1>", self.get_data)
        self.show()
    def os(self):
        op=messagebox.askyesno("Confirm","Do you really want to go Home?",parent=self.window)
        if op==True:
            self.window.destroy()
            os.system("python data.py")

    def get_data(self, ev):
        try:
            selected_item = self.Coursetable.focus()  # Get selected item from treeview
            values = self.Coursetable.item(selected_item, "values")
            self.var_roll.set(values[0])
            self.var_name.set(values[1])
            self.var_email.set(values[2])
            self.var_gender.set(values[3])
            self.var_dob.set(values[4])
            self.var_contact.set(values[5])
            self.var_a_date.set(values[6])
            self.var_course.set(values[7])
            self.var_state.set(values[8])
            self.var_city.set(values[9])
            self.var_pin.set(values[10])
            self.txt_address.delete("1.0", END)
            self.txt_address.insert(END, values[11])
        except IndexError:
            pass

    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll No should be required", parent=self.window)
            else:
                # Check if email is in the format of @gmail.com
                if not re.match(r"[^@]+@gmail\.com", self.var_email.get()):
                    messagebox.showerror("Error", "Invalid email format. Only Gmail addresses are allowed.",
                                         parent=self.window)
                    return

                # Check if contact number has exactly 10 digits
                if len(self.var_contact.get()) != 10 or not self.var_contact.get().isdigit():
                    messagebox.showerror("Error", "Contact number should be a 10-digit number", parent=self.window)
                    return

                cur.execute("select * FROM student WHERE roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", "Roll No already exists", parent=self.window)
                else:
                    cur.execute(
                        "INSERT INTO student (roll, name , email, gender , dob , contact , admission, course , state, city , pin , address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            self.var_roll.get(),
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_dob.get(),
                            self.var_contact.get(),
                            self.var_a_date.get(),
                            self.var_course.get(),
                            self.var_state.get(),
                            self.var_city.get(),
                            self.var_pin.get(),
                            self.txt_address.get('1.0', END).strip().replace('\n', ' ')
                        ))
                    con.commit()
                    messagebox.showinfo("Success", "Student added successfully", parent=self.window)
                    self.show()
                    self.clear()
        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.window)
    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            selected_item = self.Coursetable.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a record to update", parent=self.window)
                return
            values = self.Coursetable.item(selected_item, "values")
            roll = values[0]
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll No should be required", parent=self.window)
            else:
                cur.execute("UPDATE student SET name=?, email=?, gender=?, dob=?, contact=?, admission=?, course=?, state=?, city=?, pin=?, address=? WHERE roll=?",
                            (
                                self.var_name.get(),
                                self.var_email.get(),
                                self.var_gender.get(),
                                self.var_dob.get(),
                                self.var_contact.get(),
                                self.var_a_date.get(),
                                self.var_course.get(),
                                self.var_state.get(),
                                self.var_city.get(),
                                self.var_pin.get(),
                                self.txt_address.get('1.0', END).strip().replace('\n', ' '),
                                roll
                            ))
                con.commit()
                messagebox.showinfo("Success", "Student updated successfully", parent=self.window)
                self.show()
        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.window)

    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            selected_item = self.Coursetable.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a record to delete", parent=self.window)
                return
            values = self.Coursetable.item(selected_item, "values")
            roll = values[0]
            if messagebox.askyesno("Confirm", "Do you really want to delete this student?", parent=self.window):
                cur.execute("DELETE FROM student WHERE roll=?", (roll,))
                con.commit()
                messagebox.showinfo("Success", "Student deleted successfully", parent=self.window)
                self.show()
                self.clear()
        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.window)

    def clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_a_date.set("")
        self.var_course.set("")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.txt_address.delete('1.0', END)

    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            self.Coursetable.delete(*self.Coursetable.get_children())
            for row in rows:
                self.Coursetable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM student WHERE roll=?", (self.var_search.get(),))
            row = cur.fetchone()
            if row:
                self.Coursetable.delete(*self.Coursetable.get_children())
                self.Coursetable.insert('', END, values=row)
            else:
                messagebox.showinfo("Info", "No record found", parent=self.window)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()
    def fetch_course(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()
            self.course_list=[]
            if len(rows)>0:
                for rows in rows:
                    self.course_list.append(rows[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

#   GUI RUN SECTION

if __name__ == "__main__":
    window = Tk()
    obj = StudentClass(window)
    window.mainloop()
