
from flask import render_template, redirect, url_for, request, session, flash
import json

def route_index():
    return render_template("index.html")

def route_result():

    return render_template("results.html")

def route_question(questions):
    return render_template("qa.html",questions = questions)

def route_depr_results(answers):

    d = json.loads(answers)
    print(d,type(d))
    return render_template("index.html")