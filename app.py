from django.shortcuts import render
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
def home():


    return render_template('home.html')

@app.route('/movie-list', methods = ['GET', 'POST'])
def movie_list():


    return render_template('movie_list.html')

@app.route('/review', methods = ['GET', 'POST'])
def review():

    movie = request.values.get('movie-choice')
    print(movie)

    return render_template('index.html', movie = movie)



@app.route('/submit', methods = ['GET', 'POST'])
def submit():

    if request.method == 'POST':

        movie = request.values.get('movie_name')
        name = request.values.get("name")
        age = request.values.get("age")
        profession = request.values.get("profession")
        review = request.values.get("review")
        gender = request.form.get("gender")
        genre = request.form.get("genre")
        status = request.form.get("status")

        emotion = predict_emotion(review)[0]
        # print(emotion)

        result_dict = {
            'movie'         : movie,
            'name'          : name,
            'age'           : age,
            'profession'    : profession,
            'review'        : review,
            'gender'        : gender,
            'genre'         : genre,
            'marital_status': status,
            'emotion'       : emotion
        }

        print(result_dict)

        collection_name = 'review_details'

        new_collection = database[collection_name]
        x = new_collection.insert_one(result_dict)
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
