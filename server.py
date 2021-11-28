from flask import Flask, app, render_template


app = Flask(__name__)



@app.route("/")
def home():
    return render_template("home.html")
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods = ['GET', 'POST'])
def contact():

    return render_template("contact.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")

if __name__ == "__main__":
    app.run(debug=True)
                        