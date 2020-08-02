
# Import Dependencies
import datetime as dt
import numpy as np
import pandas as pd 


# Importing dependencies for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# Importing dependencies that we need for Flask
from flask import Flask, jsonify


# Setting up the database
engine = create_engine("sqlite:///hawaii.sqlite")


# Access and query our SQLite database file
Base = automap_base()


# Reflecting the database
Base.prepare(engine, reflect=True)


# Saving the references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create a session link from Python to the database
session = Session(engine)


# Setting up Flask
app = Flask(__name__)


# Creating Welcome route
@app.route("/")

# Creating a welcome function with a return statement
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')


# Setting up Precipitation route
@app.route("/api/v1.0/precipitation")

# Creating a precipitation function
def precipitation():
    # Defining previous year variable
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query to get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # Creating dictionary with date as the key and precipitation as the value
    precip ={date:prcp for date, prcp in precipitation}
    return jsonify(precip)


# Creating a Stations route
@app.route("/api/v1.0/stations")

# Creating a stations function
def stations():
    # Creating a query to get all the stations in our database
    results = session.query(Station.station).all()
    # Converting results to list using list() function and then jsonify the list
    stations = list(np.ravel(results))
    return jsonify (stations=stations)


# Creating Monthly Temperature route
@app.route("/api/v1.0/tobs")

# Creating a monthly temperature function
def temp_montly():
    # Creating a variable for previous date
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        # Unravel the results into a one-dimensional array and make list.
        # The jsonify list and return the results
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Creating a Statistics route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Creating statistics function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    else:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

