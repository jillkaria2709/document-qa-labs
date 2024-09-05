import streamlit as st
import os

# Sidebar with buttons for navigation
st.sidebar.title("Navigation")
home_button = st.sidebar.button("Home")
lab1_button = st.sidebar.button("LAB1")
lab2_button = st.sidebar.button("LAB2")

# Initialize a default page (Home) to be shown if no button is clicked yet
if 'page' not in st.session_state:
    st.session_state.page = 'LAB2'

# Update page state based on button clicks
if home_button:
    st.session_state.page = 'Home'
elif lab1_button:
    st.session_state.page = 'LAB1'
elif lab2_button:
    st.session_state.page = 'LAB2'

# Display the appropriate content based on the current page
if st.session_state.page == 'Home':
    st.title("Welcome to my labs")
    st.write("You can see my labs here.")
elif st.session_state.page == 'LAB1':
    st.title("LAB1")
    if os.path.exists('LAB1.py'):
        with open('LAB1.py') as f:
            code = f.read()
            exec(code)  # Executes the LAB1.py code
    else:
        st.error("LAB1.py file not found.")
elif st.session_state.page == 'LAB2':
    st.title("LAB2")
    if os.path.exists('LAB2.py'):
        with open('LAB2.py') as f:
            code = f.read()
            exec(code)  # Executes the LAB2.py code
    else:
        st.error("LAB2.py file not found.")
