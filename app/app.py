import flask
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from modules.test import Steam
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
api = Api(app)


@app.route("/progs")
def prog_list():
    return render_template("progs.html")  

@app.route("/faceit", methods=['GET', 'POST'])
def faceit(): 
    if flask.request.method == 'POST': 
        steam_link = request.form.get('steam_link', "").strip()
        steamid = Steam(steam_link).get_id()
    return render_template("faceit.html")  

@app.route("/")
def start():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return "404 дурак"

if __name__ == "__main__": 
    app.secret_key = os.urandom(24)
    app.run(debug=True, host="127.0.0.1", port="3000")