#!/usr/bin/python

"""
Project 2: Udacity Flask Items/Categories Project
Author: David Nadwodny

Some Concept inspired by/taxken from:
    http://flask.pocoo.org/docs/1.0/tutorial/database/
    http://flask.pocoo.org/docs/1.0/appcontext/

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, Category, User
from flask import Flask
from flask import render_template
app = Flask(__name__)


engine = create_engine('sqlite:///items.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
# database operations
# returns database connection regardless of current state


# main landing view
@app.route('/')
def landing():

    categories = session.query(Item).all()

    output = ""
    for c in categories:
        output += c.name
        output += '</br>'
    return output
    #return render_template('index.html')


# lists all categories and list of latest items
# authenticated users can add items

# Category Detail view
# lists all items that are in a category
# authenticated users may edit / delete

# Item Detail view
# shows details of a specific item
# authenticated users may edit / delete

# JSON endpoint for entire list

