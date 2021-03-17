import numpy as np 
import pandas as pd 
import datetime as dt 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date (write as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start_date/end_date (write as YYYY-MM-DD/YYYY-MM-DD)<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query Results
    results = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date)

    # Convert the query results to a dictionary using date as the key and prcp as the value.
    precipitation_date_tobs = []
    for each_row in results:
        dt_dict = {}
        dt_dict["date"] = each_row.date
        dt_dict["tobs"] = each_row.tobs
        precipitation_date_tobs.append(dt_dict)

    # Return the JSON representation of your dictionary.
    return jsonify(precipitation_date_tobs)

@app.route("/api/v1.0/stations")
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query Stations
    results = session.query(Station.name).all()

    # Return a JSON list of stations from the dataset.
    station_list = list(np.ravel(results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create session (link) from Python to the DB
    session = Session(engine)

# Query the dates and temperature observations of the most active station for the last year of data.
 
    #Query the latest_date and query_start_date
    last_year = dt.date(2017,8,23) - dt.timedelta(days=366)
    
    # Query station names and their observation counts, then select the most active station
    tobs_data = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= last_year).order_by(Measurement.date).all()  
    
    # Return list of tobs for the year before the final date
    tobs_data_list = list(tobs_data)

    # Return JSON results
    return jsonify(tobs_data_list)

@app.route("/api/v1.0/<start>")
def start_day(start):
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Define TMIN, TAVG, and TMAX
    start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start).group_by(Measurement.date).all()

    # Create List
    start_day_list = list(start_day)

    # Return JSON Results
    return jsonify(start_day_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Define TMIN, TAVG, TMAX
    start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()

    # Create List
    start_end_day_list = list(start_end_day)

    # Return JSON Results
    return jsonify(start_end_day_list)




if __name__ == "__main__":
    app.run(debug=True)