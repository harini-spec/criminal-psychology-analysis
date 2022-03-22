from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def start():

    name = request.values.get("name")
    gender = request.values.get("gender")
    age = request.values.get("age")
    profession = request.values.get("profession")
    review = request.values.get("review")
    movies = request.form.get("movies")

    print (name, gender, age, profession, review, movies)

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
