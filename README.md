Jharkhand Tourism — Prototype

This is a simple prototype of a tourism website for Jharkhand, India. It’s built with Django and helps users explore tourist places, manage personal dashboards, and even interact with an AI chatbot for guidance. Admins can manage destinations and monitor user activity.

Features

For Users:

Sign up, log in, and manage your personal dashboard.

Explore tourist places with ratings and reviews.

Access an SOS button for emergencies.

Chat with an AI bot for help and guidance.

For Admins:

View and manage all users and tourist destinations.

Approve, edit, or delete places.

Monitor activity on the platform.

Tech Stack

Backend: Django 5.2.6

Frontend: HTML, CSS, Bootstrap 5

Database: SQLite (default)

Extras: AI Chatbot and SOS alert

How to Run Locally

Clone the repository:

git clone https://github.com/ankit12p/jharkhand_tourism.git
cd jharkhand_tourism


Create and activate a virtual environment:

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Run migrations:

python manage.py migrate


Start the development server:

python manage.py runserver


Open http://127.0.0.1:8000
 in your browser to see the site.

How It Works

Users can explore tourist places, see ratings, and get recommendations.

The SOS button is visible only to logged-in users for emergencies.

The AI chatbot helps users navigate the website and answer questions.

Admins can manage all content and user activity from their dashboard.

Contributing

If you want to contribute, feel free to fork the repository, make changes, and send a pull request.

License

This project is a prototype for learning and demonstration purposes.
