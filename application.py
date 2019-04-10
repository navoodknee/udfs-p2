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


# used to determine if we need to hide or unhide the buttons
def userLoggedIn():
    try:
        login_session['email']
        print("logged in")
        return True
    except KeyError:
        print("not... loged in")
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

    # Are we logged in?
    if(userLoggedIn()):
        loggedIn = True
    else:
        loggedIn = False
        print("loggedIn is False")

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
        state=state,
        loggedIn=loggedIn)


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
            userCount = session.query(User).filter_by(email=login_session['email']).count()
            print("userCount is %s", userCount)
            if(userCount < 1):
                newUser = User(email=login_session['email'])
                session.add(newUser)
                session.commit()
                return "New User " + login_session['userid'] + " Logged in"
            else:
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

    # Are we logged in?
    if(userLoggedIn()):
        loggedIn = True
    else:
        loggedIn = False
        print("loggedIn is False")

    # Get all the categories
    categories = session.query(Category).all()
    session.commit()
    # Get all the items in reverse order
    items = session.query(Item).filter_by(item_id=category_id)
    session.commit()
    return render_template(
       'category_view.html',
       categories=categories,
       items=items,
       state=state,
       loggedIn=loggedIn)

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
    # Are we logged in?
    if(userLoggedIn()):
        loggedIn = True
    else:
        loggedIn = False
        print("loggedIn is False")
    # Get all the categories
    categories = session.query(Category).all()
    session.commit()

    item = session.query(Item).get(item_id)
    session.commit()
    return render_template(
        'item_view.html',
        categories=categories,
        item=item,
        state=state,
        loggedIn=loggedIn)


# My items interface
@app.route('/myitems/')
def my_items():
    # New session..
    try:
        state = login_session['state']
    except KeyError:
        state = setSession()

    # Get all the categories
    categories = session.query(Category).all()
    session.commit()

    # Get all the items in reverse order
    items = session.query(Item).order_by(desc(Item.id))
    session.commit()
    # Are we logged in?
    if(userLoggedIn()):
        loggedIn = True
    else:
        loggedIn = False
        print("loggedIn is False - Redirecting")
        return render_template(
            'index.html',
            categories=categories,
            items=items,
            state=state,
            loggedIn=loggedIn)
    # Get user info
    try:
        user = session.query(User).filter_by(email=login_session['email']).one()
        session.commit()
        print("login_session email is %s" % login_session['email'])
        print("user is %s" % user)
        # Get user categories
        userCategories = session.query(Category).filter_by(user_id=user.id)
        session.commit()
        # Get user Items
        userItems = session.query(Item).filter_by(user_id=user.id)
        session.commit()
    except:
        print("login_session email is %s" % login_session['email'])
        print("user is %s" % user)
        userCategories = None
        userItems = None
    return render_template(
       'myitems_view.html',
       userCategories=userCategories,
       userItems=userItems,
       categories=categories,
       state=state,
       loggedIn=loggedIn)

@app.route('/myitems/category/new/', methods=['GET', 'POST'])
def newCategory():
    # New session..
    try:
        state = login_session['state']
    except KeyError:
        state = setSession()

    # Get all the categories
    categories = session.query(Category).all()
    session.commit()

    # Get all the items in reverse order
    items = session.query(Item).order_by(desc(Item.id))
    session.commit()
    # Are we logged in? If not, we shouldn't be here... back to start
    if(userLoggedIn()):
        loggedIn = True
        user = session.query(User).filter_by(email=login_session['email']).one()
        session.commit()
    else:
        loggedIn = False
        print("loggedIn is False - Redirecting")
        return render_template(
            'index.html',
            categories=categories,
            items=items,
            state=state,
            loggedIn=loggedIn)

    if request.method == 'POST':
        newCategory = Category(name=request.form['name'], user_id=user.id)
        session.add(newCategory)
        session.commit()
        return redirect(url_for('my_items'))
    else:
        return render_template(
            'newCategory_view.html',
            categories=categories,
            items=items,
            state=state,
            loggedIn=loggedIn)

@app.route('/myitems/category/edit/<int:category_id>/', methods=['GET', 'POST'])
def editCategory(category_id):
    # New session..
    try:
        state = login_session['state']
    except KeyError:
        state = setSession()

    # Get all the categories
    categories = session.query(Category).all()
    session.commit()

    # Get all the items in reverse order
    items = session.query(Item).order_by(desc(Item.id))
    session.commit()
    # Are we logged in? If not, we shouldn't be here... back to start
    if(userLoggedIn()):
        loggedIn = True
    else:
        loggedIn = False
        print("loggedIn is False - Redirecting")
        return render_template(
            'index.html',
            categories=categories,
            items=items,
            state=state,
            loggedIn=loggedIn)

    editCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':

        if(request.form['name']):
            editCategory.name = request.form['name']
            session.commit()
        return redirect(url_for('my_items'))
    else:
        return render_template(
            'editCategory_view.html',
            category_id=editCategory.id,
            editCategory=editCategory,
            categories=categories,
            items=items,
            state=state,
            loggedIn=loggedIn)

@app.route('/myitems/category/delete/<int:category_id>/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    # New session..
    try:
        state = login_session['state']
    except KeyError:
        state = setSession()

    # Get all the categories
    categories = session.query(Category).all()
    session.commit()

    # Get all the items in reverse order
    items = session.query(Item).order_by(desc(Item.id))
    session.commit()
    # Are we logged in? If not, we shouldn't be here... back to start
    if(userLoggedIn()):
        loggedIn = True
        user = session.query(User).filter_by(email=login_session['email']).one()
    else:
        loggedIn = False
        print("loggedIn is False - Redirecting")
        return render_template(
            'index.html',
            categories=categories,
            items=items,
            state=state,
            loggedIn=loggedIn)

    deleteCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        # test to make sure this record belongs to the logged in user
        if(deleteCategory.user_id == user.id):
            session.delete(deleteCategory)
            session.commit()
        else:
            print("[!] Delete category uid was not equal to logged in user")
        return redirect(url_for('my_items'))
    else:
        return render_template(
            'deleteCategory_view.html',
            category_id=deleteCategory.id,
            deleteCategory=deleteCategory,
            categories=categories,
            items=items,
            state=state,
            loggedIn=loggedIn)
@app.route('/myitems/itemy/new/', methods=['GET', 'POST'])
def newItem():
    # New session..
    try:
        state = login_session['state']
    except KeyError:
        state = setSession()

    # Get all the categories
    categories = session.query(Category).all()
    session.commit()

    # Get all the items in reverse order
    items = session.query(Item).order_by(desc(Item.id))
    session.commit()
    # Are we logged in? If not, we shouldn't be here... back to start
    if(userLoggedIn()):
        loggedIn = True
        user = session.query(User).filter_by(email=login_session['email']).one()
        session.commit()
    else:
        loggedIn = False
        print("loggedIn is False - Redirecting")
        return render_template(
            'index.html',
            categories=categories,
            items=items,
            state=state,
            loggedIn=loggedIn)
        session.commit()
    userCategories = session.query(Category).filter_by(user_id=user.id)
    if request.method == 'POST':
        #
        category = session.query(Category).filter_by(name=request.form['category']).one()
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            user_id=user.id,
            item_id=category.id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('my_items'))
    else:
        return render_template(
            'newItem_view.html',
            userCategories=userCategories,
            categories=categories,
            items=items,
            state=state,
            loggedIn=loggedIn)
@app.route('/myitems/item/edit/<int:item_id>/', methods=['GET', 'POST'])
def editItem(item_id):
    # New session..
    try:
        state = login_session['state']
    except KeyError:
        state = setSession()

    # Get all the categories
    categories = session.query(Category).all()
    session.commit()

    # Get all the items in reverse order
    items = session.query(Item).order_by(desc(Item.id))
    session.commit()
    # Are we logged in? If not, we shouldn't be here... back to start
    if(userLoggedIn()):
        loggedIn = True
        user = session.query(User).filter_by(email=login_session['email']).one()
        session.commit()
    else:
        loggedIn = False
        print("loggedIn is False - Redirecting")
        return render_template(
            'index.html',
            categories=categories,
            items=items,
            state=state,
            loggedIn=loggedIn)
    editItem = session.query(Item).filter_by(id=item_id).one()
    userCategories = session.query(Category).filter_by(user_id=user.id)
    if request.method == 'POST':
        category = session.query(Category).filter_by(name=request.form['category']).one()
        if(request.form['name']):
            editItem.name = request.form['name']
            editItem.description = request.form['description']
            editItem.item_id = category.id
            session.commit()
        return redirect(url_for('my_items'))
    else:
        return render_template(
            'editItem_view.html',
            userCategories=userCategories,
            item_id=editItem.id,
            editItem=editItem,
            categories=categories,
            items=items,
            state=state,
            loggedIn=loggedIn)

@app.route('/myitems/item/delete/<int:item_id>/', methods=['GET', 'POST'])
def deleteItem(item_id):
    # New session..
    try:
        state = login_session['state']
    except KeyError:
        state = setSession()

    # Get all the categories
    categories = session.query(Category).all()
    session.commit()

    # Get all the items in reverse order
    items = session.query(Item).order_by(desc(Item.id))
    session.commit()
    # Are we logged in? If not, we shouldn't be here... back to start
    if(userLoggedIn()):
        loggedIn = True
        user = session.query(User).filter_by(email=login_session['email']).one()
        session.commit()
    else:
        loggedIn = False
        print("loggedIn is False - Redirecting")
        return render_template(
            'index.html',
            categories=categories,
            items=items,
            state=state,
            loggedIn=loggedIn)

    deleteItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        # test to make sure this record belongs to the logged in user
        if(deleteItem.user_id == user.id):
            session.delete(deleteItem)
            session.commit()
        else:
            print("[!] Delete item uid was not equal to logged in user")
        return redirect(url_for('my_items'))
    else:
        return render_template(
            'deleteItem_view.html',
            item_id=deleteItem.id,
            deleteItem=deleteItem,
            categories=categories,
            items=items,
            state=state,
            loggedIn=loggedIn)
# JSON endpoint for entire list
