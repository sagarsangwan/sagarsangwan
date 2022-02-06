import os
from turtle import title
from flask import Flask, app, redirect, render_template, request
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
    valid_character = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ,.!?()[]{}<>\\/\n\r\n\t'
    for char in string:
        if char.isalnum() or char in valid_character:
            clean_string += char
    return clean_string


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        details = request.form
        title = details['title']
        title = clean(title)
        record_type = details['record_type']
        deseription = details['description']
        message = clean(deseription)
        print(title, record_type, message)
        # cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO timeline_records (title, record_type, message) VALUES (%s, %s, %s)",
        #             (title, record_type, message))
        # mysql.connection.commit()
        # cur.close()
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


@app.route("/timeline", methods=["GET", "POST"])
def timeline():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM timeline_records ORDER BY created_at DESC")
        result = list(cur.fetchall())
        cur.close()
        records = []
        for i in result:
            title = i[1]
            description = list(i[2].splitlines())
            record_type = i[3]
            date = i[4]
            item = {'title': title, 'description': description,
                    'record_type': record_type, 'date': date}
            records.append(item)
        print(records)
        return render_template("pages/timeline.html", lst=[["sagar", "full stack developer", "bug"], ["sagar", "full stack developer", "feature"]])
    else:
        details = request.form
        title = clean(details['title'])
        record_type = clean(details['record_type'])
        description = clean(details['description'])
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO timeline_records (title, record_type, description) VALUES (%s, %s, %s)",
                    (title, record_type, description))
        mysql.connection.commit()
        cur.close()
        return redirect("/timeline")
    return render_template("pages/timeline.html", lst=[["sagar", "full stack developer", "bug"], ["sagar", "full stack developer", "feature"]])


@ app.errorhandler(404)
def page_not_found(e):
    return render_template("pages/404.html"), 404


@ app.errorhandler(500)
def internal_server_error(e):
    return render_template("pages/500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
# create table timeline_records(
# id int not null primary key auto_increment,
# title text not null,
# description text not null,
# record_type text not null,
# created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP not null
# )
