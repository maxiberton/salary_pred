import streamlit as st
import pickle
import numpy as np


def load_module():
    with open('saved_steps.pkl', 'rb') as file:
        d = pickle.load(file)
    return d


data = load_module()
random_reg = data['model']
le_country = data['le_country']
le_edu = data['le_edu']


def show_predict_page():
    st.title('Software Developer Salary Prediction')
    st.write("""### We need some information to predict the salary.""")

    countries = (
        'Australia',
        'Austria',
        'Brazil',
        'Canada',
        'France',
        'Germany',
        'India',
        'Israel',
        'Italy',
        'Mexico',
        'Netherlands',
        'Norway',
        'Poland',
        'Portugal',
        'Russian Federation',
        'Spain',
        'Sweden',
        'Switzerland',
        'Turkey',
        'United Kingdom of Great Britain and Northern Ireland',
        'United States of America',
    )

    edu = (
        "Bachelor's degree",
        'Less than a Bachelors',
        "Master's degree",
        'Post grad',
    )

    country = st.selectbox('Country', countries)
    edu = st.selectbox('Education Level', edu)
    exp = st.slider('Years of experience', 0, 50, 3)
    ok = st.button('Calculate Salary')

    if ok:
        X = np.array([[country, edu, exp]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_edu.transform(X[:, 1])
        X = X.astype(float)
        salary_pred = random_reg.predict(X)
        st.subheader(f'The estimated salary is USD{salary_pred[0]:.2f}')