import streamlit as st
import requests
from config import BOOKS_URL
from menu import menu_with_redirect
from utils import get_headers, fetch_books_for_admin_pages

st.set_page_config(
    page_title="Add Books",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon=":books:"
)

menu_with_redirect()

headers = get_headers()

try:
    books = fetch_books_for_admin_pages()
except Exception as e:
    st.error(f"Failed to fetch books: {e}")
    st.stop()

if books:
    book_ids = {book["name"]: book["id"] for book in books}
    book_lookup = {book["id"]: book for book in books}
    book_titles = list(book_ids.keys())
    genres = [book['genre'] for book in books]
    genres = sorted(list(set(genres)))
else:
    book_ids = {}
    book_lookup = {}
    book_titles = []
    genres = []

options = ["Title", "Author", "Description", "Genre", "Price"]

with st.container(border=True):
    book_title = st.session_state.book_to_update.get("name") if st.session_state.get("book_to_update") else None
    default_index = book_titles.index(book_title) if book_title in book_titles else 0
    book_title = st.selectbox(label="Select the book to update", options=book_titles, index=default_index)
    book = book_lookup[book_ids[book_title]]

    selected_options  = st.multiselect(label="Select the fields to be updated", options=options, default=None)

    title = st.text_input(label="Title", placeholder="Title of the book", value=book["name"], disabled = not ("Title" in selected_options))
    author = st.text_input(label="Author", placeholder="Name of the author", value=book["author"], disabled = not ("Author" in selected_options))
    description = st.text_area(label="Description", placeholder="Short description of the book", value=book["description"], disabled = not ("Description" in selected_options))
    genre = st.selectbox(label="Genre", options=genres, index=genres.index(book["genre"]), placeholder="Book genre", disabled = not ("Genre" in selected_options), accept_new_options=True)
    price =  st.number_input(label="Price", format="%0.2f", value=book["price"], disabled = not ("Price" in selected_options))

    submit = st.button(label="Update book", use_container_width=True)

    if submit:
        data = {
            "name": title,
            "author": author,
            "description": description,
            "genre": genre,
            "price": price
        }

        with st.spinner(f"Updating {book_title}..."):
            response = requests.put(f"{BOOKS_URL}/{book_ids[book_title]}", json=data, headers=headers)
            
        if response.status_code == 200:
            st.success("Book updated successfully")
        else:
            st.error(f"Failed to update {book_title}: {response.json().get("detail")}")