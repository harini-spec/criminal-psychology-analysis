import random
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import os.path
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score,cross_val_predict
from sklearn.linear_model import LogisticRegression
import seaborn as sns
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
import neattext.functions as nfx
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer



CSV_FILE_PATH       = 'merged_dataset.csv'
MODEL_PICKLE_PATH   = 'model_reg.pkl'
# VECTOR_PICKLE_PATH  = 'count_vect_5.pkl'

class MLSingleton:

    __instance = None

    def __init__(self):
        """ Virtually private constructor. """
        if MLSingleton.__instance != None:
            raise Exception("This class is a singleton!")

        self.model_name         = MODEL_PICKLE_PATH

        try:
            # Load models from pickle
            self.model              = pickle.load(open(self.model_name, 'rb'))

        except FileNotFoundError as file_err:
            print('Error while loading pickles : ', file_err)

            # Train model
            self.train_model()

        # print('Loaded model and vectorizer')

        MLSingleton.__instance = self

    def train_model(self, force = False):

        if(not force):

            print(f'{MODEL_PICKLE_PATH} available? : ', os.path.isfile(MODEL_PICKLE_PATH))
            if(os.path.isfile(MODEL_PICKLE_PATH)):
                print('Skipped as the file is already there')
                return

        print('Training fresh model and dumping pickle')

        df = pd.read_csv(CSV_FILE_PATH)
        df = df[df.Emotion != "joy"]
        df['Clean_Text'] = df['Text'].apply(nfx.remove_userhandles)
        df['Clean_Text'] = df['Clean_Text'].apply(nfx.remove_stopwords)

        Xfeatures = df['Clean_Text']
        ylabels = df['Emotion']

        x_train,x_test,y_train,y_test = train_test_split(Xfeatures,ylabels,test_size=0.3,random_state=42)

        # vectorizer = CountVectorizer()
        # X = vectorizer.fit_transform(ex)

        pipe_lr     =       Pipeline(steps=[('cv',CountVectorizer()),('lr',LogisticRegression())])
        clf         =       pipe_lr.fit(x_train,y_train)
        # pipe_lr.predict([ex1])
        
        # local_model                      = linear_model.LogisticRegression()
        # clf                              = local_model.fit(x_train,y_train)

        pickle.dump(clf, open(MODEL_PICKLE_PATH, 'wb'))
        print('Dumped model into ', MODEL_PICKLE_PATH)

        # as fresh model created apply them
        self.model              = pickle.load(open(self.model_name, 'rb'))

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if MLSingleton.__instance == None:
            MLSingleton()

        return MLSingleton.__instance

    def classify_single_predict(self, ex):

        predicted_value = self.model.predict(ex)

        return predicted_value

def startpy():
    
    s = MLSingleton.getInstance()
    # train the model
    # s.train_model(force=True)
    # ex = ["Rape is a serious crime and people have to take a careful note on it", "Movie contains lots of gore scenes.", "He need justice because it is completely unfair to him", "Movie contains lots of gore scenes. I particularly did not feel good about it", "Ted Bundy was a nasty guy. He needs to be punished"]
    ex = ["Rape is a serious crime and people have to take a careful note on it"]
    print(s.classify_single_predict(ex))

if __name__ == "__main__":
    startpy()