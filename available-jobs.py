import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from streamlit_extras.colored_header import colored_header


colored_header(
    label="Current Available Jobs",
    color_name="violet-70",
    description=""
)


df = pd.read_csv("data/job_dataset.csv")

st.dataframe(df[['Job Title', 'Company Name', 'Location', 'Sector']])


colored_header(
    label="Top Titles:",
    color_name="violet-70",
    description=""
)


titles = ' '.join(df['Job Title'])

wordcloud = WordCloud(width=800, height=400,
                      background_color='white').generate(titles)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)


colored_header(
    label="Top 10 Locations:",
    color_name="violet-70",
    description=""
)


location_frequency = df['Location'].value_counts().reset_index().head(10)
location_frequency.columns = ['Value', 'Frequency']

st.bar_chart(location_frequency.set_index('Value'))