import streamlit as st
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

# --- Configuration ---
# Set your token here or in a .env file as HF_TOKEN
HF_TOKEN = os.getenv("HF_TOKEN") or "your_hugging_face_token_here"

# Using Llama-3 for student-focused reasoning
TEXT_MODEL = "meta-llama/Llama-3.2-3B-Instruct" 

# Initialize the Hugging Face Client
client = InferenceClient(api_key=HF_TOKEN)

# --- Helper Functions ---

def get_ai_response(prompt):
    """Generates text response using HF chat_completion."""
    try:
        messages = [{"role": "user", "content": prompt}]
        response = client.chat_completion(
            model=TEXT_MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

# --- Streamlit UI Setup ---
st.set_page_config(page_title="AI Student Health Hub", layout="wide")
st.header("🎓 Student-Centric Fitness & Diet AI")

# Sidebar for Profile
if 'profile' not in st.session_state:
    st.session_state.profile = {
        'culture': 'Indian',
        'budget': 'Low ($30/week)',
        'resources': 'Dorm room, Microwave',
        'goal': 'Lose weight'
    }

with st.sidebar:
    st.subheader("Your Profile")
    st.session_state.profile['culture'] = st.text_input(
        "Culture/Diet Type", value=st.session_state.profile['culture'])
    st.session_state.profile['budget'] = st.text_input(
        "Weekly Budget", value=st.session_state.profile['budget'])
    st.session_state.profile['resources'] = st.text_area(
        "Available Resources (Tools/Gym)", value=st.session_state.profile['resources'])
    st.session_state.profile['goal'] = st.text_input(
        "Fitness Goal", value=st.session_state.profile['goal'])

# Main Tab for Meal & Workout Planner
st.subheader("Generate Personalized 7-Day Plan")
if st.button("Generate My 7-Day Plan"):
    with st.spinner("AI is crafting your student-friendly plan..."):
        prompt = f"""
        Act as a student fitness coach. Create a 7-day plan for a student with these constraints:
        - Culture: {st.session_state.profile['culture']}
        - Budget: {st.session_state.profile['budget']}
        - Equipment: {st.session_state.profile['resources']}
        - Goal: {st.session_state.profile['goal']}
        
        Ensure the meals use affordable cultural staples and the workouts are possible in a small space.
        """
        result = get_ai_response(prompt)
        st.markdown(result)