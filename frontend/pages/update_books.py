import streamlit as st
import requests
from config import API_URL
from menu import menu_with_redirect

st.set_page_config(
    page_title="Add Books",
    layout="centered",
    initial_sidebar_state="auto",
)

menu_with_redirect()

url = f"{API_URL}/books"

# Check if token exists
if "access_token" not in st.session_state:
    st.warning("You must be logged in to view this page.")
    st.stop()

headers = {
    "Authorization": f"Bearer {st.session_state.access_token}"
}

with st.container(border=True):
    st.warning("Please only fill the fields which are to be updated")

    title = st.text_input(label="Title", placeholder="Title of the book", value=None)
    author = st.text_input(label="Author", placeholder="Name of the author", value=None)
    description = st.text_area(label="Description", placeholder="Short description of the book", value=None)
    genre = st.text_input(label="Genre", placeholder="Book genre", value=None)
    price =  st.number_input(label="Price", format="%0.2f", value=0.0, value=None)

    submit = st.button(label="Update book")

    if submit:
        if not all([title, author, description, genre, price]):
            st.warning("Please fill all the fields")
        else:
            data = {
                "name": title,
                "author": author,
                "description": description,
                "genre": genre,
                "price": price
            }

            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 201:
                st.success("Book added successfully")
            else:
                st.error(f"Error {response.status_code}: {response.json().get("detail")}")