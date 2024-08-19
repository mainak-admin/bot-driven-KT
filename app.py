from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import datetime

# Load environment variables
load_dotenv()

# Set up Google Gemini API
GOOGLE_API_KEY = "AIzaSyBCdIQc2owrOKfv5jmqC3YV3KlY0Y4X63I"
genai.configure(api_key=GOOGLE_API_KEY)

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question, context):
    # Combine the context with the user's question
    combined_prompt = f"{context}\n\n{question}"
    response = chat.send_message(combined_prompt, stream=True)
    return response

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Load the pre-configured PDF document (replace 'input.pdf' with your file path)
input_file_path = "D:\\Hackathon\\Bot_driven_KT\\VALIC ONLINE.pdf"  # Change this to your actual file path
context = read_pdf(input_file_path)

# Initialize our Streamlit app
st.set_page_config(page_title="Gemini LLM Application")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input, context)
    
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    
    # Collect all response chunks
    response_text = ""
    for chunk in response:
        response_text += chunk.text

    # Add response to chat history
    st.session_state['chat_history'].append(("Bot", response_text))
    
    # Display the response to the user
    st.subheader("The Response is")
    st.write(response_text)

    # Save chat history to a text file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    history_file = f"chat_history_{timestamp}.txt"
    with open(history_file, "w") as file:
        for role, text in st.session_state['chat_history']:
            file.write(f"{role}: {text}\n")
