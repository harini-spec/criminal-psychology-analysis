# criminal-psychology-analysis

## Objective

* To predict a person’s emotion which they felt while watching a particular scene from a movie and use it for psychological study and research purposes.
* To create a more socially and mentally aware society and community where movie reviews act as a source of freedom for voicing out real and true feelings/emotions.


## Working Methodology

1. Review from the user is sent to the ML model
2. ML model predicts the emotion
3. The predicted information is sent to our database
4. Data stored in DB is sent to the psycology experts to analyse data

## Tech Stack

1. Python
2. ML Libraries
3. HTML - CSS - JS
4. MongoDB

## To run Docker 

```
sudo docker build -t myapp . 
sudo docker image ls 
sudo docker run -p 80:5000 myapp
```