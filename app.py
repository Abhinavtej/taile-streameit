import os
import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from dotenv import load_dotenv
import streamlit as st

# Add NLTK data path
nltk.data.path.append("nltk_data")

# Load environment variables
load_dotenv()

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Function to generate a story
def generate_story(user_input, genre="fiction", language="english"):
    """Generate a story using Llama-3.2 without pipeline."""
    tokens = word_tokenize(user_input)
    tagged_words = pos_tag(tokens)
    keywords = [word for word, tag in tagged_words if tag in ["NN", "NNS", "NNP", "NNPS", "JJ"]]

    prompt = f"""
    You are a creative and skilled storyteller, capable of crafting immersive and engaging narratives.
    
    **Task:** 
    Write a captivating **{genre}** story in **{language}** based on the following key elements: 
    - **Keywords:** {', '.join(keywords)}
    
    **Guidelines:** 
    - Ensure the story has a **clear beginning, middle, and end**. 
    - Maintain a **coherent flow** and **engaging storytelling style**. 
    - Use **vivid descriptions**, **realistic dialogues**, and **strong character development**. 
    - Keep the story **exciting, emotionally engaging, and original**. 
    - Make it **concise** yet **impactful**, ensuring it fits within the given constraints.
    
    **Output Format:** 
    Return only the final story without any explanations or unnecessary text. 
    
    Now, begin the story.
    """

    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(
        f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    response_json = response.json()
    story = response_json['candidates'][0]['content']['parts'][0]['text']
    return story

# Simulate word-by-word generation
def stream_story(story):
    """Simulate word-by-word streaming of the story."""
    words = story.split()  # Split the story into words
    placeholder = st.empty()  # Create a placeholder for dynamic updates
    streamed_text = ""
    for word in words:
        streamed_text += word + " "
        placeholder.markdown(streamed_text)  # Update the placeholder with the current text
        time.sleep(0.1)  # Add a small delay between words for effect

# Streamlit app
import time

# Page configuration
st.set_page_config(page_title="Word-by-Word Story Generator", page_icon="📖", layout="wide")

# Title and description
st.markdown("<h1>📖 TA<span style='color:gray'>I</span>LE: Story Generator Chatbot using Keywords</h1>", unsafe_allow_html=True)
st.write("Welcome! Tell me some keywords, choose a genre, and I'll craft a captivating story for you — one word at a time.")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    genre = st.selectbox("Choose a genre:", ["Fiction", "Fantasy", "Mystery", "Romance", "Sci-Fi", "Horror", "Adventure", "Thriller", "Historical", "Comedy"])
    language = st.selectbox("Choose a language:", ["English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam", "Marathi", "Bengali", "Gujarati", "Punjabi", "Odia"])
    
    st.header("Batch: TT 4")
    team_members = ["Abhinavtej Reddy", "K Pavan Aditya", "K Yasa Sri", "K Uday Reddy", "Karina Yadav"]
    roll_num = ["2211CS020208", "2211CS020224", "2211CS020227", "2211CS020228", "2211CS020232"]

    st.write("Team Members:")
    for i in range(len(team_members)):
        st.write(f"🔹 {team_members[i]} ({roll_num[i]})")
        
# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Enter keywords or ideas for your story:")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate story
    try:
        story = generate_story(user_input, genre.lower(), language.lower())
        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": story})

        # Display assistant message word by word
        with st.chat_message("assistant"):
            stream_story(story)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        with st.chat_message("assistant"):
            st.error(error_message)