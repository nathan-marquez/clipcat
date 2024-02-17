# main.py
import streamlit as st
import time
from visualization_page import show_visualization


# Define functions for other pages (placeholders for now)
def show_clusters():
    st.title("Clusters")
    st.write("Cluster visualization will be implemented here.")


def show_chat():
    st.title("Chat")
    st.write("Chat interface will be implemented here.")


def show_tabs():
    pages = {
        "Visualization": show_visualization,
        "Clusters": show_clusters,
        "Chat": show_chat,
    }

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", list(pages.keys()))

    # Display the selected page
    pages[page]()


# Function to show the home screen
def show_home():
    st.title("🐱 ClipCat")
    youtube_url = st.text_input("Enter a YouTube channel URL:")
    if st.button("Go"):
        # Save the URL in the session state and move to loading screen
        st.session_state.youtube_url = youtube_url
        st.session_state.current_page = "tabs"


# Function to show the loading screen and then automatically transition to the tabs
def show_loading():
    st.title("Loading...")
    st.write("Processing your request. Please wait.")
    # Mock loading process
    time.sleep(5)
    # Transition to the tabs screen after loading
    st.session_state.current_page = "tabs"


# Main app logic to control page flow
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if st.session_state.current_page == "home":
    show_home()
elif st.session_state.current_page == "loading":
    show_loading()
    st.session_state.current_page = "tabs"
elif st.session_state.current_page == "tabs":
    show_tabs()
