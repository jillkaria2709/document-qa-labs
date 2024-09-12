import streamlit as st
from streamlit import session_state as state

# Define individual pages for homework 1 and homework 2
lab3_page = st.Page("LAB3.py", title="Lab 3")
lab2_page = st.Page("LAB2.py", title="Lab 2")
lab1_page = st.Page("LAB1.py", title="Lab 1")

# Initialize navigation with the pages
pg = st.navigation([lab3_page,lab2_page, lab1_page])

# Set page configuration (optional but helps with page title and icon)
st.set_page_config(page_title="Lab Manager", page_icon=":memo:")

# Run the navigation system
pg.run()