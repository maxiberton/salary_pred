import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import zipfile
from io import BytesIO

def shorten_categories(cat, cutoff):
    cat_map = {}
    for i in range(len(cat)):
        if cat.values[i] >= cutoff:
            cat_map[cat.index[i]] = cat.index[i]
        else:
            cat_map[cat.index[i]] = 'Other'
    return cat_map


def clean_experience(df):
    df.loc[df.YearsCodePro=='Less than 1 year', 'YearsCodePro'] = 0.5
    df.loc[df.YearsCodePro=='More than 50 years', 'YearsCodePro'] = 50
    return df


def clean_edu(x):
    if "Bachelor’s" in x:
        return "Bachelor's degree"
    if "Master’s" in x:
        return "Master's degree"
    if "Professional" in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache
def load_data():
    url = 'https://info.stackoverflowsolutions.com/rs/719-EMH-566/images/stack-overflow-developer-survey-2022.zip'
    r = requests.get(url)
    buf = BytesIO(r.content)
    with zipfile.ZipFile(buf, "r") as f:
        for name in f.namelist():
            if name == 'survey_results_public.csv':
                with f.open(name) as zd:
                    df = pd.read_csv(zd)

    df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly']]
    df.rename(columns={'ConvertedCompYearly': 'Salary'}, inplace=True)
    df = df.loc[df.Salary.notnull()]
    df = df.dropna()
    df = df.loc[df.Employment.str.contains('Employed, full-time')]
    df.drop(columns=['Employment'], inplace=True)

    country_map = shorten_categories(df.Country.value_counts(), 300)
    df.Country = df.Country.map(country_map)
    df = df.loc[(df.Salary <= 250000) & (df.Salary >= 10000) & (df.Country != 'Other')]
    df = df.reset_index(drop=True)

    df.loc[df.YearsCodePro == 'Less than 1 year', 'YearsCodePro'] = 0.5
    df.loc[df.YearsCodePro == 'More than 50 years', 'YearsCodePro'] = 50

    df.EdLevel = df.EdLevel.apply(clean_edu)
    return df


df = load_data()


def show_explore_page():
    st.title('Explore Software Engineer Salaries')
    st.write("""### Stack Overflow Developer Survey 2022""")

    data = df['Country'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    st.write(""" #### Number of data from different countries """)
    st.pyplot(fig1)

    st.write(""" #### Mean Salary based on Country """)
    data_bar = df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data_bar)

    st.write(""" #### Mean Salary based on Experience """)
    data_line = df.groupby(['YearsCodePro'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data_line)
