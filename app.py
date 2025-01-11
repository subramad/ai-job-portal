import streamlit as st
from utils import extract_text_from_pdf, extract_skills, recommend_jobs
import spacy


# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


# Function to process the resume and recommend jobs
def process_resume(file_path):
    resume_text = extract_text_from_pdf(file_path)
    skills = extract_skills(resume_text)
    recommendations = recommend_jobs(skills)
    return recommendations
    

# Streamlit app
def main():
    st.title("AI-Powered Job Portal CLI")
    st.write("Upload your resume in PDF format")

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=['pdf'])

    if uploaded_file is not None:
        # Process resume and recommend jobs
        file_path=uploaded_file.name
        df_jobs = process_resume(file_path)

        # Display recommended jobs as DataFrame
        st.write("Recommended Jobs:")
        # df = pd.DataFrame(['Job Title','Company Name','Location','Industry','Sector','Average Salary'])
        st.dataframe(df_jobs[['Job Title','Company Name','Location','Sector','Match Confidence']])

# Run the Streamlit app
if __name__ == '__main__':
    main()