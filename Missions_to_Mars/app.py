from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Create an instance of flask
app = Flask(__name__)

#Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#Route to render
@app.route("/")
def home():

    #Find record of data from mongo database
    required_data = mongo.db.collection.find_one()
    #Return template and data
    return render_template("index.html", mars_info=required_data)

#Route that will scrape
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    #Update the Mongo database
    mongo.db.collection.update_one({}, {"$set": mars_data}, upsert=True)
    #Redirect to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
