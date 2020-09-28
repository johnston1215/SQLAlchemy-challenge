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
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<Start_YYYY-MM-DD>/<End_YYYY-MM-DD>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all records
    PrcpTbl = session.query(Measurement.date,Measurement.prcp).group_by(Measurement.date).order_by(Measurement.date).all()
   
    all_precips = []
    for date, precip, in PrcpTbl:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = precip
        all_precips.append(precip_dict)
    session.close()

    # Convert list of tuples into normal list
    SumTbl = list(np.ravel(all_precips))

    return jsonify(SumTbl)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    stations = session.query(Measurement.station).group_by(Measurement.station).all()

    return jsonify(stations)
    session.close()


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query TOBS for last year for most active station USC00519281
    TOBS = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-24').all()

    return jsonify(TOBS)
    session.close()

if __name__ == '__main__':
    app.run(debug=True)
