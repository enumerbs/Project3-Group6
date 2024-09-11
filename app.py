# Import the dependencies.
import numpy as np
import pandas as pd
import json

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text

from flask import Flask, jsonify, request

#################################################
# Database Setup
#################################################

# Create engine using the `DataApi.db` database file
engine = create_engine("sqlite:///db/DataApi.db")

# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the variables to represent the database tables
CountryContinent = Base.classes.CountryContinent
PopulationGrowth = Base.classes.PopulationGrowth

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available API routes"""
    return (
        f"<h1>Welcome to the Global Data Analysis API</h1>"
        f"<h2>Available Routes:</h2>"

        f"<h3><u>Reference Data</u></h3>"

        f"<p><b>/api/v1.0/country-codes</b></br>\
        All country codes sorted alphabetically</p>"

        f"<p><b>/api/v1.0/continents-with-countries</b></br>\
        All continents and countries in them, sorted alphabetically by the respective names</p>"

        f"<h3><u>Population Growth Percentage Data</u></h3>"

        f"<p><b>/api/v1.0/population-growth-percentage-years-available</b></br>\
        A list of years for which population growth percentage data is available</p>"

        f"<p><b>/api/v1.0/population-growth-percentage-all-countries-all-years</b></br>\
        A cross-tabulation of population growth percentage by country, by year for all available years</p>"

        f"<p><b>/api/v1.0/population-growth-percentage-for-country-all-years-available/&lt;country_code&gt;</b></br>\
        Population growth percentage by country, by year for all years available for that country</br>\
        Example:</br>\
        /api/v1.0/population-growth-percentage-for-country-all-years-available/AUS</p>"

        f"<p><b>/api/v1.0/population-growth-percentage-summary-by-continent/&lt;year&gt;</b></br>\
        Return MIN, AVG, and MAX population growth by continent for the specified year</p>"
    )

#------------------------------------------------
# Reference Data endpoints
#------------------------------------------------

@app.route("/api/v1.0/country-codes")
def country_codes():
    """Return a list of all country codes sorted alphabetically"""
    # Query for country codes
    session = Session(bind=engine)
    country_tuples = session.query(CountryContinent.CountryCode).order_by(CountryContinent.CountryCode).all()
    session.close()

    # Convert list of tuples into normal list
    country_codes = list(np.ravel(country_tuples))

    # Return result in JSON format
    return jsonify(country_codes)

#------------------------------------------------

@app.route("/api/v1.0/continents-with-countries")
def continents_with_countries():
    """Return a list of all continents and countries in them, sorted alphabetically by the respective names"""
    # Query for continent/country information
    # NOTE: we use the country name from the population growth table, so that name is consistent with other country name values
    # returned from other endpoints in this API.
    session = Session(bind=engine)
    result_records = session.query(CountryContinent.Continent, PopulationGrowth.CountryName, CountryContinent.CountryCode)\
                            .join(PopulationGrowth, CountryContinent.CountryCode == PopulationGrowth.CountryCode)\
                            .order_by(CountryContinent.Continent, PopulationGrowth.CountryName)\
                            .all()
    session.close()

    # Convert tuples to dataframe taking on column names from the query
    result_df = pd.DataFrame(result_records)

    # Convert to a dictionary and return result
    return result_df.to_dict(orient="records")

#------------------------------------------------
# Population Growth dataset endpoints
#------------------------------------------------

@app.route("/api/v1.0/population-growth-percentage-years-available")
def population_growth_percentage_years_available():
    """Return a list of years for which population growth percentage data is available"""
    available_years = [column.name for column in PopulationGrowth.__table__.columns if column.name.isnumeric()]

    # Return result in JSON format
    return jsonify(available_years)

#------------------------------------------------

@app.route("/api/v1.0/population-growth-percentage-all-countries-all-years")
def population_growth_percentage_all():
    """Return a cross-tabulation of population growth percentage by country, by year for all available years"""

    # Query all population growth percentage data
    session = Session(bind=engine)
    population_growth_records = session.query(PopulationGrowth).all()
    session.close()

    # Dynamically convert query results into an equivalent dictionary
    # Reference: https://www.slingacademy.com/article/sqlalchemy-convert-query-results-into-dictionary/
    result_dict = [{column.name: getattr(row, column.name) for column in PopulationGrowth.__table__.columns} for row in population_growth_records]

     # Return result in JSON format
    return result_dict

#------------------------------------------------

@app.route("/api/v1.0/population-growth-percentage-for-country-all-years-available/<country_code>")
def population_growth_percentage_for_country(country_code):
    """Return population growth percentage for the specified country, by year for all years available for that country"""

    # Query all population growth data, filtering by the specified country code
    session = Session(bind=engine)
    population_growth_records = session.query(PopulationGrowth).filter(PopulationGrowth.CountryCode == country_code).all()
    session.close()

    # Dynamically convert query results into an equivalent dictionary
    # Reference: https://www.slingacademy.com/article/sqlalchemy-convert-query-results-into-dictionary/
    result_dict = [{column.name: getattr(row, column.name) for column in PopulationGrowth.__table__.columns} for row in population_growth_records]

     # Return result in JSON format
    return result_dict

#------------------------------------------------

@app.route("/api/v1.0/population-growth-percentage-summary-by-continent/<year>")
def min_avg_max_population_growth_percentage_by_contient_for_specified_year(year):
    """Return MIN, AVG, and MAX population growth percentage by continent for the specified year"""

    available_years = [column.name for column in PopulationGrowth.__table__.columns if column.name.isnumeric()]
    if year not in available_years:
        # Data for requested year not available: return error description to the caller; set HTTP status code 400 'Bad request'
        return {"error": f"No data available for the specified year ({year})"}, 400
    else:
        session = Session(bind=engine)
        #Creating the SQL statementby using the text()
        stmt=text("SELECT Continent, MIN([" + year + "]), AVG([" + year + "]), MAX([" + year + "]) FROM PopulationGrowth as pg "\
                "inner join CountryContinent as cc on cc.CountryCode = pg.CountryCode "\
                "where [" + year + "] <> '(Not Specified)' "\
                "group by Continent")
        result_records=session.execute(stmt)
        session.close()

        # Convert tuples to dataframe taking on column names from the query
        result_df = pd.DataFrame(result_records)

        # Convert to a dictionary and return result
        return result_df.to_dict(orient="records")

#################################################
# Support for invocation from the command line
#################################################
if __name__ == "__main__":
    app.run(debug=False)