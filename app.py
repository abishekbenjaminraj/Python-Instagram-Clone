from flask import Flask,render_template,request,redirect,url_for,session,flash,make_response
import sqlite3 as sql
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "Abi123"

def isloggedin():
    return session in "username"


@app.route('/signup',methods = ["GET","POST"])
def signup():
    if request.method == "POST":
        number = request.form.get("number")
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        con = sql.connect("user.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("insert into instagram (number,name,username,password) values(?,?,?,?)",
                    (number,name,username,password))
        con.commit()
        return redirect(url_for('login'))
    return render_template ("signup.html")

@app.route('/', methods = ["GET","POST"])
def login():
    if request.method == "POST":
        name1 = request.form.get("username1")
        pass1 = request.form.get("password1")
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("select * from instagram where username=? and password=?", (name1,pass1))
        fet = cur.fetchall()
        for i in fet:
            if name1 in i and pass1 == i[3]:
                session["username"] = name1
                return redirect (url_for('main'))
            
            else:
                return "Incorrect Username or Password"
    return render_template ("login.html")
    
@app.route('/instagram')
def main():
    return render_template ("index.html")

@app.route('/<type>/increment')
def increment(type):
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("select * from likes")
        fet = cur.fetchall()
        for i in fet:
                if type=="add":
                    i=i[0]+1
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("update likes set like=?",((str(i), )))
        con.commit()
        return render_template("index.html",like=i)

@app.route("/post",methods=['GET','POST'])
def upload():
        if request.method=="GET":
            return render_template('home.html')
        elif request.method=="POST":
            destination_path=""
            fileobj = request.files['file']
            file_extensions =  ["JPG","JPEG","PNG","GIF"]
            uploaded_file_extension = fileobj.filename.split(".")[1]
            if(uploaded_file_extension.upper() in file_extensions):
                destination_path= f"static/uploads/{fileobj.filename}"
                fileobj.save(destination_path)
                try:
                    conn = sql.connect("database.db")
                    cursor = conn.cursor()
                    cursor.execute("""insert into usercontent values(:userid,:username,
                                :imagelink,:caption)""",{'userid':1,'username':'__a.b.i.s.h.e.k__001','imagelink':destination_path,'caption':'Fly me to the moon'})
                    conn.commit()
                    conn.close()
                except sql.Error as error:
                    flash(f"{error}")
                    return render_template('home.html')
            else:
                flash("only images are accepted")
                return render_template('home.html') 
        return redirect(url_for("view"))

@app.route("/view")
def view():
    try:
        conn = sql.connect("database.db")
        conn.row_factory=sql.Row
        cursor = conn.cursor()
        cursor.execute("select * from usercontent")
        rows = cursor.fetchall()
        conn.close()
    except sql.Error as error:
        flash("Something went wrong while uploading file to database!")
        return render_template('home.html')
    return render_template('view.html',response = rows )
    


if __name__ == "__main__":
    app.run(debug=True)