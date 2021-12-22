import os
from flask import Flask, app, render_template, request
from flask_mysqldb import MySQL
from projects.dictionary import dict





app = Flask(__name__)
app.config['MYSQL_USER'] = os.environ.get("DB_USER_NAME")
app.config['MYSQL_PASSWORD'] = os.environ.get("DB_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("DB_DATABASE_NAME")
app.config['MYSQL_HOST'] = os.environ.get("DB_HOST_NAME")
app.config['MYSQL_PORT'] = int(os.environ.get("DB_PORT"))

mysql = MySQL(app)

    


@app.route("/")
def home():
    return render_template("pages/home.html")

@app.route("/projects")
def projects():
    return render_template("pages/projects.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        details = request.form
        names = details['user_name']
        emails = details['email']
        messages = details['message']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO messages (user_name, email, message) VALUES (%s, %s, %s)",
                    (names, emails, messages))
        mysql.connection.commit()
        cur.close()

        return render_template("pages/contact.html", info ="Message sent sucessfully")
        
    return render_template("pages/contact.html")

@app.route("/dictionary", methods = ["GET","POST"])
def dictionary():
    if request.method == "POST":
        word = request.form['word']
        data, status, metadata = dict.translate(word, None)

        
        return render_template("pages/dictionary.html", key = (data, status, metadata))
    
    return render_template("pages/dictionary.html", key = ())
        
    


@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    if request.method == "GET":
        return render_template("pages/login.html")
    else:
        name1 = request.form["username"]
        pwd = request.form["password"]
        if name1 == os.environ.get("AUTH_USERNAME") and pwd == os.environ.get("AUTH_PASSWORD"):
            cur = mysql.connection.cursor()
            mysql.connection.commit()
            cur.execute("SELECT * FROM messages")
            tables = cur.fetchall()
            cur.close()
            return render_template("pages/dashboard.html", value = list(tables))
        else:
            return render_template("pages/login.html")
             
        
    
        


@app.errorhandler(404)
def page_not_found(e):
    return render_template("pages/404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("pages/500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
