import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
st.title("AI-Powered Job Portal")
st.write("Current Available Jobs:")



df = pd.read_csv("data/jobs.csv")

st.dataframe(df[['Job Title','Company Name','Location','Sector']])

st.write("Top Titles:")

titles = ' '.join(df['Job Title'])

wordcloud = WordCloud(width=800,height=400,background_color='white').generate(titles)
fig, ax = plt.subplots()
ax.imshow(wordcloud,interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

st.write("Top 10 Locations:")

location_frequency = df['Location'].value_counts().reset_index().head(10)
location_frequency.columns = ['Value', 'Frequency']

st.bar_chart(location_frequency.set_index('Value'))