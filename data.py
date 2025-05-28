from tkinter import *
from PIL import Image, ImageTk
import os
import sqlite3
from tkinter import messagebox

class RMS:
    def __init__(self, window):
        self.window=window
        self.window.title("Student Result Management System")
        self.window.geometry("1920x780+0+0")
        self.window.config(bg="white")
        #   LOGO 1

        self.logo_dash = ImageTk.PhotoImage(file="image/logo_p.png")

        #   LOGO 2

        #self.logo_dash = ImageTk.PhotoImage(file="D:\\studennt_data\\logo-50.jpg")

        #   TITLE

        title = Label(self.window, text="Student Result Management System", padx=10, compound=LEFT,
                      image=self.logo_dash, font=("goudy ols style", 20, "bold"), bg="#033054", fg="white")
        title.place(x=0, y=0, relwidth=1, height=50,)

        M_Fram = LabelFrame(self.window, text="Menu", font=("times new roman", 15,"bold"), bg="white")
        M_Fram.place(x=10, y=70, width=1520, height=80)
        btn_course = Button(M_Fram, text="Course", font=("goudy old style", 15, "bold"), bg="#0b5277", fg="white",cursor="hand2", command=self.course)
        btn_course.place(x=20, y=5, width=200, height=40)
        btn_student = Button(M_Fram, text="Student", font=("goudy old style", 15, "bold"), bg="#0b5277", fg="white", cursor="hand2", command=self.student)
        btn_student.place(x=270, y=5, width=200, height=40)
        btn_result = Button(M_Fram, text="Result", font=("goudy old style", 15, "bold"), bg="#0b5277", fg="white",cursor="hand2", command=self.result)
        btn_result.place(x=540, y=5, width=200, height=40)
        btn_view = Button(M_Fram, text="View Student Results", font=("goudy old style", 15, "bold"), bg="#0b5277",fg="white", cursor="hand2", command=self.view_result)
        btn_view.place(x=800, y=5, width=210, height=40)
        btn_logout = Button(M_Fram, text="Logout", font=("goudy old style", 15, "bold"), bg="#0b5277", fg="white",cursor="hand2",command=self.logout)
        btn_logout.place(x=1080, y=5, width=200, height=40)
        btn_exit = Button(M_Fram, text="Exit", font=("goudy old style", 15, "bold"), bg="#0b5277", fg="white",cursor="hand2",command=self.Exit)
        btn_exit.place(x=1350, y=5, width=150, height=40)

        M_Fram2 = LabelFrame(self.window, text="Tools", font=("times new roman", 15,"bold"), bg="white")
        M_Fram2.place(x=10, y=150, width=260, height=580)

        btn_performance = Button(M_Fram2, text="Performance", font=("goudy old style", 15, "bold"), bg="#0b5277", fg="white",cursor="hand2",command=self.performance)
        btn_performance.place(x=25, y=20, width=200, height=50)

        #   BODY IMAGE SECTION
        self.lable_imag = Image.open("image/bg.png")
        self.lable1_imag = self.lable_imag.resize((920, 450))
        self.lable2_imag = ImageTk.PhotoImage(self.lable1_imag)
        self.lable3_imag = Label(self.window, image=self.lable2_imag)
        self.lable3_imag.place(x=400, y=180, width=920, height=350)

        #   BESIC DETAI SECTION

        self.student = Label(self.window, text="Total Student\n[0]", font=("goudy old style", 20), bd=10,relief="ridge", bg="#e43b06", fg="white")
        self.student.place(x=400, y=530, width=250, height=100)
        self.lbl_course = Label(self.window, text="Total Course\n[0]", font=("goudy old style", 20), bd=10, relief="ridge",bg="#0676ad", fg="white")
        self.lbl_course.place(x=740, y=530, width=250, height=100)
        self.lbl_result = Label(self.window, text="Total Result\n[0]", font=("goudy old style", 20), bd=10,relief="ridge", bg="#038074", fg="white")
        self.lbl_result.place(x=1070, y=530, width=250, height=100)

        #   AUTO FILE SECTION

        self.fetch_course()
        self.fetch_result()
        self.fetch_student()

        #   BASE TEXT
        footer = Label(self.window,text="SRMS-Student Result Management System \n Contact us for Techinical issue : 9839xxxx61",font=("goudy ols style", 15), bg="#262626", fg="white")
        footer.pack(side=BOTTOM, fill=X)

    #   OPEN AND DESTRY FILE SECTION
    def course(self):
        self.window.destroy()
        os.system("python course.py")
    def student(self):
        self.window.destroy()
        os.system("python student.py")
    def result(self):
        self.window.destroy()
        os.system("python result.py")
    def view_result(self):
        self.window.destroy()
        os.system("python report.py")
    def performance(self):
        self.window.destroy()
        os.system("python performance.py")

    #   FETCH DATA SECTION
    def fetch_course(self):
        self.length = 0
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()
            self.length = len(rows)
            self.lbl_course.config(text=f"Total Course\n{self.length}")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()
    def fetch_result(self):
        self.length = 0
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM student")
            rows = cur.fetchall()
            self.length = len(rows)
            self.lbl_result.config(text=f"Total Result\n{self.length}")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()
    def fetch_student(self):
        self.length = 0
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM student")
            rows = cur.fetchall()
            self.length = len(rows)
            self.student.config(text=f"Total Student\n{self.length}")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

   #    LOGOUT AND EXIT SECTION

    def logout(self):
        op=messagebox.askyesno("Confirm","Do you really want to logout ?",parent=self.window)
        if op==True:
            self.window.destroy()
            os.system("python login.py")
    def Exit(self):
        op=messagebox.askyesno("confirm","Do you really want to Exit",parent=self.window)
        if op==True:
            self.window.destroy()

#   GUI RUN SECTION

if __name__ == "__main__":
    window = Tk()
    obj = RMS(window)
    window.mainloop()
