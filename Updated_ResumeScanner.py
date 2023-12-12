import pandas as pd
import numpy as np
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pdfminer.high_level import extract_text
import os
import glob
import shutil
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from secret_key import api_key

with st.sidebar:
    st.image(r'images/kpmg-logo1.jpg')
    st.title('KPMG - POC')
    st.markdown('''
    ## Functionality:
    Testing multiple POC with respect to interacting
    with contract document.
                   
    Tech Stack:
    - streamlit
    - Langchain
    - OpenAI
    - LLaMa
    - PaLM
 
    ## Developer:
 
    - Nehal Jain -> Consultant KPMG India
    - Digital LightHouse
     
    ''')
 
    add_vertical_space(4)
    st.write('© 2023 KPMG Assurance and Consulting Services LLP, an Indian Limited Liability Partnership and a member firm of the KPMG global organization of independent member firms')
    st.write('affiliated with KPMG International Limited, a private English company limited by guarantee. All rights reserved.For more detail about the structure of the KPMG global organization please visit https://kpmg.com/governance.')

llm = OpenAI(api_key=api_key)

st.title("Resume Scanner using Langchain")

job_role = st.text_input("Enter the Job Role")

# Get the resumes
resumes = os.listdir('resumes')

# function to extract text from PDF
def extract_text_from_pdf(file_path):
    return extract_text(file_path)

# function to evaluate resume basis the role using llm
def evaluate_resume(role,resume_text):
    prompt_template1 = PromptTemplate(
        input_variables =['role','resume_text'],
        template = "Given the role description: {role} and the resume text: {resume_text}, is candidate a good fit for the role?"
    )
    #p = prompt_template_name.format(role=role,resume_text=resume_text)
    chain1 = LLMChain(llm=llm, prompt=prompt_template1)
    response = chain1.run(role=role,resume_text=resume_text)
    return response

def final_output(result):
    prompt_template2 = PromptTemplate(
        input_variables =['result'],
        template = "Read the response: {result}, and if it is positive, return 'yes' else 'no' as an output"
    )
    #p = prompt_template_name.format(result=result,resume=resume)
    chain2 = LLMChain(llm=llm, prompt=prompt_template2)
    output = chain2.run(result=result)
    return output

if st.button("Scan"):
    if job_role != "":
        # classify resumes
        output_table = []
        classified_resumes = {}
        for resume in resumes:
            resume_text = extract_text_from_pdf(f'resumes/{resume}')
            result = evaluate_resume(job_role,resume_text)
            output = final_output(result)
            output_table.append((resume,output))
            classified_resumes[resume] = result

        # Convert to DataFrame
        output_df = pd.DataFrame(output_table, columns=['Resume', 'Good fit'])
        output_df = output_df.replace('\n\nYes','Yes')
        output_df = output_df.replace('\n\nNo','No')

        # Display the results
        st.dataframe(output_df)
        for resume, result in classified_resumes.items():
            st.write(f"{resume}: {result}")

        # saving shortlisted resumes into a separate folder
        for i in range(0,len(output_df)):
            if(output_df['Good fit'].iloc[i]=='Yes'):
                resume_file = output_df['Resume'].iloc[i]
                if os.path.exists("shortlisted_resumes"): 
                    files = glob.glob(os.path.join('shortlisted_resumes', '*'))
                    for file in files:
                        if os.path.isfile(file):
                            os.remove(file)
                else:
                    os.makedirs("shortlisted_resumes")
                shutil.copy(f'resumes/{resume_file}', 'shortlisted_resumes')
    else:
        st.write("Please enter a job role")