from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

app= Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Set up App Routes
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#Set up the Scrape Route; this will update data from the homepage of our app
@app.route("/scrape")
def scrape():
    #where to look
    mars = mongo.db.mars
    #scrape data
    mars_data = scraping.scrape_all()
    #update database; 
        #add an empty json fie, db, create a new document if one does not exist
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"

if __name__ == "__main__":
    app.run()