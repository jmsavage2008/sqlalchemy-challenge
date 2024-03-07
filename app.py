# Import the dependencies.
from flask import Flask
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np
from numpy import mean, min, max
import pandas as pd
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################


#Create an App
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Define Routes
@app.route("/")
def welcome():
    """List all available routes"""
    return (f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/&lt;start&gt;<br/>"
            f"/api/v1.0/&lt;start&gt;/&lt;end&gt;")

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation data"""
    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017, 8, 23)-dt.timedelta(days=365)
    year_ago

    # Perform a query to retrieve the data and precipitation scores
    measure = session.query(Measurement).\
    filter(Measurement.date >= year_ago).\
    order_by(Measurement.date).all()

    
    #Create list of dictionaries
    list_=[]
    for row in measure:
        list_.append({"Date": row.date, "Precipitation": row.prcp})
   
    session.close()

    #JSONify it
    return jsonify(list_)

@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    
    # List the stations.
    station_query = session.query(Station.station, Station.name, Station.latitude,
                                 Station.longitude, Station.elevation)
    station_query
    
    #Create list of dictionaries
    list_2=[]
    for row in station_query:
        list_2.append({"Station Number": row.station, "Station Name": row.name,
                      "Latitude": row.latitude, "Longitude": row.longitude, 
                      "Elevation": row.elevation})
   
    
    session.close()
    
    return jsonify(list_2)

@app.route("/api/v1.0/tobs")
def tobs():
   
                    
     # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Temp Data"""
    # Find last date
    session.query(Measurement.date).\
        filter(Measurement.station == "USC00519281").\
        order_by(Measurement.date.desc()).first()
    
    #Find temp from a year ago
    temp_year_ago = dt.date(2017, 8, 18)-dt.timedelta(days=365)

    #Query year ago info based on temp
    year_ago_temps = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= temp_year_ago).\
        filter(Measurement.station == "USC00519281").\
        order_by(Measurement.date).all()

    #Create list of dictionaries
    list_3=[]
    for row in year_ago_temps:
        list_3.append({"Date": row.date, "Observed Temperature": row.tobs})
   
        
    session.close()
    
    return jsonify(list_3)
            
@app.route("/api/v1.0/<start>")
def start_date(start):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Temp Data"""
    # Find last date
    session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()

    #Query data by start date
    temps = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start).\
        order_by(Measurement.date).all()

    #Create list of dictionaries
    list_4=[]
    list_5=[]
    for row in temps:
        list_4.append({"Date": row.date, "Observed Temperature": row.tobs})
        list_5.append(row.tobs)
    
    avg_temp = mean(list_5)
    min_temp = min(list_5)
    max_temp = max(list_5)
    
    stats_dict = {"Minimum Temp": min_temp, "Maximum Temp": max_temp, 
                 "Average Temp": avg_temp}
    return jsonify(stats_dict)
   
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Temp Data"""
    # Find last date
    session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    
    #Query data by start and end temp
    temps = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        order_by(Measurement.date).all()

    #Create list of dictionaries
    list_4=[]
    list_5=[]
    for row in temps:
        list_4.append({"Date": row.date, "Observed Temperature": row.tobs})
        list_5.append(row.tobs)
    avg_temp = mean(list_5)
    min_temp = min(list_5)
    max_temp = max(list_5)
    
    stats_dict = {"Minimum Temp": min_temp, "Maximum Temp": max_temp, 
                 "Average Temp": avg_temp}
    return jsonify(stats_dict)

if __name__ == "__main__":
    app.run(debug=False)