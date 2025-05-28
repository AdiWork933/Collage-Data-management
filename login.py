from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os

class Login_page:
    def __init__(self, window):
        self.window = window
        self.window.title("Login Page")
        self.window.geometry("1920x1080+0+0")
        self.window.config(bg="#021e2f")

        #   BG COLOR

        self.left = Label(self.window, bg="#08A3D2", bd=0)
        self.left.place(x=0, y=0, height=800, width=600)

        #   VARIABLE DECLERATION

        self.email = StringVar()
        self.password = StringVar()

        #   LOGIN FRAME

        login_frame = Frame(self.window, bg="white")
        login_frame.place(x=300, y=250, width=600, height=300)

        title = Label(login_frame, text="Login", font=("goudy old style", 30, "bold"), bg="#033054", fg="white")
        title.place(x=10, y=15, width=280, height=40)

        btn_eml = Label(login_frame, text="Email", font=("goudy old style", 25, "bold"), bg="white")
        btn_eml.place(x=30, y=70)
        eml_entry = Entry(login_frame, textvariable=self.email, font=("goudy old style", 20), bd=4)
        eml_entry.place(x=30, y=110, width=250)

        btn_update = Label(login_frame, text="Password", font=("goudy old style", 25, "bold"), bg="white")
        btn_update.place(x=30, y=150)
        password_entry = Entry(login_frame, textvariable=self.password, show="*", font=("goudy old style", 20), bd=4)
        password_entry.place(x=30, y=190, width=250)

        submit = Button(login_frame, text="Submit", font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2", command=self.get)
        submit.place(x=30, y=240)

        regesterbtn = Button(login_frame, text="Register", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white",cursor="hand2",command=self.REG)
        regesterbtn.place(x=130, y=240,width=90)

        regesterbtn = Button(login_frame, text="Forget password", font=("goudy old style", 10, "bold"), bg="#AC5DFF",fg="white", cursor="hand2", command=self.forget_password)
        regesterbtn.place(x=240, y=240, width=100,height=38.6)

        #   LOGIN FRAME IMAGE

        self.lable_imag = Image.open("image/welcom.png")
        self.lable1_imag = self.lable_imag.resize((200,200))
        self.lable2_imag = ImageTk.PhotoImage(self.lable1_imag)
        self.lable3_imag = Label(login_frame, image=self.lable2_imag,bd=5,background="#FFE15C")#,command=self.master
        self.lable3_imag.place(x=370, y=45)
    def master(self):
        self.window.destroy()
        os.system("python exl_data_show.py")

    #   REGESTER
    def REG(self):
        self.window.destroy()
        os.system("python register.py")

    #   VERYFICATION

    def get(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee WHERE email=?", (self.email.get(),))
            row = cur.fetchone()
            if row:
                if self.password.get() == row[7]:  # Assuming password is at index 6 in your database
                    self.window.destroy()
                    os.system("python data.py")
                else:
                    messagebox.showinfo("Info", "Incorrect password", parent=self.window)
            else:
                messagebox.showinfo("Info", "No record found ", parent=self.window)
                self.email.set("")
                self.password.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()
    def forget_password(self):
        self.window.destroy()
        os.system("python reset_password.py")


if __name__ == "__main__":
    window = Tk()
    obj = Login_page(window)
    window.mainloop()