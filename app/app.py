from flask import Flask, render_template
from flask_restful import Api
import os
from api.faceit_stats import FaceitStats

app = Flask(__name__)
api = Api(app)
api.add_resource(FaceitStats, '/api/faceit/stats')

@app.route("/", methods=['GET', 'POST'])
def faceit(): 
    return render_template('faceit.html')

@app.errorhandler(404)
def page_not_found(e):
    return "404 дурак"

if __name__ == "__main__": 
    app.secret_key = os.urandom(24)
    app.run(debug=True, host="127.0.0.1", port="3000")