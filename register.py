from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os
class Register:
    def __init__(self, window):
        self.window = window
        self.window.title("Registration Window")
        self.window.geometry("1920x1080+0+0")

        #   IMAGE

        self.bg = ImageTk.PhotoImage(file="image/b2.jpg")
        bg = Label(self.window, image=self.bg)
        bg.place(x=250, y=0, relheight=1)

        #   REGESTER IMAGE

        self.lable_imag = Image.open("image/reg.gif",)
        self.lable1_imag = self.lable_imag.resize((500,495))
        self.lable2_imag = ImageTk.PhotoImage(self.lable1_imag)
        self.lable3_imag = Label(self.window, image=self.lable2_imag,bd=2,background="#FFE15C")
        self.lable3_imag.place(x=50, y=100)

        #   FRAM FOR DTAT ENTRY

        frame1 = Frame(self.window, bg="white")
        frame1.place(x=554, y=100, width=699, height=499)#x=450, y=100, width=700, height=502

        #   TITLE

        title = Label(frame1, text="REGISTER HERE", font=("times new roman", 20, "bold"), bg="white", fg="green")
        title.place(x=50, y=30)

        #   VARIABLE DECLEARATION

        self.first_name = StringVar()
        self.last_name = StringVar()
        self.contact_no = StringVar()
        self.email_no = StringVar()
        self.pass_no = StringVar()
        self.conf_passwo = StringVar()
        self.ans = StringVar()
        self.combo = StringVar()
        self.conform = StringVar()

        #   LABEL AND ENTRY FRAME

        f_name = Label(frame1, text="First name", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        f_name.place(x=50, y=100)
        text_f_name = Entry(frame1, textvariable=self.first_name, font=("times new roman", 15, "bold"), bd=2, bg="lightgray")
        text_f_name.place(x=50, y=130)

        l_name = Label(frame1, text="Last name", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        l_name.place(x=300, y=100)
        text_l_name = Entry(frame1, textvariable=self.last_name, font=("times new roman", 15, "bold"), bd=2, bg="lightgray")
        text_l_name.place(x=300, y=130)

        c_name = Label(frame1, text="Contact No.", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        c_name.place(x=50, y=180)
        text_c_name = Entry(frame1, textvariable=self.contact_no, font=("times new roman", 15, "bold"), bd=2, bg="lightgray")
        text_c_name.place(x=50, y=210)

        e_name = Label(frame1, text="Email", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        e_name.place(x=300, y=180)
        text_e_name = Entry(frame1, textvariable=self.email_no, font=("times new roman", 15, "bold"), bd=2, bg="lightgray")
        text_e_name.place(x=300, y=210)

        S_name = Label(frame1, text="Answer", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        S_name.place(x=300, y=260)
        text_S_name = Entry(frame1, textvariable=self.ans, font=("times new roman", 15, "bold"), bd=2, bg="lightgray")
        text_S_name.place(x=300, y=290)

        combo_box = Label(frame1, text="Security Question", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        combo_box.place(x=20, y=260, width=210)
        self.combo_box_t = ttk.Combobox(frame1, textvariable=self.combo, font=("times new roman", 15, "bold"), state='readonly', justify="center")
        self.combo_box_t['values'] = ("select", "your first pet", "your birth place","Your favourite food","your favourite person")
        self.combo_box_t.current(0)
        self.combo_box_t.place(x=50, y=290)

        password = Label(frame1, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        password.place(x=50, y=330)
        self.password = Entry(frame1, show="*", textvariable=self.pass_no, font=("times new roman", 15, "bold"), bd=2, bg="lightgray")
        self.password.place(x=50, y=360)

        conform_pass = Label(frame1, text="Conform Password", font=("times new roman", 15, "bold"), bg="white", fg="gray")
        conform_pass.place(x=300, y=330)
        self.conform_pass = Entry(frame1, show="*", textvariable=self.conf_passwo, font=("times new roman", 15, "bold"), bd=2, bg="lightgray")
        self.conform_pass.place(x=300, y=360)

        #   CHECK BUTTON

        self.var_chk = IntVar() #GIVE INTERGER VARIABLE FORM CHECK BUTTON
        chkbox = Checkbutton(frame1, text="I Agree The Terms & Conditions", bg="white", activebackground="white",variable=self.var_chk, onvalue=1, offvalue=0, cursor="hand2")
        chkbox.place(x=50, y=415)

        #   REGESTER BUTTON AS IMAGE

        self.btn_img = ImageTk.PhotoImage(file="image/register.png")
        btn = Button(frame1, image=self.btn_img, cursor="hand2", command=self.register_data)
        btn.place(x=50, y=450)

        #   LOGIN BUTTON

        btn = Button(self.window, text="Sign In", font=("times new roman", 15, "bold"), bd=2, cursor="hand2",command=self.login,bg="#528DFF",fg="white",relief="ridge")
        btn.place(x=250, y=460, width=100)#x=85 y=460 width=150
    def login(self):
        self.window.destroy()
        os.system("python login.py")

    def register_data(self):
        if (self.first_name.get() == "" or self.email_no.get() == "" or self.contact_no.get() == "" or
                self.combo.get() == "select" or self.ans.get() == "" or self.pass_no.get() == "" or
                self.pass_no.get() == "" or self.conf_passwo.get() == ""):
            messagebox.showerror("Error", "All Fields are required!", parent=self.window)
        elif self.pass_no.get() != self.conf_passwo.get():
            messagebox.showerror("Error", "Conform password should be same", parent=self.window)
        elif self.var_chk.get() == 0:
            messagebox.showerror("Error", "Please Agree our terms & condition", parent=self.window)
        elif not self.email_no.get().endswith("@gmail.com"):
            messagebox.showerror("Error", "Please enter a valid Gmail address", parent=self.window)
        else:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM employee WHERE email=?", (self.email_no.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", "User already exists. Please enter properly", parent=self.window)
                else:
                    cur.execute(
                        "INSERT INTO employee (f_name,l_name,contact,email,question,answer,password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (self.first_name.get(), self.last_name.get(), self.contact_no.get(),
                         self.email_no.get(), self.combo.get(), self.ans.get(), self.pass_no.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Detail added successfully", parent=self.window)
                    self.window.destroy()
                    os.system("python login.py")
            except Exception as es:
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.window)

#   GUI RUN SECTION

if __name__ == "__main__":
    window = Tk()
    obj = Register(window)
    window.mainloop()

