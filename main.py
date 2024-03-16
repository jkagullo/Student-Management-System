import pyodbc

conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Jkyle Agullo\Documents\mydatabase.accdb;'

def add_user(conn, cursor):
    new_id = input('Enter a new user ID: ')
    newname = input('Enter a new name: ')
    age = input('Enter a new user age: ')

    insert_query = 'INSERT INTO Users (ID, username, userage) VALUES (?,?,?)'
    cursor.execute(insert_query, (new_id, newname, age))
    conn.commit()
    print('New user added successfully')

def delete_user(conn, cursor):
    user_id = input('Enter the User ID to delete: ')

    delete_query = 'DELETE FROM Users WHERE ID = ?'
    cursor.execute(delete_query, (user_id,))
    conn.commit()
    print('User deleted successfully')

def show_all(cursor):
    cursor.execute('SELECT * FROM Users')
    for row in cursor.fetchall():
        print(row)

def search_user(conn, cursor):
    userSearchID = input('Enter User ID to search: ')

    search_query = 'SELECT * FROM Users WHERE ID = ?'
    cursor.execute(search_query, (userSearchID))

    for row in cursor.fetchall():
        print (row)

def main():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    while True:
        print('\n Database Practice\n')
        print('(1) Add A New User')
        print('(2) Delete A User')
        print('(3) Show All Users')
        print('(4) Search A User')
        print('(5) Exit Application')

        choice = input('Enter Choice: ')
        print('\n')

        if choice == '1':
            add_user(conn,cursor)
        elif choice == '2':
            delete_user(conn,cursor)
        elif choice == '3':
            show_all(cursor)
        elif choice == '4':
            search_user(conn,cursor)
        elif choice == '5':
            break
        else:
            print('Invalid Choice.')
        
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()





