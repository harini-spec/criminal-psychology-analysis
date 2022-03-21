Skip to content
Search or jump to…
Pull requests
Issues
Marketplace
Explore
 
@harini-spec 
harini-spec
/
flood-detection
Private
Code
Issues
Pull requests
Actions
Projects
Security
Insights
Settings
flood-detection/model_maker.py /
@harini-spec
harini-spec streamlit model for flood prediction added
Latest commit bfb8ccf 9 days ago
 History
 1 contributor
93 lines (63 sloc)  2.64 KB
  
import random
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import os.path
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score,cross_val_predict
from sklearn.linear_model import LogisticRegression

CSV_FILE_PATH       = 'chennai.csv'
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
        
        X= df.iloc[:,0:1]
        Y= df.iloc[:,-1]

        minmax = preprocessing.MinMaxScaler(feature_range=(0,1))
        minmax.fit(X).transform(X)

        x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.2)

        x_train_std=minmax.fit_transform(x_train)         # fit the values in between 0 and 1.
        y_train_std=minmax.transform(x_test)
        
        local_model                      = linear_model.LogisticRegression()
        clf                              = local_model.fit(x_train,y_train)

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

    def classify_single_predict(self, temp):

        predicted_value = self.model.predict([temp])

        return predicted_value

def startpy():
    
    s = MLSingleton.getInstance()
    print(s.classify_single_predict([3248.6]))

if __name__ == "__main__":
    startpy()
© 2022 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
Loading complete