import sqlite3
from tkinter import Tk, Label, Entry, Button, ttk, messagebox
import os

class MasterApp:
    def __init__(self, master):
        self.window = master
        self.window.title("All Data Details")
        self.window.geometry("1920x1019+0+0")

        # Login Section
        login_frame = ttk.LabelFrame(self.window, text="Login")
        login_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        Label(login_frame, text="Email").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.email_entry = Entry(login_frame)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(login_frame, text="Security Question").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.question_var = ttk.Combobox(login_frame, values=self.fetch_security_questions())
        self.question_var.grid(row=1, column=1, padx=5, pady=5)

        Label(login_frame, text="Answer").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.answer_entry = Entry(login_frame)
        self.answer_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(login_frame, text="Password").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = Entry(login_frame, show="*")
        self.password_entry.grid(row=3, column=1, padx=5, pady=5)

        Button(login_frame, text="Login", command=self.login).grid(row=4, column=0, columnspan=2, pady=10)
        Button(login_frame, text="Exit", font=("goudy old style", 15, "bold"), fg="red", command=self.exit).grid(row=5, column=0, columnspan=2, pady=10)

        # Notebook (tabbed view) to display data
        self.notebook = ttk.Notebook(self.window)
        self.notebook.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.window.rowconfigure(1, weight=1)
        self.window.columnconfigure(0, weight=1)

    def exit(self):
        self.window.destroy()
        os.system("python login.py")

    def fetch_security_questions(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT DISTINCT question FROM employee")
            questions = cur.fetchall()
            return [q[0] for q in questions]
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
            return []
        finally:
            con.close()

    def login(self):
        email = self.email_entry.get()
        question = self.question_var.get()
        answer = self.answer_entry.get()
        password = self.password_entry.get()

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM employee WHERE email = ?", (email,))
            row = cur.fetchone()

            if row and row[5] == question and row[6] == answer and row[7] == password:
                messagebox.showinfo("Login Successful", "You have successfully logged in!")
                self.clear_login_data()
                self.show_all_data()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            con.close()

    def show_all_data(self):
        tables = ["course", "student", "result", "employee"]

        for table in tables:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()

            try:
                cur.execute(f"SELECT * FROM {table}")
                columns = [desc[0] for desc in cur.description]
                data = cur.fetchall()

                # Create a new frame for each table data in the notebook
                frame = ttk.Frame(self.notebook)
                self.notebook.add(frame, text=f"{table.capitalize()}")

                # Create treeview for table data with scrollbars
                self.create_treeview(frame, columns, data, table)

            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")
            finally:
                con.close()

    def create_treeview(self, parent, columns, data, table):
        tree = ttk.Treeview(parent, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')

        for row in data:
            tree.insert('', 'end', values=row)

        h_scroll = ttk.Scrollbar(parent, orient='horizontal', command=tree.xview)
        v_scroll = ttk.Scrollbar(parent, orient='vertical', command=tree.yview)
        tree.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        tree.pack(expand=True, fill='both')
        h_scroll.pack(side='bottom', fill='x')
        v_scroll.pack(side='right', fill='y')

        # Add update and delete functionality if the table is employee
        if table == "employee":
            self.create_employee_management(parent, tree)

    def create_employee_management(self, parent, tree):
        # Entry fields for updating employee details
        update_frame = ttk.LabelFrame(parent, text="Manage Employee")
        update_frame.pack(side='left', padx=10, pady=10, fill='y')

        self.update_entries = {}
        fields = ["f_name", "l_name", "contact", "email", "question", "answer", "password"]
        for i, field in enumerate(fields):
            Label(update_frame, text=field.capitalize()).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = Entry(update_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.update_entries[field] = entry

        self.selected_employee = None

        # Bind the tree selection
        tree.bind("<<TreeviewSelect>>", self.on_employee_select)

        # Buttons for updating and deleting employee
        update_button = Button(update_frame, text="Update", command=self.update_employee)
        update_button.grid(row=1, column=4, padx=5, pady=5, sticky="w")

        delete_button = Button(update_frame, text="Delete", command=self.delete_employee)
        delete_button.grid(row=2, column=4, padx=5, pady=5, sticky="e")

    def on_employee_select(self, event):
        selected_item = event.widget.selection()[0]
        self.selected_employee = event.widget.item(selected_item)['values']

        # Fill the entry fields with the selected employee data
        for i, field in enumerate(self.update_entries):
            self.update_entries[field].delete(0, 'end')
            self.update_entries[field].insert(0, self.selected_employee[i + 1])

    def update_employee(self):
        if not self.selected_employee:
            messagebox.showerror("Error", "No employee selected.")
            return

        updated_data = {field: self.update_entries[field].get() for field in self.update_entries}

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
            cur.execute("""
                UPDATE employee
                SET f_name = ?, l_name = ?, contact = ?, email = ?, question = ?, answer = ?, password = ?
                WHERE eid = ?
            """, (*updated_data.values(), self.selected_employee[0]))

            con.commit()
            messagebox.showinfo("Update Successful", "Employee details have been updated.")
            self.show_all_data()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            con.close()

    def delete_employee(self):
        if not self.selected_employee:
            messagebox.showerror("Error", "No employee selected.")
            return

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
            cur.execute("DELETE FROM employee WHERE eid = ?", (self.selected_employee[0],))
            con.commit()
            messagebox.showinfo("Delete Successful", "Employee has been deleted.")
            self.show_all_data()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            con.close()

    def clear_login_data(self):
        self.email_entry.delete(0, 'end')
        self.question_var.set('')
        self.answer_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

        # Remove existing tabs
        for tab_id in self.notebook.tabs():
            self.notebook.forget(tab_id)

if __name__ == "__main__":
    root = Tk()
    app = MasterApp(root)
    root.mainloop()