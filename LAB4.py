import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfFileReader
import os
from chromadb import Client  # Ensure to use the correct import based on the library's documentation

import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

st.title('My LAB3 Question Answering Chatbox')

openAImodel = st.sidebar.selectbox("Which model?", ("mini", "regular"))
buffer_size = st.sidebar.slider("Buffer Size", min_value=1, max_value=10, value=2, step=1)

if openAImodel == "mini":
    model_to_use = "gpt-4o-mini"
else:
    model_to_use = "gpt-4o"

if 'client' not in st.session_state:
    api_key = st.secrets["openai_key"]
    st.session_state.client = OpenAI(api_key=api_key)

if 'messages' not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help?"}]

# Function to create ChromaDB collection
def create_chromadb_collection(pdf_folder_path: str, collection_name: str):
    # Initialize ChromaDB client
    chroma_client = Client(api_key=st.secrets["chroma_key"])
    collection = chroma_client.create_collection(name=collection_name)

    # OpenAI Embeddings
    embedding_model = "text-embedding-3-small"
    openai_client = st.session_state.client

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

                # Add document to collection with metadata
                collection.add_document(
                    id=filename,
                    embedding=embedding,
                    metadata={"filename": filename, "text": text}
                )

    st.success("ChromaDB collection created successfully!")

# Example usage of the function
if st.button("Create ChromaDB Collection"):
    create_chromadb_collection("path/to/your/pdf/folder", "Lab4Collection")

# Display all messages
for msg in st.session_state.messages:
    chat_msg = st.chat_message(msg["role"])
    chat_msg.write(msg["content"])

# Input prompt
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Maintain the buffer size
    if len(st.session_state.messages) > buffer_size * 2:
        st.session_state.messages = st.session_state.messages[-buffer_size * 2:]

    with st.chat_message("user"):
        st.markdown(prompt)

    client = st.session_state.client
    stream = client.chat.completions.create(
        model=model_to_use,
        messages=st.session_state.messages,
        stream=True
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)

    # Ensure response is less than 150 words
    response = response[:150]
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Automatically ask for more information
    more_info_question = "Want more info? (Yes/No)"
    st.session_state.messages.append({"role": "assistant", "content": more_info_question})

# Handle the user's response for more information
if prompt and prompt.lower() in ["yes", "no"]:
    if prompt.lower() == "yes":
        st.session_state.messages.append({"role": "assistant", "content": "Continuing..."})
    elif prompt.lower() == "no":
        st.session_state.messages.append({"role": "assistant", "content": "What else?"})
