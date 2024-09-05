import streamlit as st
from openai import OpenAI, OpenAIError

# Show title and description.
st.title("📄 Question the PDF")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Load the OpenAI API key from secrets
openai_api_key = st.secrets["openai"]["api_key"]

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

        # Options for summarizing the document
        st.sidebar.header("Summarize the document")
        summary_option = st.sidebar.selectbox(
            "Choose the summary format:",
            [
                "Summarize the document in 100 words",
                "Summarize the document in 2 connecting paragraphs",
                "Summarize the document in 5 bullet points"
            ]
        )

        # Text input for custom summary format
        custom_summary_format = ""
        if summary_option == "Custom summary format":
            custom_summary_format = st.sidebar.text_input(
                "Enter your custom summary format:",
                placeholder="Describe how you'd like the summary to be formatted."
            )
        
        # Update the input field with the selected summary format
        default_question = custom_summary_format if custom_summary_format else summary_option
        question = st.text_area(
            "Now ask a question about the document!",
            placeholder="Can you give me a short summary?",
            value=default_question,
            disabled=not uploaded_file,
        )

        # Option to select between gpt-4 and gpt-4o-mini
        model_option = st.sidebar.radio(
            "Choose the model:",
            ["gpt-4", "gpt-4o-mini"]
        )

        if uploaded_file and question:
            # Process the uploaded file and question.
            document = uploaded_file.read().decode()
            summary_prompt = (
                f"Here's a document: {document}\n\n"
                f"Question: {question}\n\n"
                f"Summarize it as: {custom_summary_format if custom_summary_format else summary_option}"
            )

            # Generate an answer using the selected OpenAI model.
            response = client.chat.completions.create(
                model=model_option,
                messages=[{"role": "user", "content": summary_prompt}]
            )

            # Display the response.
            # Check the response structure
            st.write(response)  # To debug the response structure
            if response.choices:
                st.write(response.choices[0].message['content'])
            else:
                st.write("No choices in the response.")

    except OpenAIError as e:
        st.error(f"Invalid API Key. Please put in one that works")
else:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    # Optionally, you can add placeholders for the file uploader and question input
    st.write("Please enter a valid API key to access the document upload and question features.")
