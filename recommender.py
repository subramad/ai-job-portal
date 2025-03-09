import streamlit as st
from utils import extract_text_from_pdf, extract_skills, recommend_jobs
import spacy
import time
from streamlit_lottie import st_lottie_spinner
import json
from streamlit_extras.colored_header import colored_header

with open('data/Animation.json', 'r') as file:
    animation_data = json.load(file)

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


# Function to process the resume and recommend jobs
def process_resume(uploaded_file):
    resume_text = extract_text_from_pdf(uploaded_file)
    skills = extract_skills(resume_text)
    recommendations = recommend_jobs(skills)
    return recommendations, skills


colored_header(
    label="Add your Details",
    color_name="violet-70",
    description=""
)


# Enter Name
name = st.text_input("Full Name (*)", placeholder="enter your name")
# Enter Name
email = st.text_input("Email Address(*)",
                      placeholder="enter your email address")
# Enter Name
phone = st.number_input("Phone Number (*)", step=1,
                        max_value=9999999999, placeholder="enter your phone number")
# File uploader
file_upload_disabled = (name == '' or email == '' or phone == '')
if file_upload_disabled:
    st.text("Please first enter the above details to upload your resume")
uploaded_file = st.file_uploader("Add your resume PDF", type=[
                                 'pdf'], disabled=file_upload_disabled)

if uploaded_file is not None:
    # with st.spinner('Processing...'):
    with st_lottie_spinner(animation_data, height=200):
        # Process resume and recommend jobs
        time.sleep(5)
        file_path = uploaded_file.name
        df_jobs, extracted_skills = process_resume(file_path)

        # Display recommended jobs as DataFrame
        colored_header(
            label=f"Hey {name} here are the recommended jobs for you:",
            color_name="violet-70",
            description=""
        )
        # df = pd.DataFrame(['Job Title','Company Name','Location','Industry','Sector','Average Salary'])
        st.dataframe(df_jobs[['Job Title', 'Company Name',
                     'Location', 'Sector', 'Match Confidence']],use_container_width=True)

        colored_header(
            label="Matched Skills in your Resume:",
            color_name="violet-70",
            description=""
        )

        skills_formatted = ''

        for i in extracted_skills:
            skills_formatted += "- " + i + "\n"

        st.markdown(skills_formatted)
    st.balloons()
