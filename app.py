# Import Flask dependency
from flask import Flask


# Create a new Flask App Instance
app = Flask(__name__)


# Creating Flask Routes
@app.route('/')
def hello_world():
    return 'Hello World'


# Set the FLASK_APP environment variable to the name of our Flask file, app.py
