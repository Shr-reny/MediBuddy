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
so that using that info patient can report for further doctor consultation.

Your ressponsibilities include:
1.Detailed analysis: carefully analyse the image, identifying any abnormal findings.
2.Structured report: identify all anomalies or signs of disease and curate all findings in a structured manner in form of a report.
3.Recommendations: Based on your findings, recommend certain further steps or practices to follow.
4. Treatment: If appropiate, provide treatment.

Important note:
1. Scope: respond only to images that are related to human illness
2. Clarity: if image clarity is compromised respond saying that "Sorry! I cannot process on the image due to limited visibility"
3. Disclaimer : I'm an AI agent and donot hold the entire knowledge to give accurate analysis. You should consult a physician.
'''
st.set_page_config(page_title="MediBuddy", page_icon=":material/thumb_up:", layout="centered", initial_sidebar_state="auto", menu_items={
    'About': "# This is a header. This is an *extremely* cool app!"
})

st.image("logo.png", width = 450)
st.subheader(':gray[An application to help you diagnose your disease easy and quick !]' )
uploaded_file = st.file_uploader("Kindky upload the medical image with visible symptoms")
submit_button = st.button(label="Generate analysis")

if uploaded_file is not None:
    # Create a temporary directory
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Save the uploaded file to the temporary directory
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

if submit_button:
    image_data=uploaded_file.getvalue()

    files = [
    upload_to_gemini(temp_file_path, mime_type="image/jpeg"),
    ]

    chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        files[0],
        "what is this disease",
      ],
    },
    {
      "role": "model",
      "parts": system_prompt,
    },
    ]
    )
    response = chat_session.send_message("INSERT_INPUT_HERE")

    st.write(response.text)