from tkinter import *
from tkinter import ttk, messagebox
import numpy as np
import sqlite3
import pickle
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class ResultClass:
    def __init__(self, window):
        self.window = window
        self.window.title("Student Performance Prediction")
        self.window.geometry("1200x600+80+170")
        self.window.config(bg="white")
        self.window.focus_force()

        # Disable window resizing
        self.window.resizable(False, False)

        # Load the model, scaler, and encoder
        with open('CA_Marks_Prediction.pkl', 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.encoder = data['encoder']

        # Variables
        self.var_roll = StringVar()
        self.var_phone = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_prediction = StringVar()

        # Title
        title = Label(self.window, text="Student Performance Prediction", font=("goudy old style", 20, "bold"), bg="orange", fg="#262626")
        title.place(x=10, y=15, width=1180, height=50)

        # Input Fields
        lbl_roll = Label(self.window, text="Roll Number:", font=("goudy old style", 18, "bold"), bg="white")
        lbl_roll.place(x=50, y=100)
        Entry(self.window, textvariable=self.var_roll, font=("goudy old style", 18), bg="lightyellow").place(x=250, y=100, width=200)

        lbl_phone = Label(self.window, text="Phone Number:", font=("goudy old style", 18, "bold"), bg="white")
        lbl_phone.place(x=50, y=150)
        Entry(self.window, textvariable=self.var_phone, font=("goudy old style", 18), bg="lightyellow").place(x=250, y=150, width=200)

        # Predict Button
        btn_predict = Button(self.window, text="Submit", font=("goudy old style", 18, "bold"), bg="#03a9f4", fg="white", cursor="hand2", command=self.on_predict)
        btn_predict.place(x=500, y=125, width=100, height=35)

        # Result Labels
        self.lbl_name = Label(self.window, text="Student Name:", font=("goudy old style", 18, "bold"), bg="white")
        self.lbl_name.place(x=50, y=220)
        self.lbl_course = Label(self.window, text="Course:", font=("goudy old style", 18, "bold"), bg="white")
        self.lbl_course.place(x=50, y=270)
        self.lbl_prediction = Label(self.window, text="Predicted Performance:", font=("goudy old style", 18, "bold"), bg="white")
        self.lbl_prediction.place(x=50, y=320)
        
        self.btn_home = Button(self.window, text="Home", font=("goudy old style", 20, "bold"), bg="#FDFF5A",cursor="hand2", command=self.go_home)
        self.btn_home.place(x=100, y=420, width=120, height=35)

        self.btn_home = Button(self.window, text="clear", font=("goudy old style", 20, "bold"), bg="#FDFF5A",cursor="hand2", command=self.clear)
        self.btn_home.place(x=250, y=420, width=120, height=35)
        # Chart Frame
        self.frame_chart = Frame(self.window, bg="white")
        self.frame_chart.place(x=600, y=100, width=550, height=400)

    # Database Connection Function
    def clear(self):
        self.var_roll.set("")
        self.var_phone.set("")
    def go_home(self):
        if messagebox.askyesno("Confirm", "Do you really want to go Home?", parent=self.window):
            self.window.destroy()
            os.system("python main_page.py")

    def get_student_data(self, roll, phone):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT student.name, student.course, result.CA1, result.CA2, result.CA3, result.CA4 
                FROM student 
                JOIN result ON student.roll = result.roll 
                WHERE student.roll = ? AND student.contact = ?
            """, (roll, phone))
            result = cur.fetchone()
            if result:
                student_name = result[0]
                course = result[1]
                ca_scores = [float(result[2]), float(result[3]), float(result[4]), float(result[5])]
                return student_name, course, ca_scores
            else:
                return None, None, None
        except sqlite3.Error as e:
            print("Database error:", e)
            return None, None, None
        finally:
            con.close()

    # Prediction Function
    def predict_performance(self, ca_scores):
        input_data = self.scaler.transform([ca_scores])
        prediction = self.model.predict(input_data)
        predicted_label = self.encoder.inverse_transform(prediction)
        return predicted_label[0]

    # Predict Button Callback
    def on_predict(self):
        roll = self.var_roll.get()
        phone = self.var_phone.get()
        student_name, course, ca_scores = self.get_student_data(roll, phone)
        if student_name and course and ca_scores:
            result = self.predict_performance(ca_scores)
            self.lbl_name.config(text=f"Student Name: {student_name}")
            self.lbl_course.config(text=f"Course: {course}")
            self.lbl_prediction.config(text=f"Predicted Performance: {result}")
            self.plot_performance(ca_scores)
        else:
            messagebox.showerror("Error", "Invalid roll number or phone number, or CA scores not found.")

    # Plotting Function
    def plot_performance(self, ca_scores):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ca_labels = ['CA1', 'CA2', 'CA3', 'CA4']
        ax.plot(ca_labels, ca_scores, marker='o')
        ax.set_title("Performance Scores")
        ax.set_xlabel("CA Tests")
        ax.set_ylabel("Scores")
        
        for widget in self.frame_chart.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

# GUI Run Section
if __name__ == "__main__":
    window = Tk()
    obj = ResultClass(window)
    window.mainloop()
