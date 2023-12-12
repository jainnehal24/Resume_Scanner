import streamlit as st
from resumeScannerModel import extract_text_from_pdf,evaluate_resume

st.title("Resume Scanner using Langchain")

resume_file = st.file_uploader("Upload Resume", type=['pdf'])
job_role = st.text_input("Enter the Job Role")

if st.button("Scan"):
    if resume_file is not None and job_role != "":
        # Here you would extract the text from the resume file
        resume_text = extract_text_from_pdf(resume_file)
        result = evaluate_resume(job_role,resume_text)
        st.write(result)
    else:
        st.write("Please upload a resume file and enter a job role")