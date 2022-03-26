from flask import Flask, render_template, request
from model_maker import predict_emotion
from pymongo import MongoClient
import os


app = Flask(__name__)

MONGO_URI           = os.environ.get('MONGO_URI')

client = MongoClient(MONGO_URI)  
DB_NAME = 'movie_reviews_emotion'
database = client[DB_NAME]

@app.route('/', methods = ['GET', 'POST'])
def start():

    name = request.values.get("name")
    gender = request.values.get("gender")
    age = request.values.get("age")
    profession = request.values.get("profession")
    review = request.values.get("review")
    movies = request.form.get("movies")

    print (name, gender, age, profession, review, movies)

    if request.method == 'POST':

        emotion = predict_emotion(review)[0]

        review_dict = {
            'review'    : review,
            'emotion'   : emotion
        }

        collection_name = 'review_details'

        new_collection = database[collection_name]
        x = new_collection.insert_one(review_dict)
        print(x)

        return render_template('index.html', emotion = emotion)

    return render_template('index.html')

@app.route('/ping')
def ping():

    result = {
        "ping"  : "pong"
    }
    return result


if __name__== "__main__":
    app.run(host="0.0.0.0", debug = True, port = 5003)

'''

choose a movie


'''
