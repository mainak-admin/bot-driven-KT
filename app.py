#Prompts:
# Hi. My name is Mainak. Can you give a short overview of Valic Online.
# Can you give me the steps of how to perform a one time withdrawal in Valic Online
# I want to know what are the interrelated applications with Valic Online.

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
input_file_path = "D:\\Hackathon\\bot-driven-KT\\VALIC ONLINE.pdf"  # Change this to your actual file path
context = read_pdf(input_file_path)

# Initialize our Streamlit app with custom page configuration
st.set_page_config(page_title="Bot Driven Knowledge Transfer", page_icon=":robot_face:", layout="centered")

# Add custom CSS for styling and background
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0096FF; /* Light cyan background color */
    }
    .stTextInput > div > input {
        background-color: rgba(255, 255, 255, 0.8);
        color: #000000; /* Change text color to black */
        border-radius: 5px;
        padding: 10px;
    }
    .main {
        background-color: rgba(255, 255, 255, 0.8); /* Change background to white */
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        color: #000000; /* Change text color to black */
    }
    .stButton button {
        background-color: #1a73e8;
        color: #000000; /* Change text color to black */
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #0c5dbf;
    }
    .stMarkdown {
        color: #000000; /* Change text color to black */
    }
    .stSidebar {
        background-color: #ffffff;
    }
    .stSidebar .stTitle {
        color: #000000; /* Change text color to black */
    }
    .footer {
        text-align: center;
        color: #000000; /* Change text color to black */
        font-size: 12px;
        margin-top: 20px;
    }
    .stTitle {
        color: #ffffff; /* Change title text color to white */
    }
    .stMarkdown h2 {
        color: #ffffff; /* Ensure h2 text (e.g., Ask a Question) is white */
    }
    </style>
    """, unsafe_allow_html=True
)


# Add a header image using Streamlit's image function
st.image("D:\\Hackathon\\bot-driven-KT\\cognizant.jpeg", use_column_width=False, width=200, caption="Cognizant Technology Solutions")

# Add the main header and sub-header
st.title("Bot Driven Knowledge Transfer Chatbot :robot_face:")
st.markdown("**Ask questions and get insights for any application effortlessly.**")
st.markdown("---")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Sidebar for navigation and additional options
st.sidebar.title("Navigation")
st.sidebar.markdown("Explore the application options below:")
st.sidebar.markdown("- Ask a Question")
st.sidebar.markdown("- View Chat History")
st.sidebar.markdown("- About")

# Input and submit button
st.markdown("#### :speech_balloon: Ask a Question:")
input = st.text_input("", key="input", placeholder="Type your question here...")
submit = st.button("Ask the question")

# Process the input and generate response
if submit and input:
    try:
        response = get_gemini_response(input, context)
        
        # Add user query to session state chat history
        st.session_state['chat_history'].append(("You", input))
        
        # Collect all response chunks
        response_text = ""
        for chunk in response:
            # Check if chunk contains valid text before accessing it
            if hasattr(chunk, 'text') and chunk.text:
                response_text += chunk.text
            else:
                # Log or handle the case where text is not available
                st.write("Warning: Part of the response was not accessible.")

        # Check if any response text was collected
        if response_text:
            # Add response to chat history
            st.session_state['chat_history'].append(("Bot", response_text))
            
            # Display the response to the user
            st.subheader("The Response is:")
            st.markdown(f"<div style='background-color: rgba(255, 255, 255, 0.8); padding: 15px; border-radius: 5px;'>{response_text}</div>", unsafe_allow_html=True)
        else:
            st.write("The bot couldn't provide a valid response. Please try rephrasing your question.")
    
    except Exception as e:
        st.write(f"An error occurred: {e}")

    # Save chat history to a text file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    history_file = f"chat_history_{timestamp}.txt"
    with open(history_file, "w") as file:
        for role, text in st.session_state['chat_history']:
            file.write(f"{role}: {text}\n")

# Footer
st.markdown("---")
st.markdown("<div class='footer'>Developed by Cognizant. Powered by Cognizant Technology Solutions.</div>", unsafe_allow_html=True)
