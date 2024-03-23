import pyodbc
import random
import tkinter as tk
from tkinter import messagebox
import time as _time

conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\3rd Year\2nd Sem\Advandced Web Development\Databases\studentpy.accdb;'

def add_student_gui(conn, cursor):
    # Create a new toplevel window
    add_student_window = tk.Toplevel()

    # Set the Window Title
    add_student_window.title("Add A New Student")

    #Set the size of the window
    add_student_window.geometry("400x400")
    
    form_frame = tk.Frame(add_student_window)
    form_frame.pack()

    #Add a Label
    firstnamelabel= tk.Label(form_frame, text="First Name", font=("Roboto",14))
    firstnamelabel.grid(row = 0, column = 0, sticky= 'w')

    firstnameinput = tk.Entry(form_frame)
    firstnameinput.grid(row = 0, column = 0, sticky = 'e')  # Corrected column

    lastnamelabel= tk.Label(form_frame, text="Last Name", font=("Roboto",14))
    lastnamelabel.grid(row = 1, column = 0, sticky= 'w')

    lastnameinput = tk.Entry(form_frame)
    lastnameinput.grid(row = 1, column = 0, sticky = 'e')  # Corrected column

    agelabel = tk.Label(form_frame, text = "Age", font = ("Roboto", 14))
    agelabel.grid(row = 2, column = 0, sticky= 'w')

    ageinput = tk.Entry(form_frame)
    ageinput.grid(row = 2, column = 0, sticky = 'e')  # Corrected column

    birthdaylabel = tk.Label(form_frame, text = "Birthday", font = ("Roboto", 14))
    birthdaylabel.grid(row = 3, column = 0, sticky = 'w')

    birthdayinput = tk.Entry(form_frame)
    birthdayinput.grid(row = 3, column = 0, sticky ='e')  # Corrected column

    new_studentID = generate_id(cursor)

    idlabel= tk.Label(form_frame, text=f"Generated Student ID: {new_studentID}", font = ("Roboto", 14))
    idlabel.grid(row = 4, column = 0, sticky= 'e')  # Corrected row

    def submit():
        firstname = firstnameinput.get()
        lastname = lastnameinput.get()
        age = ageinput.get()
        birthday = birthdayinput.get()

        try:
            insert_query = 'INSERT INTO Student (Firstname, LastName, Birthday, Age, StudentID) VALUES (?,?,?,?,?)'
            cursor.execute(insert_query, (firstname, lastname, birthday, age, new_studentID))
            conn.commit()
            print("Student was successfully added.")
            add_student_window.destroy()
        except pyodbc.Error as ex:
            print(f"There was an error adding student", ex)
    
    def exit_window():
        add_student_window.destroy()

    submit_button = tk.Button(form_frame, text = "Submit", font = ("Roboto", 14), command = submit)
    submit_button.grid(row = 5, column = 0, sticky = 'w')
    exit_button = tk.Button(form_frame, text="Exit", font = ("Roboto", 14), command = exit_window)
    exit_button.grid(row = 5, column = 1, sticky= 'e')

def edit_student(conn,cursor):
    edit_student_window = tk.Toplevel()

    edit_student_window.title("Edit Student Information")

    edit_student_window.geometry("400x400")

    form_frame = tk.Frame(edit_student_window)
    form_frame.pack()

    editIDlabel = tk.Label(form_frame, text = "Student ID: ", font = ("Roboto", 14))
    editIDlabel.grid(row = 0, column = 0, sticky = 'w')

    editIDinput = tk.Entry(form_frame)
    editIDinput.grid(row = 0, column = 1, sticky = 'e')

    firstnamelabel = tk.Label(form_frame, text = "First Name: ", font = ("Roboto", 14))
    firstnamelabel.grid(row = 1, column = 0, sticky = 'w')

    firstnameinput = tk.Entry(form_frame)
    firstnameinput.grid(row = 1, column = 1, sticky = 'e')

    lastnamelabel = tk.Label(form_frame, text = "Lirst Name: ", font = ("Roboto", 14))
    lastnamelabel.grid(row = 2, column = 0, sticky = 'w')

    lastnameinput = tk.Entry(form_frame)
    lastnameinput.grid(row = 2, column = 1, sticky = 'e')

    agelabel = tk.Label(form_frame, text = "Age: ", font = ("Roboto", 14))
    agelabel.grid(row = 3, column = 0, sticky = 'w')

    ageinput = tk.Entry(form_frame)
    ageinput.grid(row = 3, column = 1, sticky = 'e')

    birthdaylabel = tk.Label(form_frame, text = "Birthday: ", font = ("Roboto", 14))
    birthdaylabel.grid(row = 4, column = 0, sticky = 'w')

    birthdayinput = tk.Entry(form_frame)
    birthdayinput.grid(row = 4, column = 1, sticky = 'e')

    def fetch_data():
        student_id = editIDinput.get()
        cursor.execute("SELECT * FROM Student WHERE StudentID= ?", (student_id))
        result = cursor.fetchone()

        if result is not None:
            editIDinput.config(state = 'disabled')
            firstnameinput.delete(0, tk.END)
            firstnameinput.insert(0, result[2])

            lastnameinput.delete(0, tk.END)
            lastnameinput.insert(0, result[3])

            ageinput.delete(0, tk.END)
            ageinput.insert(0, result[1])

            birthdayinput.delete(0, tk.END)
            birthdayinput.insert(0, result[5])
    
    fetch_button = tk.Button(form_frame, text = "Search Student", command = fetch_data)
    fetch_button.grid(row = 5, column = 1, sticky= 'w')

    def submit_changes():
        student_id = editIDinput.get()
        new_firstname = firstnameinput.get()
        new_lastname = lastnameinput.get()
        new_age = ageinput.get()
        new_birthday = birthdayinput.get()

        cursor.execute("UPDATE Student SET FirstName = ?, LastName = ?, Age = ?, Birthday = ? WHERE StudentID = ?", (new_firstname, new_lastname, new_age, new_birthday, student_id))
        conn.commit()
        messagebox.showinfo("Success", "Successfully Updated Student Information")
        edit_student_window.destroy()
    
    submit_button = tk.Button(form_frame, text = "Submit Changes", font = ("Roboto",14), command = submit_changes)
    submit_button.grid(row = 7, column = 1, sticky = 'w')


def delete_student(conn,cursor):
    delete_student_window = tk.Toplevel()

    delete_student_window.title("Delete A Student")

    delete_student_window.geometry("400x400")

    form_frame = tk.Frame(delete_student_window)
    form_frame.pack()

    deleteIDlabel = tk.Label(form_frame, text = "Student ID: ", font = ("Roboto", 14))
    deleteIDlabel.grid(row = 0, column = 0, sticky = 'w')

    deleteIDinput = tk.Entry(form_frame)
    deleteIDinput.grid(row = 0, column = 1 , sticky = 'e')

    def delete_data():
        student_id = deleteIDinput.get()
        cursor.execute("DELETE FROM Student WHERE StudentID = ?", (student_id))
        conn.commit()
        messagebox.showinfo(f"Success", "Student "+ student_id + "Successfully Deleted")
        delete_student_window.destroy()
    
    submit_button = tk.Button(form_frame, text = "Submit", font = ("Roboto", 10), command = delete_data)
    submit_button.grid(row = 1, column = 1, sticky = 'w')

def search_student(conn,cursor):
    # Create top level window
    search_student_window = tk.Toplevel()

    # Add the title
    search_student_window.title("Search A Student")

    # Set the window size
    search_student_window.geometry("400x400")

    # Set form frame
    form_frame = tk.Frame(search_student_window)
    form_frame.pack()

    # Add Labels
    searchID = tk.Label(form_frame, text = "Enter Student ID: ", font = ("Roboto", 14))
    searchID.grid(row = 0, column = 0, sticky = 'w')

    searchIDinput = tk.Entry(form_frame)
    searchIDinput.grid(row = 0, column = 1, sticky = 'e')

    def execute_search():
        student_id = searchIDinput.get()
        cursor.execute("SELECT * FROM Student WHERE StudentID = ?", (student_id))
        result = cursor.fetchone()
        if result is None:
            messagebox.ERROR("Search Result", "Student not found.")
        else:
            messagebox.showinfo("Search Result", "Student found:\n Name: " + result[2] + result[3] +", ID: "+str(result[4]))

    def exit_window():
        search_student_window.destroy()
    
    search_button = tk.Button(form_frame, text = "Search", command = execute_search)
    search_button.grid(row = 1, column = 0, sticky = 'w')
    exit_button = tk.Button(form_frame, text = "Exit", command = exit_window)
    exit_button.grid(row = 1 , column = 1, sticky = 'e')


def generate_id(cursor):
    while True:
        new_ID = random.randint(100000,999999)
        cursor.execute("SELECT * FROM Student WHERE STUDENTID = ?", new_ID)
        result = cursor.fetchone()
        if result is None:
            return new_ID
        
def update_time(label):
    current_time = _time.strftime('%Y-%m-%d | %H:%M:%S')
    label.config(text = current_time)
    label.after(1000,update_time,label)

def main():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    root = tk.Tk()

    # Set window title
    root.title("kxle.dev")

    # Set the window size
    root.geometry("600x600")

    # Labels
    title = tk.Label(root, text="Student Management System", font=("Roboto",32-8))
    title.pack()

    # Set Time
    time_label = tk.Label(root, font = ("Roboto", 14))
    time_label.pack(pady=(0, 30))
    update_time(time_label)

    button_frame = tk.Frame(root)
    button_frame.pack()

    devlabel = tk.Label(button_frame, text = "Developed by kxle.dev", font = ("Roboto", 10))
    devlabel.grid(row = 2, column = 0, sticky = 'w')

    add_student_button = tk.Button(button_frame, text="➕Add A Student", command=lambda: add_student_gui(conn, cursor), width = 15, height = 3, font = ("Roboto", 14))
    add_student_button.grid(row = 0, column = 0, sticky= 'w')

    search_student_button = tk.Button(button_frame, text = "🔍Search Student", command=lambda: search_student(conn, cursor), width = 15, height = 3, font = ("Roboto", 14))
    search_student_button.grid(row = 0, column = 1, sticky = 'e')

    edit_student_button = tk.Button(button_frame, text = "🖊️Edit Student\nInformation", command = lambda: edit_student(conn,cursor), width = 15, height = 3, font = ("Roboto", 14))
    edit_student_button.grid(row = 1, column = 0, sticky = 'w')

    delete_student_button = tk.Button(button_frame, text = "❌Delete A Student", command = lambda: delete_student(conn,cursor), width = 15, height = 3, font = ("Roboto", 14))
    delete_student_button.grid(row = 1, column = 1, sticky = 'e')

    root.mainloop()

if __name__ == '__main__':
    main()