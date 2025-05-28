from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import os
class CourseClass:
    def __init__(self, window):
        self.window = window
        self.window.title("Student Result Management System")
        self.window.geometry("1200x480+80+170")
        self.window.config(bg="white")
        self.window.focus_force()
        self.window.resizable(False, False)

        #   VARIABLE TYPE DECLERATION

        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()

        #   HEADING

        title = Label(self.window, text="Manage Course Details", font=("goudy old style", 20, "bold"), bg="#033054", fg="white")
        title.place(x=10, y=15, width=1180, height=35)

        #   LABEL

        lbl_CourseName = Label(self.window, text="Course Name", font=("goudy old style", 15, "bold"), bg="white")
        lbl_CourseName.place(x=10, y=60)
        lbl_duration = Label(self.window, text="Duration", font=("goudy old style", 15, "bold"), bg="white")
        lbl_duration.place(x=10, y=100)
        lbl_Charge = Label(self.window, text="Charges", font=("goudy old style", 15, "bold"), bg="white")
        lbl_Charge.place(x=10, y=140)
        lbl_Description = Label(self.window, text="Description", font=("goudy old style", 15, "bold"), bg="white")
        lbl_Description.place(x=10, y=180)

        #   ENTRY

        self.txt_CourseName = Entry(self.window, textvariable=self.var_course, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_CourseName.place(x=150, y=60, width=200)
        self.txt_duration = Entry(self.window, textvariable=self.var_duration, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_duration.place(x=150, y=100, width=200)
        self.txt_Charge = Entry(self.window, textvariable=self.var_charges, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_Charge.place(x=150, y=140, width=200)
        self.txt_Description = Text(self.window, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_Description.place(x=150, y=180, width=500, height=130)

        # BUTTON

        self.btn_add = Button(self.window, text="Save", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.add)
        self.btn_add.place(x=100, y=400)
        self.btn_update = Button(self.window, text="Update", font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2", command=self.update)
        self.btn_update.place(x=200, y=400)
        self.btn_delete = Button(self.window, text="Delete", font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2", command=self.delete)
        self.btn_delete.place(x=320, y=400)
        self.btn_clear = Button(self.window, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=440, y=400)

        #   HOME BUTTON

        self.btn_hom = Button(self.window, text="Home", font=("goudy old style", 15, "bold"), bg="#FDFF5A",cursor="hand2", command=self.os)
        self.btn_hom.place(x=550, y=400)

        lbl_Search_coursename = Label(self.window, text="Course Name", font=("goudy old style", 15, "bold"), bg="white")
        lbl_Search_coursename.place(x=720, y=60)
        self.txt_search_CourseName = Entry(self.window, textvariable=self.var_search, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_search_CourseName.place(x=850, y=60, width=180)
        lbl_Search = Button(self.window, text="Search", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2", command=self.search)
        lbl_Search.place(x=1070, y=60, width=120, height=28)

        #   FRAME DECLERATION

        self.C_Frame = Frame(self.window, bd=2, relief="ridge")
        self.C_Frame.place(x=720, y=100, width=470, height=340)
        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        self.Coursetable = ttk.Treeview(self.C_Frame, columns=("Cid", "name", "duration", "charges", "description"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        self.Coursetable.heading("Cid", text="Course ID")
        self.Coursetable.heading("name", text="Course Name")
        self.Coursetable.heading("duration", text="Duration")
        self.Coursetable.heading("charges", text="Charges")
        self.Coursetable.heading("description", text="Description")
        self.Coursetable["show"] = 'headings'

        self.Coursetable.column("Cid", width=90)
        self.Coursetable.column("name", width=100)
        self.Coursetable.column("duration", width=100)
        self.Coursetable.column("charges", width=100)
        self.Coursetable.column("description", width=150)
        self.Coursetable.pack(fill=BOTH, expand=1)
        self.Coursetable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    def os(self):
        op=messagebox.askyesno("Confirm","Do you really want to go Home?",parent=self.window)
        if op==True:
            self.window.destroy()
            os.system("python data.py")
    def get_data(self, ev): #   ev -->Enviroment vatiable

        r = self.Coursetable.focus()
        content = self.Coursetable.item(r)
        row = content["values"]
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        self.txt_Description.delete("1.0", END)
        self.txt_Description.insert(END, row[4])

    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.window)
            else:
                cur.execute("select * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", "Course Name already exists", parent=self.window)
                else:
                    cur.execute("INSERT INTO course (name, duration, charges, description) VALUES (?, ?, ?, ?)",
                                (
                                    self.var_course.get(),
                                    self.var_duration.get(),
                                    self.var_charges.get(),
                                    self.txt_Description.get('1.0', END).strip()
                                ))
                    con.commit()
                    messagebox.showinfo("Success", "Course added successfully", parent=self.window)
                    self.show()
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
            course_id = values[0]
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.window)
            else:
                cur.execute("UPDATE course SET name=?, duration=?, charges=?, description=? WHERE Cid=?",
                            (
                                self.var_course.get(),
                                self.var_duration.get(),
                                self.var_charges.get(),
                                self.txt_Description.get('1.0', END).strip(),
                                course_id
                            ))
                con.commit()
                messagebox.showinfo("Success", "Course updated successfully", parent=self.window)
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
            course_id = values[0]
            if messagebox.askyesno("Confirm", "Do you really want to delete this course?", parent=self.window):
                cur.execute("DELETE FROM course WHERE Cid=?", (course_id,))
                con.commit()
                messagebox.showinfo("Success", "Course deleted successfully", parent=self.window)
                self.show()
        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.window)

    def clear(self):
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.txt_Description.delete('1.0', END)

    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course")
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
            cur.execute("SELECT * FROM course WHERE name LIKE ?", (f"%{self.var_search.get()}%",))
            rows = cur.fetchall()
            if rows:
                self.Coursetable.delete(*self.Coursetable.get_children())
                for row in rows:
                    self.Coursetable.insert('', END, values=row)
            else:
                messagebox.showinfo("Info", "No record found", parent=self.window)
        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

#   GUI RUN SECTION

if __name__ == "__main__":
    window = Tk()
    obj = CourseClass(window)
    window.mainloop()
