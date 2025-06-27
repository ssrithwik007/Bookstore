import streamlit as st
import requests
from config import BOOKS_URL
from menu import menu_with_redirect
from utils import get_headers, fetch_books_for_admin_pages
import time

st.set_page_config(
    page_title="Add Books",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon=":books:"
)

menu_with_redirect()

headers = get_headers()

books = fetch_books_for_admin_pages()

if books:
    genres = [book['genre'] for book in books]
    genres = sorted(list(set(genres)))    
else:
    genres = []


with st.container(border=True):
    title = st.text_input(label="Title", placeholder="Title of the book", value=None)
    author = st.text_input(label="Author", placeholder="Name of the author", value=None)
    description = st.text_area(label="Description", placeholder="Short description of the book", value=None)
    genre = st.selectbox(label="Genre", options=genres, index=0, placeholder="Select a genre", accept_new_options=True)
    price =  st.number_input(label="Price", format="%0.2f", value=0.0)
    submit = st.button(label="Add book", use_container_width=True, disabled=not all([title, author, description, genre, price]))

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

            with st.spinner("Adding book..."):
                response = requests.post(BOOKS_URL, json=data, headers=headers)
                time.sleep(2)
            if response.status_code == 201:
                st.toast("Book added successfully", icon="🎉")
                time.sleep(2)
                st.rerun()
            else:
                if response.headers.get("Content-Type") == "application/json":
                    error_detail = response.json().get("detail", "Unknown error")
                else:
                    error_detail = response.text
                st.toast(f"Failed to add book: {error_detail}", icon="❌")
                time.sleep(2)
                st.rerun()