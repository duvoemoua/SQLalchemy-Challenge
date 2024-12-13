# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) 
    session = Session(engine)

    # Query preciptation
    recent_year = dt.date(2017, 8, 23)
    recent_year_data = recent_year - dt.timedelta(days=365)
    precip_query = session.query(measurement.date, measurement.prcp).filter(measurement.date >= recent_year_data).all()
    
    session.close()

    precip_data = []
    for date,prcp in precip_query:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_data.append(precip_dict)

    return jsonify(precip_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) 
    session = Session(engine)

    # Query stations
    stations_query = session.query(station.station).all()
   
    session.close()

    stations_list = list(np.ravel(stations_query))

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) 
    session = Session(engine)

    # Query tobs
    recent_year = dt.date(2017, 8, 23)
    recent_year_data = recent_year - dt.timedelta(days=365)
    tobs_query = session.query(measurement.date, measurement.tobs).filter((measurement.station == 'USC00519281') & (measurement.date >= recent_year_data)).all()
    session.close()

    tobs_data = []
    for date, tobs in tobs_query:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temp Observations"] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)




@app.route("/api/v1.0/<start>")
def start_date(start):
     # Create our session (link) 
    session = Session(engine)

    # Query start
    start_query = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    session.close()

    start_data = []
    for TMIN, TAVG, TMAX in start_query:
        start_dict = {}
        start_dict["TMIN"] = TMIN
        start_dict["TAVG"] = TAVG
        start_dict["TMAX"] = TMAX
        start_data.append(start_dict)

    return jsonify(start_data)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
     # Create our session (link) 
    session = Session(engine)

    # Query tobs
    start_end_query = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()

    session.close()
  
    # Create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    start_end_data = []
    for TMIN, TAVG, TMAX in start_end_query:
        start_end_stats_dict = {}
        start_end_stats_dict["TMIN"] = TMIN
        start_end_stats_dict["TAVG"] = TAVG
        start_end_stats_dict["TMAX"] = TMAX
        start_end_data.append(start_end_stats_dict) 
    

    return jsonify(start_end_data)

   
if __name__ == "__main__":
    app.run(debug=True, port=9000)







