import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfFileReader
import os
from chromadb import Client

# Optional: Handle pysqlite3 import to avoid SQLite issues
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    st.warning("pysqlite3 package is not available. Please install it to resolve SQLite issues. The application might still work with default sqlite3.")

# Initialize OpenAI client
if 'client' not in st.session_state:
    api_key = st.secrets.get("openai_key")
    if api_key:
        st.session_state.client = OpenAI(api_key=api_key)
    else:
        st.error("OpenAI API key is not set in secrets.")

# Function to create the ChromaDB collection
def create_lab4_chromadb_collection(pdf_folder_path: str):
    if 'Lab4_vectorDB' not in st.session_state:
        try:
            # Initialize ChromaDB client
            chroma_client = Client(api_key=st.secrets.get("chroma_key"))
            collection = chroma_client.create_collection(name="Lab4Collection")

            # Define embedding model and OpenAI client
            embedding_model = "text-embedding-3-small"
            openai_client = st.session_state.client

            # Process each PDF file in the folder
            for filename in os.listdir(pdf_folder_path):
                if filename.endswith(".pdf"):
                    file_path = os.path.join(pdf_folder_path, filename)
                    with open(file_path, 'rb') as file:
                        pdf_reader = PdfFileReader(file)
                        text = ""
                        for page_num in range(pdf_reader.numPages):
                            text += pdf_reader.getPage(page_num).extract_text()

                        # Generate embedding for the text
                        embedding_response = openai_client.embeddings.create(
                            model=embedding_model,
                            input=text
                        )
                        embedding = embedding_response['data'][0]['embedding']

                        # Add document to ChromaDB collection with metadata
                        collection.add_document(
                            id=filename,
                            embedding=embedding,
                            metadata={"filename": filename, "text": text}
                        )

            # Store the collection in session state to avoid re-creating it
            st.session_state.Lab4_vectorDB = collection
            st.success("Lab4 ChromaDB collection created successfully!")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.info("Lab4 ChromaDB already exists in session state.")

# Function to test the ChromaDB with a query
def test_chromadb(query: str):
    try:
        collection = st.session_state.Lab4_vectorDB
        results = collection.query_texts(query_texts=[query], top_k=3)
        st.write(f"Top 3 documents for query '{query}':")
        for doc in results['documents']:
            st.write(doc['metadata']['filename'])
    except Exception as e:
        st.error(f"Error during query: {e}")

# Streamlit app structure
st.title("Lab4A: ChromaDB and OpenAI Embedding")

# Button to create the ChromaDB collection from PDF files
if st.button("Create Lab4 ChromaDB Collection"):
    create_lab4_chromadb_collection("path/to/your/pdf/folder")

# Input box to enter a test query and button to test the ChromaDB
query = st.text_input("Enter a test query", "")
if st.button("Test ChromaDB") and query:
    test_chromadb(query)
