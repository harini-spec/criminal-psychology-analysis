import streamlit as st
import pickle
import numpy as np

model = pickle.load(open('model_reg.pkl','rb'))

st.title("Emotion prediction")

def main():
    st.subheader("Enter your text")
    title = st.text_input('', 'Review')

    res = model.predict([title])
    st.code(res[0])

if __name__ == "__main__":
    main()