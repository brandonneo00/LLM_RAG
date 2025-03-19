from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
embedding_function = OpenAIEmbeddings()
# vectorstore = Chroma(persist_directory="../chroma_db", embedding_function=embedding_function) #commented out by me 18 march 2025
# print(vectorstore._collection.count()) #commented out by me 18 march 2025

## Added by me on 18 March 2025
import chromadb
persistent_client = chromadb.PersistentClient(path="../chroma_db")
collection = persistent_client.get_or_create_collection("budget_2024")

vectorstore = Chroma(
    client=persistent_client,
    collection_name="budget_2024",
    embedding_function=embedding_function,
)
print(vectorstore._collection.count())
## End of addition
