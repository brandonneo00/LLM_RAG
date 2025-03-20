import requests
import streamlit as st

def get_api_response(question, session_id, model):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "question": question,
        "model": model,
        # "api_key": st.session_state.api_key
    }
    if session_id:
        data["session_id"] = session_id

    try:
        response = requests.post("http://backend:8000/chat", headers=headers, json=data,allow_redirects=False)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API request failed with status code {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None
    
def update_env(api_key):
    if api_key:
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {"api_key": api_key}
        
        try:
            response = requests.post("http://backend:8000/update-api-key", headers=headers, json=data, allow_redirects=False)
            
            if response.status_code == 200:
                st.sidebar.success("API key saved successfully!")
            else:
                st.sidebar.error(f"Request failed with status code {response.status_code}: {response.text}")
        except Exception as e:
            st.sidebar.error(f"An error occurred: {str(e)}")
