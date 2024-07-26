import os
import tempfile
import streamlit as st
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv() 
genai.configure(api_key= os.environ.get("API_KEY"))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config
)

def upload_to_gemini(data, mime_type=None):
  file = genai.upload_file(data, mime_type=mime_type)
  return file


system_prompt =  '''
As a highly trained medical practioner in image analysis, you are responsible for generating an approximate diagnosis 
so that using that info patient can report for further doctor consultation. You will just detect the disease and any abnormal anomalies
from the image ans suggest what further steps can be done. Do not directly say to seek medical advice rather give an observation first 
and then recommend to a doctor.

Your should give me the following:
1.Detailed analysis: carefully analyse the image to identify any abnormal findings. Surf the web for possible disease matches.
2.Structured report: identify all anomalies or common signs of disease and curate all findings in a structured manner in form of a report.
3.Recommendations: Based on your findings, recommend certain further steps or practices to follow.
4.Treatment: If appropiate, provide treatment or advice for doctor consultation.

Important note:
1. Scope: Do respond to images with skin abnormalities that are related to human illness
2. Clarity: if image clarity is compromised respond saying that "Sorry! I cannot process on the image due to limited visibility"
3. Disclaimer : I'm an AI agent and donot hold the entire knowledge to give accurate analysis. You should consult a physician.
'''
st.set_page_config(page_title="MediBuddy", page_icon=":material/thumb_up:", layout="centered", initial_sidebar_state="auto", menu_items={
    'About': "# This is a header. This is an *extremely* cool app!"
})

st.image("logo.png", width = 450)
st.subheader(':gray[An assistant to help you diagnose !]' )
uploaded_file = st.file_uploader("Kindy upload the medical image with visible symptoms")
submit_button = st.button(label="Generate analysis")

if uploaded_file is not None:  
    # Create a temporary directory
  with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    # Save the uploaded file to the temporary directory
    temp_file.write(uploaded_file.read())
    temp_file_path = temp_file.name
    st.image(uploaded_file)

if submit_button:
    files = [
    upload_to_gemini(temp_file_path, mime_type="image/jpeg"),
    ]

    chat_session = model.start_chat(
    history=[
    {
      "role": "user",
      "parts": [
        files[0],
        system_prompt,
      ],
    },
    ]
    )
    response = chat_session.send_message("INSERT_INPUT_HERE")
    # response = model.generate_content(system_prompt)

    st.write(response.text)