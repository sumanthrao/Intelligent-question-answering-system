import os
from flask import Flask, render_template
from route import *
app = Flask(__name__)
app._static_folder = os.path.join(os.getcwd(),"static")

@app.route('/')
def index():
	return route_index() 

if (__name__ == "__main__"):
    app.run(debug=True)