from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#Allowing mongo to be used in flask - use mars_app - is the identical code in mongodb
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_app")


@app.route("/")
def init_browser():
    #
    mars_data_db = mongo.db.mars_collection.find_one()


    return render_template("index.html", mars = mars_data_db)

@app.route("/scrape")
def scrape():


    mars_data = scrape_mars.scrape_info()


    mongo.db.mars_collection.update({}, mars_data, upsert = True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)
