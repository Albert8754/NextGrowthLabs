{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Untitled2.ipynb",
      "provenance": [],
      "authorship_tag": "ABX9TyPYGHeDxNFonZLHJ28zrwKW",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Albert8754/NextGrowthLabs/blob/main/2.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "AV_dHnBj6C7t"
      },
      "outputs": [],
      "source": [
        "import streamlit as st\n",
        "import numpy as np\n",
        "import pandas as pd\n",
        "import nltk\n",
        "from nltk.sentiment.vader import SentimentIntensityAnalyzer\n",
        "import re\n",
        "nltk.download('stopwords')\n",
        "from nltk.stem.porter import PorterStemmer\n",
        "from nltk.corpus import stopwords\n",
        "\n",
        "port=PorterStemmer()\n",
        "def cleaner(text):\n",
        "    clean=re.sub('a-zA-z','',text)\n",
        "    clean=clean.lower()\n",
        "    clean=clean.split()\n",
        "    clean=[port.stem(word) for word in clean if word not in stopwords.words('english')]\n",
        "    clean=''.join(clean)\n",
        "    return clean\n",
        "\n",
        "st.title(\"Identifying Incorrect Ratings\")\n",
        "st.header(\"Instructions\")\n",
        "st.markdown(\"1.Review column's name should be Text\")\n",
        "st.markdown(\"2.Rating column's name should be Star\")\n",
        "st.markdown(\"3.Rating range should be 0-5\")\n",
        "\n",
        "uploaded_file = st.file_uploader(label=\"Choose a File\",\n",
        "                                 type=['csv'])\n",
        "\n",
        "\n",
        "df = pd.read_csv(uploaded_file)\n",
        "st.dataframe(df)\n",
        "\n",
        "if st.button(\"Click for Results\") :\n",
        "    df[\"Cleaned\"] = df[\"Text\"].apply(lambda x: cleaner(str(x)))\n",
        "\n",
        "    sid = SentimentIntensityAnalyzer()\n",
        "\n",
        "    df[\"Score\"] = df[\"Cleaned\"].apply(lambda review:sid.polarity_scores(review))\n",
        "    df[\"updated\"]  = df['Score'].apply(lambda score_dict: score_dict['compound'])\n",
        "    df[\"result\"] = df[\"updated\"].apply(lambda c: 'positive' if c>0 else ('no review needed'))\n",
        "\n",
        "    post[\"Suggestion\"] = post[\"Star\"].apply(lambda star: \"No Attention Needed\" if star >= 3 else \"Attention Needed\")\n",
        "\n",
        "\n",
        "    keyword = ['good', 'nice', 'thank you', 'best', 'awesome', 'helpful']\n",
        "\n",
        "    final_df = post[(post[\"Suggestion\"] == \"Attention Needed\")]\n",
        "    final_df = final_df[final_df[\"Cleaned_Text\"].isin(keyword)]\n",
        "\n",
        "    display_df = final_df[['Text','Star','Cleaned_Text','Suggestion']]\n",
        "    \n",
        "    st.markdown(\"This is a dataset containing all the positive reviews with low ratings\")\n",
        "    st.dataframe(display_df)\n",
        "    \n",
        "    st.markdown(\"This ia visualisation of diffrence between low ratings and high ratings\")\n",
        "    st.bar_chart(df_attention.Suggestion.value_counts())\n",
        "\n",
        "    data = final_df\n",
        "    \n",
        "    st.markdown(\"Download the dataset with all the incorrect ratings\")\n",
        "    st.download_button(\n",
        "        label=\"Download data as CSV\",\n",
        "        data=data.to_csv().encode(\"utf-8\"),\n",
        "        file_name='data.csv',\n",
        "        mime='text/csv',\n",
        "    )"
      ]
    }
  ]
}