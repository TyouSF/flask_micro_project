from app import create_app
from flask import render_template

app = create_app()


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/base/')
def basepage():
    return render_template("basepage.html")


app.run()
