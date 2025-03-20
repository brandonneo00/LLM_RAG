from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os 


persistent_client = chromadb.PersistentClient(path="../chroma_db")
collection = persistent_client.get_or_create_collection("budget_2024")
output_parser = StrOutputParser()

# Set up prompts and chains
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant from Singapore's Ministry of Finance." 
                "You are helping members of the public to answer questions that they have regarding the Singapore Budget 2024." 
                "You are here to provide information strictly about Singapore's Budget 2024. "
                "If a user asks a question that is not related to the Singapore Budget 2024, "
                "respond with 'I'm sorry, but I can only provide information related to Singapore's Budget 2024.'"
                "Use the following context to only answer the user's question that's related to the Singapore Budget 2024."),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

def get_rag_chain(model="gpt-4o-mini"):
    load_dotenv()
    embedding_function = OpenAIEmbeddings()
    vectorstore = Chroma(
        client=persistent_client,
        collection_name="budget_2024",
        embedding_function=embedding_function,
    )
    # print(vectorstore._collection.count(),"brandon")
        

    retriever = vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5,"k": 4}) 
    # retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 3, "lambda": 0.85}, threshold=0.8)

    # load_dotenv()
    llm = ChatOpenAI(model=model, temperature=0)
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)   
    print(f"this is the history_aware_retriever: {history_aware_retriever}")
    print(f"this is the rag_chain: {rag_chain}") 
    return rag_chain
