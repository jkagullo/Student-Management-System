import pyodbc
import random

# Setup the connection string
conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\3rd Year\2nd Sem\Advandced Web Development\Databases\studentpy.accdb;'

'''
try:
    # Execute the ALTER TABLE command to add a new column
    cursor.execute('ALTER TABLE Student ADD COLUMN DATETIME')
    print("Executed Successfully")
except pyodbc.Error as ex:
    print("An Error Occured:", ex)
'''

def menu():
    print("Student Mangement System\n")
    print("===============================\n")
    print("Choose An Option:\n")
    print("(1) Add A Student")
    print("(2) Search A Student")
    print("(3) Show All Student")
    print("(4) Update Student")
    print("(5) Generate Report")
    print("(6) Exit Application")
    choice = input ("Enter Choice: ")
    return choice

def add_student(conn,cursor):
    new_firstname = input("Enter First Name: ")
    new_lastname = input("Enter Last Name: ")
    new_age = input("Enter Age: ")
    # When Adding A New Student, Generate a Unique Student ID
    new_studentID = generate_unique_id(cursor)
    print(f"Generated Student ID: {new_studentID}")
    new_birthday = input("Enter Birthday (YYYY-MM-DD): ")
    try:
        insert_query = 'INSERT INTO Student (Age,FirstName,LastName, StudentID, Birthday) VALUES (?,?,?,?,?)'
        cursor.execute(insert_query, (new_age,new_firstname,new_lastname,new_studentID,new_birthday))
        conn.commit()
    except pyodbc.Error as ex:
        print(f"There was an error adding the student.", ex)

def update_student(conn,cursor):
    student_id = input("Enter Student ID: ")
    print("======================================\n")
    print("(1) Update First Name\n")
    print("(2) Update Last Name\n")
    print("(3) Update Age\n")
    print("(4) Update Birthday\n") 
    print("======================================\n")
    choice = input("Select Option: ").strip()
    if choice == '1':
        new_value = input("Enter New First Name: ")
        update_query = 'UPDATE Student SET FirstName = ? WHERE StudentID = ?'
    elif choice == '2':
        new_value = input("Enter New Last Name: ")
        update_query = 'UPDATE Student SET LastName = ? Where StudentID = ?'
    elif choice == '3':
        new_value = input("Enter New Age: ")
        update_query = 'UPDATE Student SET Age = ? Where StudentID = ?'
    elif choice == '4':
        new_value = input("Enter New Birthday: ")
        update_query = 'UPDATE Student SET Birthday = ? WHERE StudentID = ?'
    else:
        print("Invalid Choice.")
    
    try:
        cursor.execute(update_query,(new_value, student_id))
        conn.commit()
        print("Student Updated Successfully.")
    except pyodbc.Error as ex:
        print(f"There was an error updating the Student.",ex)

def search_student(conn,cursor):
    search_id = input("Enter Student ID: ")

    try:
        search_query = 'SELECT * FROM Student WHERE StudentID = ?'
        cursor.execute(search_query, (search_id))
        for row in cursor.fetchall():
            print(row)
    except pyodbc.Error as ex:
        print(f"There was an error searching for student.",ex)

def show_all(conn,cursor):
    try:
        cursor.execute("SELECT * FROM Student")
        for row in cursor.fetchall():
            print(row)
    except pyodbc.Error as ex:
        print(f"There was an error retrieving all students", ex)

def generate_report(conn,cursor):
    generate_id = input("Enter Student ID: ")
    try:
        cursor.execute("SELECT FirstName, LastName, Age, Birthday FROM Student WHERE StudentID = ?", generate_id)
        result = cursor.fetchone()
        if result is None:
            print("No Student Found.")
        else:
            print("\nStudent Report\n")
            print("=================================")
            print(f"\nFirst Name: {result[0]}\nLast Name: {result[1]}\nAge: {result[2]}\nBirthday: {result[3]}\n")
            print("=================================")
    except pyodbc.Error as ex:
        print(f"There was an error generating report", ex)

def generate_unique_id(cursor):
    while True:
        new_ID = random.randint(100000,999999)
        cursor.execute("SELECT * FROM Student WHERE STUDENTID = ?", new_ID)
        result = cursor.fetchone()
        if result is None:
            return new_ID
        
def main():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    while True:
        choice = menu()
        if choice == '1':
            add_student(conn,cursor)
        elif choice == '2':
            search_student(conn,cursor)
        elif choice == '3':
            show_all(conn,cursor)
        elif choice == '4':
            update_student(conn,cursor)
        elif choice == '5':
            generate_report(conn,cursor)
        elif choice == '6':
            exit(0)
            break
        else: print("Invalid Choice, Please Try Again.")
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()



