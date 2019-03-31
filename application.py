#!/usr/bin/python
"""
Project 2: Udacity Flask Items/Categories Project
Author: David Nadwodny

Some Concept inspired by/taxken from:
    http://flask.pocoo.org/docs/1.0/tutorial/database/
    http://flask.pocoo.org/docs/1.0/appcontext/

"""
import random, string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, Category, User

from flask import Flask, request, redirect, jsonify, url_for
from flask import session as login_session
from flask import render_template
from apiclient import discovery
import httplib2
from oauth2client import client
import json

app = Flask(__name__)

CLIENT_SECRET_FILE = 'client_secrets.json'
CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Itemify"
app.secret_key = "super secret key"

engine = create_engine(
    'sqlite:///items.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# helper funtion that sets the state
def getSession():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))
    login_session['state'] = state


# main landing view
@app.route('/')
def landing():

    categories = session.query(Category).all()
    session.commit()
    items = session.query(Item).all()
    session.commit()
    return render_template(
        'index.html',
        categories=categories,
        items=items,
        session_id=login_session['state'])


@app.route('/test')
def test():
    return render_template('login.html')


@app.route('/auth', methods=['POST'])
def auth():

    # Grab state here
    login_session['state'] = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))
    if request.method == 'POST':

        # get auth code out of request.data
        auth_code = request.data

        # CSRF protection. Redirect if bad
        if not request.headers.get('X-Requested-With'):
            return redirect(url_for('landing'))

        # Exchange auth code for access token, refresh token, and ID token
        credentials = client.credentials_from_clientsecrets_and_code(
            CLIENT_SECRET_FILE, [
                'https://www.googleapis.com/auth/drive.appdata', 'profile',
                'email'
            ], auth_code)

        # Get profile info from ID token
        userid = credentials.id_token['sub']
        email = credentials.id_token['email']
        name = credentials.id_token['name']
        return userid + " " + email + " " + name


# lists all categories and list of latest items
# authenticated users can add items

# Category Detail view
# lists all items that are in a category
# authenticated users may edit / delete

# Item Detail view
# shows details of a specific item
# authenticated users may edit / delete

# JSON endpoint for entire list
