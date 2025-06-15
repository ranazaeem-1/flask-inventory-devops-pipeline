from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
import os
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'de98652554577bbae5bf7a5909c7f7b6'  # Simple secret key for Flask sessions

# Connect directly using PyMongo client instead of Flask-PyMongo
try:
    # MongoDB Atlas connection string
    mongo_uri = 'mongodb+srv://abc:abc@cluster0.fu3wg2m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
    client = MongoClient(mongo_uri)
    
    # Test the connection
    client.admin.command('ping')
    logger.info("Connected to MongoDB Atlas successfully!")
    
    # Get database reference
    db = client.crud  # Using the 'crud' database from your successful connection
    
except Exception as e:
    logger.error(f"MongoDB connection error: {e}")
    raise RuntimeError(f"Failed to connect to MongoDB: {e}")

# Models (Helper functions for MongoDB)
def get_user_by_id(user_id):
    try:
        return db.users.find_one({'_id': ObjectId(user_id)})
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        return None

def get_user_by_username(username):
    try:
        return db.users.find_one({'username': username})
    except Exception as e:
        logger.error(f"Error getting user by username: {e}")
        return None

def get_user_by_email(email):
    try:
        return db.users.find_one({'email': email})
    except Exception as e:
        logger.error(f"Error getting user by email: {e}")
        return None

def create_user(username, email, password):
    try:
        user = {
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),
            'created_at': datetime.datetime.now()
        }
        return db.users.insert_one(user)
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return None

def check_password(user, password):
    if not user or 'password_hash' not in user:
        return False
    return check_password_hash(user['password_hash'], password)

def get_items_by_user(user_id):
    try:
        return list(db.items.find({'user_id': str(user_id)}))
    except Exception as e:
        logger.error(f"Error getting items: {e}")
        return []

def get_item_by_id(item_id):
    try:
        return db.items.find_one({'_id': ObjectId(item_id)})
    except Exception as e:
        logger.error(f"Error getting item by ID: {e}")
        return None

def create_item(name, description, quantity, user_id):
    try:
        item = {
            'name': name,
            'description': description,
            'quantity': quantity,
            'user_id': str(user_id),
            'created_at': datetime.datetime.now()
        }
        return db.items.insert_one(item)
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        return None

def update_item(item_id, name, description, quantity):
    try:
        db.items.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': {
                'name': name,
                'description': description,
                'quantity': quantity,
                'updated_at': datetime.datetime.now()
            }}
        )
        return True
    except Exception as e:
        logger.error(f"Error updating item: {e}")
        return False

def delete_item(item_id):
    try:
        db.items.delete_one({'_id': ObjectId(item_id)})
        return True
    except Exception as e:
        logger.error(f"Error deleting item: {e}")
        return False

def search_items(user_id, search_term):
    try:
        return list(db.items.find({
            'user_id': str(user_id),
            'name': {'$regex': search_term, '$options': 'i'}
        }))
    except Exception as e:
        logger.error(f"Error searching items: {e}")
        return []

def update_user_email(user_id, email):
    try:
        db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {
                'email': email,
                'updated_at': datetime.datetime.now()
            }}
        )
        return True
    except Exception as e:
        logger.error(f"Error updating user email: {e}")
        return False

# Routes
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    items = get_items_by_user(session['user_id'])
    return render_template('home.html', items=items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user_by_username(username)
        if user and check_password(user, password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if get_user_by_username(username):
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
            
        if get_user_by_email(email):
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
            
        result = create_user(username, email, password)
        if not result:
            flash('An error occurred during registration', 'danger')
            return redirect(url_for('register'))
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity = int(request.form['quantity'])
        
        result = create_item(name, description, quantity, session['user_id'])
        if not result:
            flash('An error occurred while adding the item', 'danger')
            return redirect(url_for('add_item'))
        
        flash('Item added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_item.html')

@app.route('/edit_item/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    item = get_item_by_id(item_id)
    if not item or item['user_id'] != session['user_id']:
        flash('You are not authorized to edit this item', 'danger')
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity = int(request.form['quantity'])
        
        if update_item(item_id, name, description, quantity):
            flash('Item updated successfully!', 'success')
        else:
            flash('An error occurred while updating the item', 'danger')
        return redirect(url_for('home'))
    return render_template('edit_item.html', item=item)

@app.route('/delete_item/<item_id>')
def delete_item_route(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    item = get_item_by_id(item_id)
    if not item or item['user_id'] != session['user_id']:
        flash('You are not authorized to delete this item', 'danger')
        return redirect(url_for('home'))
        
    if delete_item(item_id):
        flash('Item deleted successfully!', 'success')
    else:
        flash('An error occurred while deleting the item', 'danger')
    return redirect(url_for('home'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        search_term = request.form['search_term']
        items = search_items(session['user_id'], search_term)
        return render_template('search_results.html', items=items, search_term=search_term)
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user = get_user_by_id(session['user_id'])
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('logout'))
        
    if request.method == 'POST':
        email = request.form['email']
        
        existing_user = get_user_by_email(email)
        if existing_user and str(existing_user['_id']) != session['user_id']:
            flash('Email already registered', 'danger')
        else:
            if update_user_email(session['user_id'], email):
                flash('Profile updated successfully!', 'success')
            else:
                flash('An error occurred while updating your profile', 'danger')
        
    return render_template('profile.html', user=user)

# Update the home.html template to work with MongoDB
@app.template_filter('mongo_id')
def mongo_id_filter(obj):
    return str(obj['_id']) if obj and '_id' in obj else ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
