from flask import Flask, request, redirect, url_for, flash, render_template
from tinydb import TinyDB, Query, where
import numpy as np
import re
import json
import copy
from app.processtools import *

app = Flask(__name__)
db = TinyDB('db.json')

def get_collection(data):
    collection = {}
    for k, v in data.items():
        ks = k.split('_')
        if ks[0] == 'name':
            collection[v] = data['type_' + ks[1]]
        elif k == 'template_name':
            collection['name'] = v
    return collection


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/add_form', methods=["POST"])
def add_form():
    if request.method == "POST":
        data = get_collection(request.form.to_dict())
        db.insert(data)
        return "new tamplete was added"
    
@app.route('/get_form', methods=["POST"])
def get_form():
    if request.method == "POST":
        data = get_collection(request.form.to_dict())
        orig_dict = copy.deepcopy(data)
        return search(data)
 
    
@app.route("/db_structure")
def db_structure():
    return db.all()
        
