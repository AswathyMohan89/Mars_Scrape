from flask import Flask, render_template, jsonify,redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)


@app.route('/')
def index():
    # @TODO
    # Create a route and view function that:
    # 1. returns one document from your mongo db
    # 2. renders an index.html template with that data
    # CODE GOES HERE
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", listings=mars_data)
    return


@app.route('/scrape')
def scrape():
    # @TODO
    # 1. find the collection that you are going to insert scraped data to and set it to a variable.
    # 2. scrape your url here, and set it to a variable. Hint: You will be calling a function from scrape.py.
    # 3. update your database with your new data.
    # 4. redirect your url back to the route.
    mars_data = mongo.db.mars_data
    listings_data = scrape_mars.scrape1()
    mars_data.update(
        {},
        listings_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)

    


if __name__ == "__main__":
    app.run(debug=True)
