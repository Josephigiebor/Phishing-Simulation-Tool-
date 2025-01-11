# Phishing Simulation Tool 🚨

The **Phishing Simulation Tool** is a web-based application built using **Flask** and **SQLite** to simulate phishing attacks in a controlled environment. This tool helps organizations and individuals educate users about email security and identify human vulnerabilities to phishing attempts.

The tool tracks user interactions with phishing links and credentials submissions, logs their IP addresses, user agents, and geolocation data, and displays the results on a dashboard.

---

## 🚀 **Features**

- 📧 **Phishing Landing Page**: A fake login page to simulate a phishing attack.
- 🔗 **Phishing Link Tracking**: Tracks when users click on phishing links sent via email.
- 🔐 **Credential Submission Tracking**: Tracks credentials submitted on the phishing landing page.
- 🌍 **Geolocation Tracking**: Logs the IP address, country, and city of the user interacting with the phishing page.
- 📊 **Interactive Dashboard**: Displays logged interactions in a table with real-time updates and a search feature.

---

## 📋 **Technologies Used**

- **Python**: The backend logic.
- **Flask**: The web framework for handling routes and rendering templates.
- **SQLite**: The database to store user interactions.
- **HTML/CSS**: The front-end for the phishing pages and dashboard.
- **geopy**: A library to get geolocation data based on IP addresses.

---

## 📂 **Project Structure**

phishing-simulation-tool/ ├── app.py # Main Flask application ├── interactions.db # SQLite database file ├── /templates # HTML templates │ ├── index.html # Phishing landing page │ ├── feedback.html # Feedback page after phishing interaction │ └── dashboard.html # Dashboard to display user interactions └── /static # Static files (CSS, images, etc.)
