from flask import Flask
from flask import request
from flask import render_template
import json

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def about():
    f = open("data/CommutingModes.json","r")
    data = json.load(f)
    f.close()


    return render_template('about.html')

@app.route('/macro')
def macro():
    f = open("data/CommutingModes.json","r")
    data = json.load(f)
    f.close()


    return render_template('macro.html')

@app.route('/micro/<borough>')
def micro(borough):
    f = open("data/CommutingModes.json","r")
    data = json.load(f)
    f.close()


    return render_template('micro.html',borough=borough)

app.run(debug=True, port = 1243)
