from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os


class ResultClass:
    def __init__(self, window):
        self.window = window
        self.window.title("Student Result Management System")
        self.window.geometry("1200x480+80+170")
        self.window.config(bg="white")
        self.window.focus_force()
        self.window.resizable(False, False)

        #   TITLE

        title = Label(self.window, text="Add Student Result", font=("goudy ols style", 20, "bold"), bg="orange",fg="#262626")
        title.place(x=10, y=15, width=1180, height=50)

        #   VARIABLE DECLEARATION

        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.CA1 = StringVar()
        self.CA2 = StringVar()
        self.CA3 = StringVar()
        self.CA4 = StringVar()
        self.roll_list = []
        self.fetch_roll()

        #   LABEL

        lbl_select = Label(self.window, text="Select Student", font=("goudy old style", 20, "bold"), bg="white")
        lbl_select.place(x=50, y=100)
        lbl_name = Label(self.window, text="Name", font=("goudy old style", 20, "bold"), bg="white")
        lbl_name.place(x=50, y=160)
        lbl_course = Label(self.window, text="Course", font=("goudy old style", 20, "bold"), bg="white")
        lbl_course.place(x=50, y=220)
        lbl_CA1 = Label(self.window, text="CA1", font=("goudy old style", 20, "bold"), bg="white")
        lbl_CA1.place(x=50, y=280)
        lbl_CA2 = Label(self.window, text="CA2", font=("goudy old style", 20, "bold"), bg="white")
        lbl_CA2.place(x=350, y=280)
        lbl_CA3 = Label(self.window, text="CA3", font=("goudy old style", 20, "bold"), bg="white")
        lbl_CA3.place(x=50, y=340)
        lbl_CA4 = Label(self.window, text="CA4", font=("goudy old style", 20, "bold"), bg="white")
        lbl_CA4.place(x=350, y=340)

        #   COMBO BOX

        self.txt_student = ttk.Combobox(self.window, textvariable=self.var_roll, values=self.roll_list,font=("goudy old style", 20, "bold"), state='readonly', justify="center")
        self.txt_student.place(x=280, y=100, width=150)
        self.txt_student.set("Select")

        #   SEARCH BUTTON

        lbl_search = Button(self.window, text="Search", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white",cursor="hand2", command=self.search)
        lbl_search.place(x=480, y=100, width=120, height=35)

        #   ENTRY FILD

        self.txt_name = Entry(self.window, textvariable=self.var_name, font=("goudy old style", 20, "bold"),state="readonly", bg="lightyellow")
        self.txt_name.place(x=280, y=160, width=320)
        self.txt_course = Entry(self.window, textvariable=self.var_course, font=("goudy old style", 20, "bold"),state="readonly", bg="lightyellow")
        self.txt_course.place(x=280, y=220, width=320)
        self.CA1_entry = Entry(self.window, textvariable=self.CA1, font=("goudy old style", 20, "bold"),bg="lightyellow")
        self.CA1_entry.place(x=180, y=280, width=150)
        self.CA2_entry = Entry(self.window, textvariable=self.CA2, font=("goudy old style", 20, "bold"),bg="lightyellow")
        self.CA2_entry.place(x=460, y=280, width=150)
        self.CA3_entry = Entry(self.window, textvariable=self.CA3, font=("goudy old style", 20, "bold"),bg="lightyellow")
        self.CA3_entry.place(x=180, y=340, width=150)
        self.CA4_entry = Entry(self.window, textvariable=self.CA4, font=("goudy old style", 20, "bold"),bg="lightyellow")
        self.CA4_entry.place(x=460, y=340, width=150)

        #   BUTTONS

        self.btn_submit = Button(self.window, text="Submit", font=("goudy old style", 20, "bold"), bg="lightgreen",activebackground="lightgreen", cursor="hand2", command=self.add)
        self.btn_submit.place(x=50, y=420, width=120, height=35)
        self.btn_clear = Button(self.window, text="Clear", font=("goudy old style", 20, "bold"), bg="lightgray",activebackground="lightgray", cursor="hand2", command=self.clear_fields)
        self.btn_clear.place(x=350, y=420, width=120, height=35)
        self.btn_update = Button(self.window, text="Update", font=("goudy old style", 20, "bold"), bg="#4caf50",cursor="hand2", command=self.update_result)
        self.btn_update.place(x=200, y=420, width=120, height=35)
        self.btn_home = Button(self.window, text="Home", font=("goudy old style", 20, "bold"), bg="#FDFF5A",cursor="hand2", command=self.go_home)
        self.btn_home.place(x=500, y=420, width=120, height=35)

        #   IMAGE

        self.label_image = Image.open("image/result.jpg")
        self.label_image_resized = self.label_image.resize((500, 300))
        self.label_image_tk = ImageTk.PhotoImage(self.label_image_resized)
        self.label_image_widget = Label(self.window, image=self.label_image_tk)
        self.label_image_widget.place(x=630, y=100)

    def fetch_roll(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT roll FROM student")
            rows = cur.fetchall()
            self.roll_list = [row[0] for row in rows]
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching roll numbers: {str(e)}")
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name, course FROM student WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if row:
                self.var_name.set(row[0])
                self.var_course.set(row[1])

                # Fetching the saved results
                cur.execute("SELECT CA1, CA2, CA3, CA4 FROM result WHERE roll=?", (self.var_roll.get(),))
                result_row = cur.fetchone()
                if result_row:
                    self.CA1.set(result_row[0])
                    self.CA2.set(result_row[1])
                    self.CA3.set(result_row[2])
                    self.CA4.set(result_row[3])
                else:
                    self.CA1.set("")
                    self.CA2.set("")
                    self.CA3.set("")
                    self.CA4.set("")
            else:
                messagebox.showinfo("Info", "No record found", parent=self.window)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error searching student: {str(e)}")
        finally:
            con.close()

    def add(self):
        if not self.var_name.get():
            messagebox.showerror("Error", "Please first search for student name", parent=self.window)
            return

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM result WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if row:
                messagebox.showerror("Error", "Result already present", parent=self.window)
            else:
                cur.execute("INSERT INTO result (roll, name, course, CA1, CA2, CA3, CA4) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (self.var_roll.get(),
                             self.var_name.get(),
                             self.var_course.get(),
                             self.CA1.get(),
                             self.CA2.get(),
                             self.CA3.get(),
                             self.CA4.get()))
                con.commit()
                messagebox.showinfo("Success", "Result added successfully", parent=self.window)
                self.clear_fields()
                self.fetch_roll()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {str(e)}", parent=self.window)
        finally:
            con.close()

    def clear_fields(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_course.set("")
        self.CA1.set("")
        self.CA2.set("")
        self.CA3.set("")
        self.CA4.set("")

    def update_result(self):
        if not self.var_name.get():
            messagebox.showerror("Error", "Please first search for student name", parent=self.window)
            return

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("UPDATE result SET CA1=?, CA2=?, CA3=?, CA4=? WHERE roll=?",
                        (self.CA1.get(), self.CA2.get(), self.CA3.get(), self.CA4.get(), self.var_roll.get()))
            con.commit()
            messagebox.showinfo("Success", "Result updated successfully", parent=self.window)
            self.clear_fields()
            self.fetch_roll()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {str(e)}", parent=self.window)
        finally:
            con.close()

    def go_home(self):
        if messagebox.askyesno("Confirm", "Do you really want to go Home?", parent=self.window):
            self.window.destroy()
            os.system("python data.py")

    def display_results(self):
        self.tree.delete(*self.tree.get_children())
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM result")
            rows = cur.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error displaying results: {str(e)}")
        finally:
            con.close()

#   GUI RUN SECTION

if __name__ == "__main__":
    window = Tk()
    obj = ResultClass(window)
    window.mainloop()
