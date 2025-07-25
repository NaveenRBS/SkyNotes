# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from datetime import timedelta
# from werkzeug.security import check_password_hash, generate_password_hash
# import pymysql
# import pymysql.cursors
# import traceback

# app = Flask(__name__)
# app.secret_key = '12345'
# app.permanent_session_lifetime = timedelta(days=7)

# # Railway DB config
# app.config["MYSQL_HOST"] = "mysql.railway.internal"
# app.config["MYSQL_PORT"] = 3306
# app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = "xKaFXsDMnUVqxUsDdpXmYQfXuzwbBraQ"
# app.config["MYSQL_DB"] = "railway"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# # Safe connection function
# def get_mysql_connection():
#     return pymysql.connect(
#         host=app.config["MYSQL_HOST"],
#         port=app.config["MYSQL_PORT"],
#         user=app.config["MYSQL_USER"],
#         password=app.config["MYSQL_PASSWORD"],
#         db=app.config["MYSQL_DB"],
#         cursorclass=pymysql.cursors.DictCursor
#     )

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if 'user_id' in session:
#         user_id = session['user_id']
#         if request.method == "POST":
#             title = request.form['title']
#             note = request.form['note']
#             con = get_mysql_connection()
#             cur = con.cursor()
#             cur.execute("INSERT INTO notes (user_id, title, note) VALUES (%s, %s, %s)", (user_id, title, note))
#             con.commit()
#             cur.close()
#             con.close()
#             return redirect(url_for("home"))
    
#         con = get_mysql_connection()
#         cur = con.cursor()
#         cur.execute("SELECT * FROM notes WHERE user_id=%s", (user_id,))
#         notes = cur.fetchall()
#         cur.close()
#         con.close()
#         return render_template('index.html', datas=notes)
#     else:
#         return render_template('home.html')

# @app.route('/deletenote/<int:user>/<int:id>')
# def deletenote(user, id):
#     if session.get('user_id') == user:
#         con = get_mysql_connection()
#         cur = con.cursor()
#         cur.execute("DELETE FROM notes WHERE note_id=%s", (id,))
#         con.commit()
#         cur.close()
#         con.close()
#         flash("Note deleted successfully")
#     return redirect(url_for("home"))

# @app.route('/editnote<int:user>/<int:id>', methods=["POST", "GET"])
# def editnote(user, id):
#     if session.get('user_id') == user:
#         con = get_mysql_connection()
#         cur = con.cursor()
#         if request.method == "POST":
#             title = request.form['title']
#             note = request.form['note']
#             cur.execute("UPDATE notes SET title=%s, note=%s WHERE note_id=%s AND user_id=%s",
#                         (title, note, id, user))
#             con.commit()
#             cur.close()
#             con.close()
#             return redirect(url_for("home"))

#         cur.execute("SELECT * FROM notes WHERE user_id=%s AND note_id=%s", (user, id))
#         data = cur.fetchone()
#         cur.close()
#         con.close()
#         return render_template('edituser.html', datas=data)
#     else:
#         return redirect(url_for('home'))

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     password_incorrect = False
#     if request.method == 'POST':
#         session.permanent = True
#         email = request.form['usermail']
#         password = request.form['password']

#         con = get_mysql_connection()
#         cur = con.cursor()
#         cur.execute("SELECT * FROM users WHERE email=%s", (email,))
#         user = cur.fetchone()
#         cur.close()
#         con.close()
        
#         if user and check_password_hash(user['password'], password):
#             session['user_id'] = user['user_id']
#             return redirect(url_for('home'))
#         else:
#             password_incorrect = True
#             return render_template('login.html', password_incorrect=password_incorrect, useremail=email)
#     else:
#         if 'user_id' in session:
#             return redirect(url_for('home'))
#     return render_template("login.html")

# @app.route('/sign-up', methods=['POST', 'GET'])
# def signup():
#     if request.method == 'POST':
#         session.permanent = True
#         username = request.form['username']
#         email = request.form['usermail']
#         password = request.form['password']

#         con = get_mysql_connection()
#         cur = con.cursor()
#         cur.execute("SELECT * FROM users WHERE email=%s", (email,))
#         res = cur.fetchone()

#         if res:
#             cur.close()
#             con.close()
#             return render_template("login.html", alreadysignuped=True, useremail=email)
#         else:
#             cur.execute("INSERT INTO users (user_name, email, password) VALUES (%s, %s, %s)",
#                         (username, email, generate_password_hash(password)))
#             con.commit()
#             cur.execute("SELECT * FROM users WHERE email=%s", (email,))
#             user = cur.fetchone()
#             cur.close()
#             con.close()
#             session['user_id'] = user['user_id']
#             return redirect(url_for('home'))
#     else:
#         if 'user_id' in session:
#             return redirect(url_for('home'))
#     return render_template('signup.html')

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect(url_for('home'))

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8080)

# # if __name__ == '__main__':
# #     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
import pymysql
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.permanent_session_lifetime = timedelta(days=7)

# Railway DB config
app.config["MYSQL_HOST"] = "mysql.railway.internal"
app.config["MYSQL_PORT"] = 3306
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "xKaFXsDMnUVqxUsDdpXmYQfXuzwbBraQ"
app.config["MYSQL_DB"] = "railway"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

def get_mysql_connection():
    return pymysql.connect(
        host=app.config["MYSQL_HOST"],
        port=app.config["MYSQL_PORT"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        db=app.config["MYSQL_DB"],
        cursorclass=pymysql.cursors.DictCursor
    )

# Public landing page
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# Dashboard for logged-in users
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        note  = request.form.get('note', '').strip()
        if title and note:
            con = get_mysql_connection()
            cur = con.cursor()
            cur.execute(
                "INSERT INTO notes (user_id, title, note) VALUES (%s, %s, %s)",
                (user_id, title, note)
            )
            con.commit()
            cur.close()
            con.close()
        return redirect(url_for('dashboard'))

    con = get_mysql_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM notes WHERE user_id=%s ORDER BY note_id DESC", (user_id,))
    notes = cur.fetchall()
    cur.close()
    con.close()
    return render_template('index.html', datas=notes)

@app.route('/deletenote/<int:user_id>/<int:note_id>')
def deletenote(user_id, note_id):
    if session.get('user_id') == user_id:
        con = get_mysql_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM notes WHERE note_id=%s AND user_id=%s", (note_id, user_id))
        con.commit()
        cur.close()
        con.close()
        flash("Note deleted successfully.")
    return redirect(url_for('dashboard'))

@app.route('/editnote/<int:user_id>/<int:note_id>', methods=['GET', 'POST'])
def editnote(user_id, note_id):
    if session.get('user_id') != user_id:
        return redirect(url_for('dashboard'))

    con = get_mysql_connection()
    cur = con.cursor()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        note  = request.form.get('note', '').strip()
        if title and note:
            cur.execute(
                "UPDATE notes SET title=%s, note=%s WHERE note_id=%s AND user_id=%s",
                (title, note, note_id, user_id)
            )
            con.commit()
        cur.close()
        con.close()
        return redirect(url_for('dashboard'))

    cur.execute(
        "SELECT * FROM notes WHERE note_id=%s AND user_id=%s",
        (note_id, user_id)
    )
    data = cur.fetchone()
    cur.close()
    con.close()
    return render_template('edituser.html', datas=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        flash("You're already logged in.")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        session.permanent = True
        email    = request.form.get('usermail', '').strip()
        password = request.form.get('password', '')

        con = get_mysql_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        con.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "error")
            return render_template('login.html', useremail=email)

    return render_template('login.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        flash("You're already logged in.")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        session.permanent = True
        username = request.form.get('username', '').strip()
        email    = request.form.get('usermail', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm', '')

        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template('signup.html', username=username, useremail=email)

        con = get_mysql_connection()
        cur = con.cursor()
        cur.execute("SELECT 1 FROM users WHERE email=%s", (email,))
        if cur.fetchone():
            cur.close()
            con.close()
            flash("Email already registered. Please log in.", "error")
            return redirect(url_for('login'))

        cur.execute(
            "INSERT INTO users (user_name, email, password) VALUES (%s, %s, %s)",
            (username, email, generate_password_hash(password))
        )
        con.commit()
        # fetch the new user’s ID
        cur.execute("SELECT user_id FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        con.close()

        session['user_id'] = user['user_id']
        return redirect(url_for('dashboard'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
