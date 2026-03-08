import os
from  datetime import datetime
from flask import Flask , render_template , request
import atten_db_try1 as db
app=Flask(__name__)

def get_time():
    date=datetime.now()
    return date.strftime("%d %B  %Y")

@app.route("/")
def start():
    students=db.gets_all(conn)
    return render_template("atten_display1.html", students=students, date= get_time() , list_=None)

@app.route("/submit", methods=["POST"])    
def get(): 
    id_student=request.form["students_input"] #input label in html
    conn=db.get_connection()#creates the connection with html
    db.add(conn,id_student, get_time())#insert students
    list_=db.show(conn, get_time())# shows the students that are present in the day
    students=db.gets_all(conn)
    return render_template("atten_display1.html", students=students, date= get_time() , list_=list_)

if __name__=="__main__":
    conn=db.get_connection()
    db.creates_daily(conn)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
