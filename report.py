from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import os
class ReportClass:
    def __init__(self, window):
        self.window = window
        self.window.title("Student Result Management System")
        self.window.geometry("1350x480+80+170")
        self.window.config(bg="white")
        self.window.focus_force()

        #   TITLE

        title = Label(self.window, text="Student Result", font=("goudy old style", 30, "bold"), bg="orange",fg="#262626").place(x=10, y=15, relwidth=1, height=50)

        #   SEARCH VARIABLE DECLERATION

        self.var_search = StringVar()
        lbl_Search = Label(self.window, text="Search By Roll NO", font=("goudy old style", 15, "bold"), bg="white")
        lbl_Search.place(x=370, y=100)
        lbl_Search = Entry(self.window,textvariable=self.var_search, font=("goudy old style", 20), bg="lightyellow")
        lbl_Search.place(x=530, y=100,width=200)
        btn_Search = Button(self.window, text="Search", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white",cursor="hand2",command=self.search)
        btn_Search.place(x=750, y=100, width=120, height=35)
        btn_clear = Button(self.window, text="Clear", font=("goudy old style", 20, "bold"), bg="lightgray",activebackground="lightgray", cursor="hand2", command=self.clear_fields)
        btn_clear.place(x=410, y=420, width=120, height=35)
        btn_del = Button(self.window, text="Delete", font=("goudy old style", 20, "bold"), bg="red",activebackground="red", cursor="hand2", command=self.delete_record)
        btn_del.place(x=560, y=420, width=120, height=35)
        self.btn_hom = Button(self.window, text="Home", font=("goudy old style", 20, "bold"), bg="#FDFF5A",cursor="hand2", command=self.os)
        self.btn_hom.place(x=710, y=420, width=120, height=35)


        #   LABEL

        lbl_roll = Label(self.window, text="Roll No", font=("goudy old style", 15, "bold"), bg="white",relief="groov",bd=2).place(x=100, y=200,width=150,height=50)
        lbl_name = Label(self.window, text="Name", font=("goudy old style", 15, "bold"), bg="white",relief="groov",bd=2).place(x=250, y=200,width=250,height=50)
        lbl_course = Label(self.window, text="Course", font=("goudy old style", 15, "bold"), bg="white",relief="groov",bd=2).place(x=500,y=200,width=150,height=50)
        lbl_CA1 = Label(self.window, text="CA1", font=("goudy old style", 15, "bold"),relief="groov", bg="white",bd=2).place(x=650,y=200,width=150,height=50)
        lbl_CA2= Label(self.window, text="CA2", font=("goudy old style", 15, "bold"), bg="white",relief="groov",bd=2).place(x=800,y=200,width=150,height=50)
        lbl_CA3 = Label(self.window, text="CA3", font=("goudy old style", 15, "bold"), bg="white",relief="groov",bd=2).place(x=950, y=200,width=150,height=50)
        lbl_CA4 = Label(self.window, text="CA4", font=("goudy old style", 15, "bold"), bg="white", relief="groov",bd=2).place(x=1100, y=200, width=150, height=50)

        #   LABEL OF ANS

        self.roll = Label(self.window, font=("goudy old style", 15, "bold"), bg="white", relief="groov",bd=2)
        self.roll.place(x=100, y=250, width=150, height=50)
        self.name = Label(self.window, font=("goudy old style", 15, "bold"), bg="white", relief="groov",bd=2)
        self.name.place(x=250, y=250, width=250, height=50)
        self.course = Label(self.window, font=("goudy old style", 15, "bold"), bg="white", relief="groov",bd=2)
        self.course.place(x=500, y=250, width=150, height=50)
        self.CA1 = Label(self.window, font=("goudy old style", 15, "bold"), relief="groov",bg="white", bd=2)
        self.CA1.place(x=650, y=250, width=150, height=50)
        self.CA2 = Label(self.window, font=("goudy old style", 15, "bold"), bg="white",relief="groov", bd=2)
        self.CA2.place(x=800, y=250, width=150, height=50)
        self.CA3 = Label(self.window, font=("goudy old style", 15, "bold"), bg="white",relief="groov", bd=2)
        self.CA3.place(x=950, y=250, width=150, height=50)
        self.CA4 = Label(self.window, font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2)
        self.CA4.place(x=1100, y=250, width=150, height=50)



    def os(self):
        op=messagebox.askyesno("Confirm","Do you really want to go Home?",parent=self.window)
        if op==True:
            self.window.destroy()
            os.system("python main_page.py")
    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Roll No should be required",parent=self.window)
            cur.execute("SELECT * FROM result WHERE roll=?", (self.var_search.get(),))
            row = cur.fetchone()
            if row:
                self.roll.config(text=row[1])
                self.name.config(text=row[2])
                self.course.config(text=row[3])
                self.CA1.config(text=row[4])
                self.CA2.config(text=row[5])
                self.CA3.config(text=row[6])
                self.CA4.config(text=row[7])

            else:
                messagebox.showinfo("Info", "No record found", parent=self.window)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def clear_fields(self):
        self.roll.config(text="")
        self.name.config(text="")
        self.course.config(text="")
        self.CA1.config(text="")
        self.CA2.config(text="")
        self.CA3.config(text="")
        self.CA4.config(text="")
        self.var_search.set("")

    def delete_record(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Roll No should be required", parent=self.window)
            else:
                cur.execute("DELETE FROM result WHERE roll=?", (self.var_search.get(),))
                con.commit()
                messagebox.showinfo("Success", "Record deleted successfully", parent=self.window)
                self.clear_fields()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.window)
        finally:
            con.close()

#   GUI RUN SECTION

if __name__ == "__main__":
    window = Tk()
    obj = ReportClass(window)
    window.mainloop()
