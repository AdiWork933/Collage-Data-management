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
        title = Label(self.window, text="Add Student Result", font=("goudy old style", 20, "bold"), bg="orange", fg="#262626")
        title.place(x=10, y=15, width=1180, height=50)

        #   VARIABLE DECLARATION
        self.var_dept = StringVar()
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.CA1 = StringVar()
        self.CA2 = StringVar()
        self.CA3 = StringVar()
        self.CA4 = StringVar()

        self.department_list = self.fetch_departments()
        self.roll_list = []

        #   LABELS
        Label(self.window, text="Select Department", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=80)
        Label(self.window, text="Select Student", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=130)
        Label(self.window, text="Name", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=180)
        Label(self.window, text="Course", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=230)
        Label(self.window, text="CA1", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=280)
        Label(self.window, text="CA2", font=("goudy old style", 20, "bold"), bg="white").place(x=350, y=280)
        Label(self.window, text="CA3", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=330)
        Label(self.window, text="CA4", font=("goudy old style", 20, "bold"), bg="white").place(x=350, y=330)

        #   COMBO BOXES
        self.combo_dept = ttk.Combobox(self.window, textvariable=self.var_dept, values=self.department_list,
                                       font=("goudy old style", 15), state='readonly', justify='center')
        self.combo_dept.place(x=280, y=80, width=200)
        self.combo_dept.set("Select")
        self.combo_dept.bind("<<ComboboxSelected>>", self.on_dept_select)

        self.combo_roll = ttk.Combobox(self.window, textvariable=self.var_roll,
                                       font=("goudy old style", 15), state='readonly', justify='center')
        self.combo_roll.place(x=280, y=130, width=150)
        self.combo_roll.set("Select")

        Button(self.window, text="Search", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white",
               cursor="hand2", command=self.search).place(x=480, y=130, width=120, height=35)

        #   ENTRIES
        Entry(self.window, textvariable=self.var_name, font=("goudy old style", 20, "bold"),
              state="readonly", bg="lightyellow").place(x=280, y=180, width=320)
        Entry(self.window, textvariable=self.var_course, font=("goudy old style", 20, "bold"),
              state="readonly", bg="lightyellow").place(x=280, y=230, width=320)
        Entry(self.window, textvariable=self.CA1, font=("goudy old style", 20, "bold"),
              bg="lightyellow").place(x=180, y=280, width=150)
        Entry(self.window, textvariable=self.CA2, font=("goudy old style", 20, "bold"),
              bg="lightyellow").place(x=460, y=280, width=150)
        Entry(self.window, textvariable=self.CA3, font=("goudy old style", 20, "bold"),
              bg="lightyellow").place(x=180, y=330, width=150)
        Entry(self.window, textvariable=self.CA4, font=("goudy old style", 20, "bold"),
              bg="lightyellow").place(x=460, y=330, width=150)

        #   BUTTONS
        Button(self.window, text="Submit", font=("goudy old style", 20, "bold"),
               bg="lightgreen", activebackground="lightgreen", cursor="hand2", command=self.add).place(x=50, y=390, width=120, height=35)
        Button(self.window, text="Update", font=("goudy old style", 20, "bold"),
               bg="#4caf50", cursor="hand2", command=self.update_result).place(x=200, y=390, width=120, height=35)
        Button(self.window, text="Clear", font=("goudy old style", 20, "bold"),
               bg="lightgray", activebackground="lightgray", cursor="hand2", command=self.clear_fields).place(x=350, y=390, width=120, height=35)
        Button(self.window, text="Home", font=("goudy old style", 20, "bold"),
               bg="#FDFF5A", cursor="hand2", command=self.go_home).place(x=500, y=390, width=120, height=35)

        #   IMAGE
        self.label_image = Image.open("image/result.jpg")
        self.label_image_resized = self.label_image.resize((500, 300))
        self.label_image_tk = ImageTk.PhotoImage(self.label_image_resized)
        self.label_image_widget = Label(self.window, image=self.label_image_tk)
        self.label_image_widget.place(x=630, y=100)

    def fetch_departments(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT DISTINCT course FROM student")
            departments = [row[0] for row in cur.fetchall()]
            return departments
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching departments: {e}")
            return []
        finally:
            con.close()

    def on_dept_select(self, event):
        self.roll_list.clear()
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT roll FROM student WHERE course=?", (self.var_dept.get(),))
            self.roll_list = [row[0] for row in cur.fetchall()]
            self.combo_roll.config(values=self.roll_list)
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching roll numbers: {e}")
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name, course FROM student WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if row:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
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
                messagebox.showinfo("Info", "No student record found", parent=self.window)
        except Exception as e:
            messagebox.showerror("Error", f"Search error: {e}")
        finally:
            con.close()

    def add(self):
        if not self.var_name.get():
            messagebox.showerror("Error", "Please first search for student", parent=self.window)
            return
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM result WHERE roll=?", (self.var_roll.get(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Result already present", parent=self.window)
                return
            cur.execute("INSERT INTO result (roll, name, course, CA1, CA2, CA3, CA4) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (self.var_roll.get(), self.var_name.get(), self.var_course.get(),
                         self.CA1.get(), self.CA2.get(), self.CA3.get(), self.CA4.get()))
            con.commit()
            messagebox.showinfo("Success", "Result added successfully", parent=self.window)
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Add error: {e}")
        finally:
            con.close()

    def update_result(self):
        if not self.var_name.get():
            messagebox.showerror("Error", "Please first search for student", parent=self.window)
            return
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            cur.execute("UPDATE result SET CA1=?, CA2=?, CA3=?, CA4=? WHERE roll=?",
                        (self.CA1.get(), self.CA2.get(), self.CA3.get(), self.CA4.get(), self.var_roll.get()))
            con.commit()
            messagebox.showinfo("Success", "Result updated successfully", parent=self.window)
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Update error: {e}")
        finally:
            con.close()

    def clear_fields(self):
        self.var_dept.set("Select")
        self.var_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.CA1.set("")
        self.CA2.set("")
        self.CA3.set("")
        self.CA4.set("")
        self.combo_roll.config(values=[])

    def go_home(self):
        if messagebox.askyesno("Confirm", "Do you really want to go Home?", parent=self.window):
            self.window.destroy()
            os.system("python main_page.py")


# GUI RUN
if __name__ == "__main__":
    window = Tk()
    obj = ResultClass(window)
    window.mainloop()
