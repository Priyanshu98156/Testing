import google.generativeai as genai
import os
import streamlit as st

# Set your API key from an environment variable for security
# It is better to use os.getenv() than hardcoding your key
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
genai.configure(api_key=st.secrets["GoogleAiStudio"]["api_key"])

# Your final prompt with placeholders for user input
prompt = """
Role: You are an expert ATS-optimized resume writer. Your goal is to create a hyper-relevant, three-sentence professional summary by perfectly aligning a candidate's experience with a job's requirements.

Job Description:
{job_description_text}

Candidate's Profile:
{user_summary_text}

Instructions:
1.  **Analysis:** Identify the top 3 keywords from the Job Description. Identify the top 3 matching skills from the Candidate's Profile.
2.  **Draft a strict three-sentence summary (60-80 words total).**
    *   **Sentence 1 (Identity & Core Skills):** State the candidate's professional title and integrate the 2 most relevant high-level skills from your analysis.
    *   **Sentence 2 (Quantified Achievement):** Feature one strong, quantifiable achievement that proves expertise in a primary job requirement. Use action verbs like 'developed', 'engineered', or 'optimized'. *Infer a reasonable metric if one is implied but not stated.*
    *   **Sentence 3 (Technical Proficiencies & Value):** List key technical proficiencies (languages, tools) from the JD and conclude with a value-oriented trait (e.g., "...driven to deliver efficient and scalable solutions").
3.  **Style:** Use a professional, third-person tone without pronouns. Ban all clichés ("hardworking," "team player"). Prioritize keywords from the Job Description above all else.
4.  **Output:** Provide only the final three-sentence summary. No other text.
"""

def generate_resume_summary(job_description, user_summary):
    """
    Generates a professional resume summary using the Gemini API.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Fill in the placeholders in the prompt with the actual user data
    formatted_prompt = prompt.format(
        job_description_text=job_description,
        user_summary_text=user_summary
    )
    
    response = model.generate_content(formatted_prompt)
    
    return response.text

# Example Usage:
job_desc ="""Sagemaker, Python, LLM

A day in the life of an Infoscion

 As part of the Infosys delivery team, your primary role would be to interface with the client for quality assurance, issue resolution and ensuring high customer satisfaction.
 You will understand requirements, create and review designs, validate the architecture and ensure high levels of service offerings to clients in the technology domain.
 You will participate in project estimation, provide inputs for solution delivery, conduct technical risk planning, perform code reviews and unit test plan reviews.
 You will lead and guide your teams towards developing optimized high quality code deliverables, continual knowledge management and adherence to the organizational guidelines and processes.
 You would be a key contributor to building efficient programs/ systems and if you think you fit right in to help our clients navigate their next in their digital transformation journey, this is the place for you! If you think you fit right in to help our clients navigate their next in their digital transformation journey, this is the place for you! Ability to develop value-creating strategies and models that enable clients to innovate, drive growth and increase their business profitability
 Good knowledge on software configuration management systems
 Awareness of latest technologies and Industry trends
 Logical thinking and problem solving skills along with an ability to collaborate
 Understanding of the financial processes for various types of projects and the various pricing models available
 Ability to assess the current processes, identify improvement areas and suggest the technology solutions
 One or two industry domain knowledge
 Client Interfacing skills
 Project and Team management"""
user_sum = "Highly ambitiuos fresher. WIll like to work in the industry and use my skills. Have a deep understanding of python and machine learning made some projects like covid data analaysis and medvision which leverages cnn to tell that a user has tumor or not, made a employee managements system using python and tkinter"

polished_summary = generate_resume_summary(job_desc, user_sum)
print("polished summary")
print(polished_summary)