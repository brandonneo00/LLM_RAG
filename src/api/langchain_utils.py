from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
# from chroma_utils import vectorstore #commented out by me 18 march 2025

## Added by me 18 March 2025
import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

persistent_client = chromadb.PersistentClient(path="../chroma_db")
collection = persistent_client.get_or_create_collection("budget_2024")
embedding_function = OpenAIEmbeddings()
vectorstore = Chroma(
    client=persistent_client,
    collection_name="budget_2024",
    embedding_function=embedding_function,
)
## End of my's addition

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

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
    ("system", "You are a helpful AI assistant. Use the following context to answer the user's question."),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])



def get_rag_chain(model="gpt-4o-mini"):
    llm = ChatOpenAI(model=model)
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)   
    print(f"this is the history_aware_retriever: {history_aware_retriever}")
    print(f"this is the rag_chain: {rag_chain}") 
    return rag_chain
