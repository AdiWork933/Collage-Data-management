import sqlite3
import os
from tkinter import Tk, Label, Entry, Button, messagebox, StringVar, OptionMenu, IntVar, Checkbutton

class PasswordResetApp:
    def __init__(self, master):
        self.window = master
        self.window.title("Main Window")
        self.window.geometry("400x200")

        self.reset_button = Button(self.window, text="Forget Password", command=self.forget_password)
        self.reset_button.pack(pady=30)

        self.login_button = Button(self.window, text="Back to Login", command=self.go)
        self.login_button.pack(pady=40)

    def go(self):
        self.window.destroy()
        os.system("python login.py")

    def forget_password(self):
        # Destroy the current window
        self.window.destroy()

        # Open a new window for email input
        email_window = Tk()
        email_window.title("Forget Password")
        email_window.geometry("500x200")
        email_window.config(bg="#021e2f")

        Label(email_window, text="Enter your email:", bg="#021e2f", fg="white").pack(pady=10)
        email_entry = Entry(email_window)
        email_entry.pack(pady=5)

        Button(email_window, text="Submit",
               command=lambda: self.display_security_question(email_window, email_entry.get())).pack(pady=20)

    def display_security_question(self, email_window, email):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT question, answer FROM employee WHERE email = ?", (email,))
            row = cur.fetchone()

            if row:
                email_window.destroy()

                # Extracting question and answer from the database
                question = row[0]
                current_answer = row[1]

                # Open a new window for password and security question reset
                reset_window = Tk()
                reset_window.title("Reset Password and Security Question")
                reset_window.geometry("500x500")
                reset_window.config(bg="#021e2f")

                Label(reset_window, text="Current Security Question:", bg="#021e2f", fg="white").pack(pady=10)

                # Fetch distinct security questions from the database
                cur.execute("SELECT DISTINCT question FROM employee")
                questions = [q[0] for q in cur.fetchall()]

                # Dropdown menu for current security question
                question_var = StringVar(reset_window)
                question_var.set(question)  # set the default option to the user's current question
                question_menu = OptionMenu(reset_window, question_var, *questions)
                question_menu.pack(pady=5)

                Label(reset_window, text="Answer:", bg="#021e2f", fg="white").pack(pady=10)
                answer_entry = Entry(reset_window)
                answer_entry.pack(pady=5)

                Label(reset_window, text="New Password:", bg="#021e2f", fg="white").pack(pady=10)
                new_password_entry = Entry(reset_window, show="*")
                new_password_entry.pack(pady=5)

                # Checkbox to indicate if user wants to change security question and answer
                change_question_var = IntVar()
                change_question_check = Checkbutton(reset_window, text="Change Security Question and Answer",
                                                    variable=change_question_var, bg="#021e2f", fg="white")
                change_question_check.pack(pady=10)

                # New Security Question and Answer fields
                new_question_label = Label(reset_window, text="New Security Question:", bg="#021e2f", fg="white")
                new_question_label.pack(pady=5)

                # Dropdown menu for new security question
                new_question_var = StringVar(reset_window)
                new_question_menu = OptionMenu(reset_window, new_question_var, *questions)
                new_question_menu.pack(pady=5)

                new_answer_label = Label(reset_window, text="New Answer:", bg="#021e2f", fg="white")
                new_answer_label.pack(pady=5)
                new_answer_entry = Entry(reset_window)
                new_answer_entry.pack(pady=5)

                Button(reset_window, text="Submit",
                       command=lambda: self.submit_reset(email, question_var.get(), answer_entry.get(),
                                                        new_password_entry.get(),
                                                        change_question_var.get(),
                                                        new_question_var.get(), new_answer_entry.get(),
                                                        reset_window)).pack(pady=20)
            else:
                messagebox.showerror("Error", "Email not found.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            con.close()

    def submit_reset(self, email, old_question, answer, new_password, change_question, new_question, new_answer,
                     reset_window):
        if not answer or not new_password:
            messagebox.showerror("Error", "Answer and New Password are required.")
            return

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        try:
            if change_question:
                if not new_question or not new_answer:
                    messagebox.showerror("Error", "New Security Question and Answer are required.")
                    return

                # Update password, security question, and answer
                cur.execute("UPDATE employee SET password = ?, question = ?, answer = ? WHERE email = ?",
                            (new_password, new_question, new_answer, email))
            else:
                # Update password and optionally update the answer
                cur.execute("UPDATE employee SET password = ?, answer = ? WHERE email = ?",
                            (new_password, answer, email))

            con.commit()
            messagebox.showinfo("Password and Question Reset", "Password and Security Question have been reset successfully.")
            reset_window.destroy()  # Close the reset window after successful update
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    app = PasswordResetApp(root)
    root.mainloop()
