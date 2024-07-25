import os
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

st.set_page_config(page_title="MediBuddy", page_icon=":material/thumb_up:", layout="centered", initial_sidebar_state="auto", menu_items={
    'About': "# This is a header. This is an *extremely* cool app!"
})

st.image("logo.png", width = 450)
st.subheader(':gray[An application to help you diagnose your disease easy and quick !]' )
uploaded_file = st.file_uploader("Kindky upload the medical image with visible symptoms")
submit_button = st.button(label="Generate analysis")
