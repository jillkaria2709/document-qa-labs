import streamlit as st
from openai import OpenAI, OpenAIError

# Show title and description.
st.title("📄 Question the PDF")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")

# Check if the API key has been entered
if openai_api_key:
    try:
        # Attempt to create an OpenAI client to validate the API key.
        client = OpenAI(api_key=openai_api_key)
        
        # Optionally, make a simple API call to verify the key
        client.models.list()  # This call checks if the API key is valid
        
        # Proceed with the rest of the app if the API key is valid
        st.write("API key is valid! You can now upload a document and ask questions.")

        # Let the user upload a file via `st.file_uploader`.
        uploaded_file = st.file_uploader(
            "Upload a document (.txt or .md)", type=("txt", "md")
        )

        # Ask the user for a question via `st.text_area`.
        question = st.text_area(
            "Now ask a question about the document!",
            placeholder="Can you give me a short summary?",
            disabled=not uploaded_file,
        )

        if uploaded_file and question:
            # Process the uploaded file and question.
            document = uploaded_file.read().decode()
            messages = [
                {
                    "role": "user",
                    "content": f"Here's a document: {document} \n\n---\n\n {question}",
                }
            ]

            # Generate an answer using the OpenAI API.
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True,
            )

            # Stream the response to the app using `st.write_stream`.
            st.write_stream(stream)

    except OpenAIError as e:
        st.error(f"Invalid API Key. Please put in one that works")
else:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    # Optionally, you can add placeholders for the file uploader and question input
    st.write("Please enter a valid API key to access the document upload and question features.")
