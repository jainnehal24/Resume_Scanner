import pandas as pd
import numpy as np
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pdfminer.high_level import extract_text
import os
from secret_key import api_key

# initializing llm model
llm = OpenAI(api_key=api_key)

# Define a function to extract text from PDF
def extract_text_from_pdf(file_path):
    return extract_text(file_path)

# Define a function that uses LangChain to determine if the resume is a good fit for the role    
def evaluate_resume(role,resume_text):
    prompt_template_name = PromptTemplate(
        input_variables =['role','resume_text'],
        template = "Given the role description: {role} and the resume text: {resume_text}, is candidate a good fit for the role?"
    )
    p = prompt_template_name.format(role=role,resume_text=resume_text)
    chain = LLMChain(llm=llm, prompt=prompt_template_name)
    response = chain.run(role=role,resume_text=resume_text)
    return response