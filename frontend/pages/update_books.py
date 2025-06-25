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

response = requests.get(url=url)
books = response.json()
book_ids = {book["name"]: book["id"] for book in books}
book_lookup = {book["id"]: book for book in books}
book_titles = list(book_ids.keys())

options = ["Title", "Author", "Description", "Genre", "Price"]

with st.container(border=True):
    if "book_id" in st.session_state:
        book_id = st.session_state.book_id
        book_title = next((title for title, id in book_ids.items() if id == book_id), None)
        st.session_state.book = None
    else:
        book_title = None

    default_index = book_titles.index(book_title) if book_title in book_titles else 0

    book_title = st.selectbox(label="Select the book to update", options=book_titles, index=default_index)

    book = book_lookup[book_ids[book_title]]

    selected_options  = st.multiselect(label="Select the fields to be updated", options=options, default=None)

    title = st.text_input(label="Title", placeholder="Title of the book", value=book["name"], disabled = not ("Title" in selected_options))
    author = st.text_input(label="Author", placeholder="Name of the author", value=book["author"], disabled = not ("Author" in selected_options))
    description = st.text_area(label="Description", placeholder="Short description of the book", value=book["description"], disabled = not ("Description" in selected_options))
    genre = st.text_input(label="Genre", placeholder="Book genre", value=book["genre"], disabled = not ("Genre" in selected_options))
    price =  st.number_input(label="Price", format="%0.2f", value=book["price"], disabled = not ("Price" in selected_options))

    submit = st.button(label="Update book")

    if submit:
        data = {
            "name": title,
            "author": author,
            "description": description,
            "genre": genre,
            "price": price
        }

        response = requests.put(f"{url}/{book_ids[book_title]}", json=data, headers=headers)
        
        if response.status_code == 200:
            st.success("Book updated successfully")
        else:
            st.error(f"Failed to update {book_title}: {response.json().get("detail")}")