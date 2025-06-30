from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash

# Use PyMySQL as MySQLdb
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

app = Flask(__name__)
app.secret_key = '12345'
app.permanent_session_lifetime = timedelta(days=7)

# MySQL configurations (override with Railway ENV vars)
# app.config["MYSQL_HOST"] = "localhost"
# app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = "NaveenRBS"
# app.config["MYSQL_DB"] = "skynotes"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Railway MySQL configuration
app.config["MYSQL_HOST"] = "turntable.proxy.rlwy.net"
app.config["MYSQL_PORT"] = 52532
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "xKaFXsDMnUVqxUsDdpXmYQfXuzwbBraQ"
app.config["MYSQL_DB"] = "railway"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


# Connect manually with MySQLdb (not Flask-MySQLdb anymore)
def get_mysql_connection():
    return MySQLdb.connect(
        host=app.config["MYSQL_HOST"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        db=app.config["MYSQL_DB"],
        cursorclass=MySQLdb.cursors.DictCursor
    )

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user_id' in session:
        id = session['user_id']
        if request.method == "POST":
            notetitle = request.form['title']
            notes = request.form['note']
            con = get_mysql_connection()
            cur = con.cursor()
            cur.execute("INSERT INTO notes (user_id, title, note) VALUES (%s, %s, %s)", (id, notetitle, notes))
            con.commit()
            cur.close()
            con.close()
            return redirect(url_for("home"))
        
        con = get_mysql_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM notes WHERE user_id=%s", (id,))
        res = cur.fetchall()
        cur.close()
        con.close()
        return render_template('index.html', datas=res)
    else:
        return render_template('home.html')

@app.route('/deletenote/<int:user>/<string:id>')
def deletenote(user, id):
    if session['user_id'] == user:
        con = get_mysql_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM notes WHERE note_id=%s", [id])
        con.commit()
        cur.close()
        con.close()
        flash("Note deleted Successfully")
        return redirect(url_for("home"))
    else:
        return redirect(url_for('login'))

@app.route('/editnote<int:user>/<int:id>', methods=["POST", "GET"])
def editnote(user, id):
    if session['user_id'] == user:
        con = get_mysql_connection()
        cur = con.cursor()
        if request.method == "POST":
            notetitle = request.form['title']
            notes = request.form['note']
            sql = "UPDATE notes SET title=%s, note=%s WHERE note_id=%s AND user_id=%s"
            cur.execute(sql, (notetitle, notes, id, user))
            con.commit()
            cur.close()
            con.close()
            return redirect(url_for("home"))
        
        cur.execute("SELECT * FROM notes WHERE user_id=%s AND note_id=%s", (user, id))
        res = cur.fetchone()
        cur.close()
        con.close()
        return render_template('edituser.html', datas=res)
    else:
        return redirect(url_for('home'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    password_incorrect = False
    if request.method == 'POST':
        session.permanent = True
        useremail = request.form['usermail']
        password = request.form['password']

        con = get_mysql_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (useremail,))
        user = cur.fetchone()
        cur.close()
        con.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            return redirect(url_for('home'))
        else:
            password_incorrect = True
            return render_template('login.html', password_incorrect=password_incorrect, useremail=useremail)
    else:
        if 'user_id' in session:
            return redirect(url_for('home'))
    return render_template("login.html")

@app.route('/sign-up', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        session.permanent = True
        username = request.form['username']
        useremail = request.form['usermail']
        password = request.form['password']

        con = get_mysql_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (useremail,))
        res = cur.fetchone()

        if res:
            cur.close()
            con.close()
            return render_template("login.html", alreadysignuped=True, useremail=useremail)
        else:
            cur.execute("INSERT INTO Users (user_name, email, password) VALUES (%s, %s, %s)",
                        (username, useremail, generate_password_hash(password)))
            con.commit()
            cur.execute("SELECT * FROM users WHERE email=%s", (useremail,))
            res = cur.fetchone()
            cur.close()
            con.close()
            session['user_id'] = res['user_id']
            return redirect(url_for('home'))
    else:
        if 'user_id' in session:
            return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
