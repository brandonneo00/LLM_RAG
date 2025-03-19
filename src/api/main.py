from fastapi import FastAPI
from pydantic_models import QueryInput, QueryResponse
from langchain_utils import get_rag_chain
from db_utils import insert_application_logs, get_chat_history

import uuid
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)
app = FastAPI()

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    session_id = query_input.session_id
    logging.info(f"Session ID: {session_id}, User Query: {query_input.question}, Model: {query_input.model.value}")
    if not session_id:
        session_id = str(uuid.uuid4())

    chat_history = get_chat_history(session_id)
    rag_chain = get_rag_chain(query_input.model.value)
    invoked_chain = rag_chain.invoke({
        "input": query_input.question,
        "chat_history": chat_history
    })
    print(f"this is invoked_chain: {invoked_chain}")
    
    answer = invoked_chain['answer']
    print(f"this is answer: {answer}")

    insert_application_logs(session_id, query_input.question, answer, query_input.model.value)
    logging.info(f"Session ID: {session_id}, AI Response: {answer}")
    return QueryResponse(answer=answer, session_id=session_id, model=query_input.model, sources=invoked_chain['context'])

