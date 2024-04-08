from tkinter import *
import sqlite3
from tkinter import filedialog

# Initialize Tkinter
root = Tk()
root.geometry('600x600')
root.resizable('false', 'false')
root.title('Data Entry Automation')

# Global variables for database connection and cursor
connection = None
cursor = None
tables_g = []

# Function to navigate to the home page
def home_page():
    data_enter_f.place_forget()
    data_f.place_forget()
    home_f.place(x=0, y=0)

# Function to navigate to the data page
def data_page():
    home_f.place_forget()
    data_enter_f.place_forget()
    data_f.place(x=0, y=0)

# Function to navigate to the data entry page
def data_enter():
    home_f.place_forget()
    data_f.place_forget()
    data_enter_f.place(x=0, y=0)

# Function to fetch tables from the database
def database(fp):
    global cursor, tables_g
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    y_position = 80
    for table in tables:
        tables_g.append(table[0])
        table_name = table[0]
        table_label = Label(data_f, text=table_name, font=('Roboto', 15))
        table_label.place(x=50, y=y_position)
        y_position += 50
    enter_data_b(tables_g)

# Function to handle data entry for a specific table
def enter_data_to_page(choice_num):
    global cursor, tables_g
    data_enter()
    cursor.execute(f"PRAGMA table_info({tables_g[choice_num]})")
    columns = cursor.fetchall()

    column_names = []
    for col in columns:
        column_names.append(col[1])

    column_l = Label(data_enter_f, text='Column Name', font=('Roboto', 25,'bold','italic'),fg='blue')
    column_l.place(x=200, y=10)

    x_pos = 10
    y_pos = 80
    entered_data = []
    for i in column_names:
        col_enter_e = Entry(data_enter_f,width=13)
        col_enter_e.place(x=x_pos, y=y_pos+30)
        entered_data.append(col_enter_e)
        column_name_l = Label(data_enter_f, text=i, font=('Roboto', 10,'bold','underline'))
        column_name_l.place(x=x_pos, y=y_pos)
        if x_pos<430:
            x_pos = (x_pos+len(i)*5) + 70
        else:
            y_pos += 100
            x_pos = 10

    col_name_t = tuple(column_names)
    def enter_data_to_database():
        values = []
        for entry in entered_data:
            value = entry.get()
            values.append(value)

        # Prepare the SQL query with placeholders for dynamic column names
        sql_query = f"INSERT INTO {tables_g[choice_num]} {col_name_t} VALUES ({', '.join(['?'] * len(entered_data))})"
        data_to_insert = tuple(values)
        cursor.execute(sql_query, data_to_insert)
        connection.commit()

    data_enter_b = Button(data_enter_f, text="ENTER DATA", font=('Roboto', 10, 'bold'), fg="Blue",command=enter_data_to_database)
    data_enter_b.place(x=250, y=550)

# Function to create buttons for entering data into each table
def enter_data_b(tab):
    global data_f
    y_posit = 80
    choice = []
    for i in range(len(tab)):
        choice.append(i)
        data_enter_b = Button(data_f, text="ENTER DATA", font=('Roboto', 10, 'bold'), fg="Blue",
                              command=lambda num=i: enter_data_to_page(num))
        data_enter_b.place(x=250, y=y_posit)
        y_posit += 50

# Function to select a database file
def file():
    global connection, cursor
    data_page()
    global file_path
    file_path = filedialog.askopenfilename()
    ext = ''
    for i in range(len(file_path)):
        if file_path[i] == '.':
            for j in range(i, len(file_path)):
                ext += file_path[j]
            break
        else:
            continue
    if ext == '.db':
        connection = sqlite3.connect(file_path)
        cursor = connection.cursor()
        database(file_path)
    else:
        print("Wrong Format File")

# Frames
home_f = Frame(root, width=600, height=600)
data_f = Frame(root, width=600, height=600)
data_enter_f = Frame(root, width=600, height=600)

# Labels
title_l = Label(home_f, text="Data Entry Automation".upper(), font=('Roboto', 30, 'bold'), fg="Blue")
title_l.place(x=35, y=25)
ask_l = Label(home_f, text="Locate Your File", font=('Roboto', 15))
ask_l.place(x=200, y=200)
ask_about_table_l = Label(data_f, text="Which Table Do You want to Modify?", font=('Roboto', 15))
ask_about_table_l.place(x=50, y=0)
table_names_l = Label(data_f, font=('Roboto', 15))

# Buttons
file_b = Button(home_f, text="LOCATE", font=('Roboto', 10, 'bold'), fg="Blue", command=file)
file_b.place(x=250, y=250)

home_page()
root.mainloop()
