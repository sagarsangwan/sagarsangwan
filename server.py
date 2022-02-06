import os
from flask import Flask, app, render_template, request
from flask_mysqldb import MySQL
from projects.wordbook import dict
from dotenv import load_dotenv

load_dotenv('.env')

app = Flask(__name__)
app.config['MYSQL_USER'] = os.environ.get("DB_USER_NAME")
app.config['MYSQL_PASSWORD'] = os.environ.get("DB_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("DB_DATABASE_NAME")
app.config['MYSQL_HOST'] = os.environ.get("DB_HOST_NAME")
app.config['MYSQL_PORT'] = int(os.environ.get("DB_PORT"))
mysql = MySQL(app)
# to remove special characters from string


def clean(string):
    clean_string = ""
    valid_character = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ,.!?()[]{}<>\\/'
    for char in string:
        if char.isalnum() or char in valid_character:
            clean_string += char
    return clean_string


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        details = request.form
        names = details['user_name']
        names = clean(names)
        emails = details['email']
        messages = details['message']
        message = clean(messages)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO messages (user_name, email, message) VALUES (%s, %s, %s)",
                    (names, emails, message))
        mysql.connection.commit()
        cur.close()
        return render_template("pages/home.html", info="Message sent sucessfully")

    return render_template("pages/home.html")


@app.route("/dictionary", methods=["GET"])
def dictionary():
    word1 = request.args.get('word')
    data, status, metadata = dict.translate(word1)
    return render_template("pages/dictionary.html", key=(data, status, metadata))


@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    if request.method == "GET":
        return render_template("pages/login.html")
    else:
        name1 = request.form["username"]
        pwd = request.form["password"]
        print(name1, pwd)
        print(os.environ.get("AUTH_USERNAME"), os.environ.get("AUTH_PASSWORD"))
        if name1 == os.environ.get("AUTH_USERNAME") and pwd == os.environ.get("AUTH_PASSWORD"):
            cur = mysql.connection.cursor()
            mysql.connection.commit()
            cur.execute("SELECT * FROM messages")
            tables = cur.fetchall()
            cur.close()
            return render_template("pages/dashboard.html", value=list(tables))
        else:
            return render_template("pages/login.html")


@app.route("/timeline")
def timeline():
    return render_template("pages/timeline.html", lst=[["sagar", "full stack developer", "bug"], ["sagar", "full stack developer", "feature"]])


@app.errorhandler(404)
def page_not_found(e):
    return render_template("pages/404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("pages/500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
