# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 18:46:16 2022

@author: HP
"""

import streamlit as st
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

port=PorterStemmer()
def cleaner(text):
    clean=re.sub('a-zA-z','',text)
    clean=clean.lower()
    clean=clean.split()
    clean=[port.stem(word) for word in clean if word not in stopwords.words('english')]
    clean=''.join(clean)
    return clean

st.title("Identifying Incorrect Ratings")
st.header("Instructions")
st.markdown("1.Review column's name should be Text")
st.markdown("2.Rating column's name should be Star")
st.markdown("3.Rating range should be 0-5")

uploaded_file = st.file_uploader(label="Choose a File",
                                 type=['csv'])


df = pd.read_csv(uploaded_file)
st.dataframe(df)

if st.button("Click for Results") :
    df["Cleaned"] = df["Text"].apply(lambda x: cleaner(str(x)))

    sid = SentimentIntensityAnalyzer()

    df["Score"] = df["Cleaned"].apply(lambda review:sid.polarity_scores(review))
    df["updated"]  = df['Score'].apply(lambda score_dict: score_dict['compound'])
    df["result"] = df["updated"].apply(lambda c: 'positive' if c>0 else ('no review needed'))

    df["Suggestion"] = df["Star"].apply(lambda star: "No Attention Needed" if star >= 3 else "Attention Needed")


    keyword = ['good', 'nice', 'thank you', 'best', 'awesome', 'helpful']

    final_df = df[(df["Suggestion"] == "Attention Needed")]
    final_df = final_df[final_df["Cleaned_Text"].isin(keyword)]

    display_df = final_df[['Text','Star','Cleaned_Text','Suggestion']]
    
    st.markdown("This is a dataset containing all the positive reviews with low ratings")
    st.dataframe(display_df)
    
    st.markdown("This ia visualisation of diffrence between low ratings and high ratings")
    st.bar_chart(df.Suggestion.value_counts())

    data = final_df
    
    st.markdown("Download the dataset with all the incorrect ratings")
    st.download_button(
        label="Download data as CSV",
        data=data.to_csv().encode("utf-8"),
        file_name='data.csv',
        mime='text/csv',
    )
