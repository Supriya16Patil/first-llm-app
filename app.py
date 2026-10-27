# app.py - Your First Secured LLM App
import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="First LLM App", page_icon="🤖", layout="centered")

# --- 2. SECURE API KEY SETUP ---
# Streamlit automatically looks for secrets in:
# Locally: .streamlit/secrets.toml
# Remotely: Streamlit Cloud -> Advanced Settings

def get_api_key():
    """Attempts to retrieve the API key from st.secrets."""
    try:
        # Access the key using TOML section/key notation
        key = st.secrets["gemini"]["api_key"]
        return key
    except (KeyError, FileNotFoundError):
        st.error("Missing Gemini API Key. Please configure st.secrets.")
        st.stop() # Halts the app if key is missing

# --- 3. INITIALIZE THE MODEL ---
# Configure Google GenAI with the retrieved key
api_key = get_api_key()
genai.configure(api_key=api_key)

# Initialize the Gemini 1.5 Flash model (good for speed/cost)
# Other models: 'gemini-1.5-pro'
model = genai.GenerativeModel('gemini-3.6-flash')

# --- 4. USER INTERFACE (UI) ---
st.title("🤖 Your First LLM Assistant")
st.markdown("This app uses Python, Streamlit, and Google's **Gemini 1.5 Flash** model.")

# Create a text area for user input
user_prompt = st.text_area("Enter your prompt:", height=150, placeholder="e.g., Write a short story about a robot learning to paint...")

# Create a button to trigger generation
generate_btn = st.button("Generate Response")

# --- 5. LOGIC AND RESPONSE ---
if generate_btn and user_prompt:
    with st.spinner("Gemini is thinking..."):
        try:
            # Generate content from the model
            # You can add 'generation_config' here for temperature/tokens
            response = model.generate_content(user_prompt)
            
            # --- 6. DISPLAY OUTPUT ---
            st.subheader("Gemini's Response:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"An error occurred during generation: {e}")
elif generate_btn and not user_prompt:
    st.warning("Please enter a prompt before clicking generate.")
