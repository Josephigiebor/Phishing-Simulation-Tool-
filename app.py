import os
from flask import Flask, request, render_template, redirect
import sqlite3
from geopy.geocoders import Nominatim

# Initialize the Flask app
app = Flask(__name__, template_folder='templates')

# Initialize the geolocator
geolocator = Nominatim(user_agent="geoapiExercises")

# Database connection function
def get_db_connection():
    try:
        conn = sqlite3.connect('interactions.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

# Function to create the interactions table if it doesn't exist
def create_table():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    action TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    country TEXT,
                    city TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database creation error: {e}")
        finally:
            conn.close()

# Call the function to create the table when the app starts
create_table()

# Function to get location details from IP address
def get_location(ip_address):
    try:
        location = geolocator.geocode(ip_address)
        if location:
            return location.address.split(", ")[-2], location.address.split(", ")[-1]
        else:
            return None, None
    except:
        return None, None

# Route for the landing page
@app.route('/')
def landing_page():
    return render_template('index.html')

# Route to track clicks on phishing links
@app.route('/track_click', methods=['GET'])
def track_click():
    email = request.args.get('email')
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    country, city = get_location(ip_address)

    if email:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO interactions (email, action, ip_address, user_agent, country, city) VALUES (?, ?, ?, ?, ?, ?)',
                    (email, 'Clicked Link', ip_address, user_agent, country, city)
                )
                conn.commit()
                print(f"Logged interaction for {email}")
            except sqlite3.Error as e:
                print(f"Database insert error: {e}")
            finally:
                conn.close()

    return render_template('feedback.html', message="You’ve been phished! Stay vigilant and avoid clicking on suspicious links.")

# Route to handle form submissions
@app.route('/track_submission', methods=['POST'])
def track_submission():
    username = request.form.get('username')
    password = request.form.get('password')
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    country, city = get_location(ip_address)

    if username and password:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO interactions (email, action, ip_address, user_agent, country, city) VALUES (?, ?, ?, ?, ?, ?)',
                    (f"Username: {username}, Password: {password}", 'Submitted Credentials', ip_address, user_agent, country, city)
                )
                conn.commit()
                print(f"Logged credentials: Username={username}, Password={password}")
            except sqlite3.Error as e:
                print(f"Database insert error: {e}")
            finally:
                conn.close()

    return render_template('feedback.html', message="Your submission has been recorded for security purposes. Please stay safe!")

# Route to show a feedback message after clicking the phishing link
@app.route('/feedback')
def feedback():
    return render_template('feedback.html', message="You’ve been phished! Stay vigilant and avoid clicking on suspicious links.")

# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    interactions = []
    unique_users = set()
    actions_tracked = 0

    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM interactions ORDER BY timestamp DESC')
        interactions = cursor.fetchall()

        # Calculate unique users and actions
        for interaction in interactions:
            unique_users.add(interaction['email'])
            actions_tracked += 1

        conn.close()

    return render_template(
        'dashboard.html',
        interactions=interactions,
        unique_users=len(unique_users),
        actions_tracked=actions_tracked
    )

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
