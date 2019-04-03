#!/usr/bin/python
"""
Project 2: Udacity Flask Items/Categories Project
Author: David Nadwodny

Some Concept inspired by/taxken from:
    http://flask.pocoo.org/docs/1.0/tutorial/database/
    http://flask.pocoo.org/docs/1.0/appcontext/

"""
import random, string
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Item, Category, User

from flask import Flask, request, redirect, jsonify, url_for
from flask import session as login_session
from flask import render_template
from apiclient import discovery
import httplib2
from oauth2client import client
import json

# application config
app = Flask(__name__)
CLIENT_SECRET_FILE = 'client_secrets.json'
CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Itemify"
app.secret_key = "super secret key"

# Database / Session set up
engine = create_engine(
    'sqlite:///items.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# START Utilities
# helper function that checks sessions againts requests
def checkState(current_session, saved_session):
    if (current_session == saved_session):
        return True
    else:
        return False


# helper function that sets the state
def setSession():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))
    login_session['state'] = state
    print('%s state is', state)
    return(state)


# START VIEWS
# main landing view
# lists all categories and list of latest items
# authenticated users can add items
@app.route('/')
def landing():

    # New session..
    try:
        state = login_session['state']
    except KeyError:
        state = setSession()
        print("- %s" % login_session['state'])
    # Get all the categories
    categories = session.query(Category).all()
    session.commit()
    # Get all the items in reverse order
    items = session.query(Item).order_by(desc(Item.id))
    session.commit()
    return render_template(
        'index.html',
        categories=categories,
        items=items,
        state=state)


@app.route('/test')
def test(args_session, saved_session):
    return render_template('test.html')

# Receives AJAX from signInButton and validates google login
@app.route('/auth', methods=['POST'])
def auth():

    # validate session tokenn
    if(checkState(request.args.get('state'), login_session['state'])):
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

            # Get profile info from ID token and add to session
            login_session['userid'] = credentials.id_token['sub']
            login_session['email'] = credentials.id_token['email']
            login_session['name'] = credentials.id_token['name']

            # create new user if they aren't in our User table

            return login_session['userid'] + " Logged in"
    # Fail silently to give no useful feedback to would be attacker
    else:
        return redirect(url_for('landing'))

# Receives AJAX from signOutButton / logs user out and redirects them to /
@app.route('/logout', methods=['POST'])
def logout():

    # validate session tokenn
    if(checkState(request.args.get('state'), login_session['state'])):
        if request.method == 'POST':

            # CSRF protection. Redirect if bad
            if not request.headers.get('X-Requested-With'):
                return redirect(url_for('landing'))
            # clear out the silentl session vars
            login_session.clear()
            # just return
            return redirect(url_for('landing'))

    # Fail silently to give no useful feedback to would be attacker
    else:
        return redirect(url_for('landing'))

# Category Detail view
# lists all items that are in a category
# authenticated users may edit / delete
@app.route('/cat/<int:category_id>/')
def category_view(category_id):
    # New session..
    try:
        state = login_session['state']
    except KeyError:
        state = setSession()
        print("- %s" % login_session['state'])
    # Get all the categories
    categories = session.query(Category).all()
    session.commit()
    # Get all the items in reverse order
    items = session.query(Item).filter_by(item_id=category_id)
    session.commit()
    return render_template(
        'category_view.html', categories=categories, items=items, state=state)
# Item Detail view
# shows details of a specific item
# authenticated users may edit / delete
@app.route('/cat/<int:category_id>/item/<int:item_id>/')
def item_view(category_id, item_id):
    # New session..
    try:
        state = login_session['state']
    except KeyError:
        state = setSession()
    # Get all the categories
    categories = session.query(Category).all()
    session.commit()

    item = session.query(Item).get(item_id)
    print("item is %s" % str(item_id))
    session.commit()
    return render_template(
        'item_view.html', categories=categories, item=item, state=state)
    return(None)
# JSON endpoint for entire list
