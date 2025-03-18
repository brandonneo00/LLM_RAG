import streamlit as st
from dotenv import load_dotenv, set_key

dotenv_path = ".env"
load_dotenv(dotenv_path)

def update_env(api_key):
    """Update the API key in the .env file."""
    if api_key:
        set_key(dotenv_path, "OPENAI_API_KEY", api_key)
        st.sidebar.success("API key saved successfully!")

def display_sidebar():
    # Specify API Key
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password", key="api_key")

    # User needs to click on this button to load the API Key into the .env file
    if st.sidebar.button("Save API Key"):
        if api_key:
            update_env(api_key)
        else:
            st.sidebar.error("Please enter a valid API key!")

    # Model Selection
    model_options = ["gpt-4o", "gpt-4o-mini"]
    st.sidebar.selectbox("Select Model", options=model_options, key="model")

