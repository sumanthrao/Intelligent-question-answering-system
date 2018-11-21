
from flask import render_template, redirect, url_for, request, session, flash

def route_index():
    return render_template("index.html")

def route_result():

    return render_template("results.html")
