from flask import Flask, render_template, request , redirect , url_for , flash ,session
from datetime import timedelta 
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = '12345'
app.permanent_session_lifetime = timedelta(days=7)

# MySQL configurations
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "NaveenRBS"
app.config["MYSQL_DB"] = "skynotes"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


 
@app.route('/', methods=['GET', 'POST'] )
def home():    
    
# check if the user is logged in , if not redirect to home page  
  if 'user_id' in session :
    id = session['user_id']
    # insert the data into user notes and redirect it to home again to show the inserted note using the user_id stored in session
    if request.method == "POST":

        notetitle = request.form['title']
        notes = request.form['note']  
        con = mysql.connection.cursor()
        con.execute("INSERT INTO notes (user_id,title, note) VALUES (%s,%s,%s)",(id,notetitle,notes))
        mysql.connection.commit()
        con.close() 
        
        return redirect (url_for("home"))
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM notes WHERE user_id=%s", (id,))
    res = con.fetchall()
    con.close()
    
    return render_template('index.html', datas=res)
  else :
    return render_template('home.html')
    
# get the note id by data.note_id in index page and delete it from the db

@app.route('/deletenote/<int:user>/<string:id>')
def deletenote(user,id):
   
    if  session['user_id'] == user:
        con = mysql.connection.cursor()
        sql = "delete from notes where note_id=%s"
        con.execute(sql,[id,])
        mysql.connection.commit()
        con.close()
        flash("Note deleted Successfully")
        return redirect(url_for("home")) 
    else :
        return redirect(url_for('login'))  


 
@app.route('/editnote<int:user>/<int:id>', methods=["POST", "GET"])
def editnote(user,id):
    # check that note user id and session's user id are same to prevent another users to modify other's note 
    if  session['user_id'] == user:
        con = mysql.connection.cursor()
        if request.method == "POST" :
            notetitle = request.form['title']
            notes = request.form['note']
            sql = "UPDATE notes SET title=%s, note=%s WHERE note_id=%s and user_id=%s" 
            con.execute(sql, (notetitle, notes, id,user))    
            mysql.connection.commit()
            con.close()
            return redirect(url_for("home"))
        con.execute("SELECT * FROM notes WHERE user_id=%s and note_id=%s",(user,id,))
        res = con.fetchone()
        return render_template('edituser.html', datas=res)
    else:
       return redirect(url_for('home'))

@app.route('/login',methods=['POST','GET'])
def login():
    
    password_incorrect = False
    if request.method == 'POST':
        session.permanent = True 
        useremail = request.form['usermail']
        password = request.form['password']
        
        con = mysql.connection.cursor()
        con.execute(("select * from users WHERE email=%s"),(useremail,))
        user = con.fetchone()
        con.close() 
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            return redirect(url_for('home'))
        else:
            password_incorrect = True
            return render_template('login.html',password_incorrect = password_incorrect,useremail=useremail)
    else:
        if 'user_id' in session :
            return redirect(url_for('home'))        
    return render_template ("login.html")


@app.route('/sign-up',methods=['POST','GET'])
def signup():
    con = mysql.connection.cursor()
    if request.method == 'POST':
        session.permanent = True 
        username = request.form['username']
        useremail = request.form['usermail']
        password = request.form['password']   
        cpassword = request.form['cpassword']
        
        con.execute(("select * from users WHERE email=%s "),(useremail,))
        res = con.fetchone()
        alreadysignuped = False
        
        if res :
           alreadysignuped = True
           return render_template("login.html",alreadysignuped = alreadysignuped,useremail=useremail)
            
        else :
            sql="INSERT INTO Users (user_name,email,password) VALUES (%s,%s,%s);"
            con.execute(sql,(username,useremail, generate_password_hash(password))) 
            mysql.connection.commit()
            # create a new user with the data and get the unique auto incremented user_id from with the help of email . 
            con.execute(("select * from users WHERE email=%s "),(useremail,))
            res = con.fetchone()
            # store it in the session to access and check if the user is logged in or not 
            session['user_id'] = res['user_id']
            con.close()
            
            return redirect(url_for('home'))
    else:
        if 'user_id' in session :
            return redirect(url_for('home'))
    return render_template('signup.html')


@app.route('/logout')
def logout():
    if 'user_id' in session :
      session.pop('user_id',None)
      return redirect(url_for('home'))
    else :      
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
    
