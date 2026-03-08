import sqlite3

def get_connection():
      return sqlite3.connect('Attendance.db', check_same_thread=False)# able to be used in different threads,
      #which is necessary for a web application where multiple requests may be handled concurrently.

def main():
    conn=get_connection()
    cur=conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS students( 
                id INTEGER PRIMARY KEY,
                name TEXT  NOT NULL,
                center TEXT NOT NULL   )''')
    
   
    while True:
        try:
            option=input("Enter here your option: ")
            if option=='1':
                 name=input("Enter Name: ").title().strip()
                 center=input("Enter Center: ").strip()
                 add_student(conn, name, center)
            elif option == '2':
                print(" ")
                c=input("Enter Center: ").strip()
                show_students(conn)
        except (EOFError, sqlite3.IntegrityError, sqlite3.ProgrammingError) as e:
            break
            print("Error: ", e)

    conn.commit()
    conn.close()    
                    
def show_students(conn):
    cur=conn.cursor()
    cur.execute('''SELECT * FROM students''' )
    rows=cur.fetchall()
    for id , name, center_ in rows:
        print(f'{id})_  {name}                  in Center               {center_}')

def add_student(conn, name, center ):
    cur=conn.cursor()
    cur.execute('''INSERT INTO students (name , center) VALUES (?,?)''',(name , center))
    conn.commit()



def creates_daily(conn):# goes along with the logic part 
    cur=conn.cursor()
    cur.execute('''CREATE TABLE  IF NOT EXISTS daily_list (
                id INTEGER PRIMARY KEY,
                id_students INTEGER  NOT NULL,
                date TEXT NOT NULL,
                UNIQUE (id_students, date),
                FOREIGN KEY (id_students) REFERENCES students(id) )''')
    

def add(conn,id, date):# all this data comes from the html input (the name) , the data from the other python file
    cur=conn.cursor()
    cur.execute('INSERT INTO daily_list (id_students,date) VALUES (?,?)',(id,date))
    conn.commit()    

def gets_all(conn):
    cur=conn.cursor()
    cur.execute("SELECT id , name FROM  students")
    return  cur.fetchall()

    
def show(conn,date):
   today=date

   cur=conn.cursor()
   cur.execute('SELECT students.name, daily_list.date FROM daily_list JOIN students ON daily_list.id_students = students.id WHERE DATE = ? ', (today,)) 
   #Here, basically Python selects name from the table student, data from daily_list, 
   #and then it joins the two tables together based on the condition that the id_students in daily_list matches the id in students.
   #This way, we can get the name of the student along with the date they were marked as present.
   list_=cur.fetchall() 
   return list_


if __name__=="__main__":
    main()
