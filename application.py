#!/usr/bin/python

"""
Project 2: Udacity Flask Items/Categories Project
Author: David Nadwodny

"""


from flask import Flask
from flask import render_template, current_app, g
from flask.cli import with_appcontext
app = Flask(__name__)


# main landing view
@app.route('/')
def hello_world():

    return render_template('index.html')

# lists all categories and list of latest items
# authenticated users can add items

# Category Detail view
# lists all items that are in a category
# authenticated users may edit / delete

# Item Detail view
# shows details of a specific item
# authenticated users may edit / delete

# JSON endpoint for entire list
