# LLM_RAG_Chatbot

## Architecture Diagrams that highlight key components and the flow of information in the system 

### A brief explanation of the RAG implementation and its rationale 
- input processing: when a user inputs a question (and the chat history before if any), the system first reformulates it into a standalone query using the contextualise prompt. this is essential to remove any dependencies on previous parts of the conversation
- retrieval step: the refined query is then passed to the vectorstore retriever, based on the vector embeddings stored in the chroma database, the MMR retriever fetches the top 4 most relevant and diverse documents
- augmented generation: the retrieved documents, along with the chat history and the standalone question (rich context) are then fed into the LLM via the QA prompt to generate a well-informed answer
- answer: the rag chain outputs the answer, combining retrieval and generation for a more context-aware response 

- ^^ what is the frontend and backend? 
- ^^ various types of db? 

## A list of prompts used to interact with the LLM, demonstrating the different scenarios the chatbot is expected to handle 


## Submit a list of prompts that you designed for the LLM
- Guardrails

## A comprehensive README that provides clear instructions on how to set up and run the chatbot application through docker
- at the parent directory of the cloned repo, run `docker-compose up --build`
- open the URL provided in the terminal 

## environment variable to update the chatgpt apikey 


