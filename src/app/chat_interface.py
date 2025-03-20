import streamlit as st
from api_utils import get_api_response

def display_chat_interface():
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Query:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Generating response..."):
            response = get_api_response(prompt, st.session_state.session_id, st.session_state.model)
            print(f"this is the response: {response}")
            print(f"this is the source: {response['sources']}")

            sources_headers_lst = []
            sources_filename_lst = [] 
            for doc in response['sources']:
                if doc.get('metadata').get('Header 1') is not None:
                    sources_headers_lst.append(doc.get('metadata').get('Header 1'))
                sources_filename_lst.append(doc.get('metadata').get('file_name'))

            unique_sources_headers_lst = list(set(sources_headers_lst))
            unique_sources_filename_lst = list(set(sources_filename_lst))

            print(f"this is the sources_lst: {unique_sources_headers_lst}")
            print(f"this is the sources_filename_lst: {unique_sources_filename_lst}")
            
            if response:
                st.session_state.session_id = response.get('session_id')
                st.session_state.messages.append({"role": "assistant", "content": response['answer']})
                
                with st.chat_message("assistant"):
                    st.markdown(response['answer'])
                    
                    with st.expander("Details"):
                        st.subheader("Generated Answer")
                        st.code(response['answer'])
                        st.subheader("Model Used")
                        st.code(response['model'])
                        st.subheader("Session ID")
                        st.code(response['session_id'])
                        st.subheader("Sources and Citations")
                        st.write(f"For more information, please refer to the following PDFs in this link https://www.mof.gov.sg/singapore-budget/budget-2024 :")
                        for filename in unique_sources_filename_lst:
                            st.markdown(f"- {filename}")
                        st.write(f"Here are the section headers of original sources of information used for your reference: ")
                        for header in unique_sources_headers_lst:
                            st.code(f"{header}")
                        
            else:
                st.error("Failed to get a response from the API. Please try again.")
