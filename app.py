import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station
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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"                
        
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
  
    
    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    results = session.query(measurement.date, measurement.prcp).all()
    
    results = dict(results)

    session.close()

    return jsonify(results)



@app.route("/api/v1.0/stations")
def stations():
    #Return a JSON list of stations from the dataset.
    session = Session(engine)
    # Query all stations
    results = session.query(station.station).all()
    #Converting the tuple into a list
    results = [s[0] for s in results]
    
    session.close()
    return jsonify(results)
    
@app.route("/api/v1.0/tobs")
def tobs():
    #query for the dates and temperature observations from a year from the last data point.
    session = Session(engine)

    results = session.query(measurement.tobs).filter(measurement.date>="2016-08-23").all()
      
    #Converting the tuple into a list
    results = [s[0] for s in results]

    session.close()

    return jsonify(results)

    

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start = None, end = None):
    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start
    session = Session(engine)
    
    if not end:
        # calculate TMIN, TAVG, TMAX for dates greater than start
        results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).all()
        
        return jsonify(results[0])
    
    else: 
    
        # calculate TMIN, TAVG, TMAX with start and end dates
        results= 
        session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).all()

        session.close()

        return jsonify(results[0])

if __name__ == '__main__':
    app.run(debug=True)
