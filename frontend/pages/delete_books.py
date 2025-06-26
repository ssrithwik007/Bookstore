import streamlit as st
import requests
from config import API_URL
from menu import menu_with_redirect

st.set_page_config(
    page_title="Delete Books",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon=":books:"
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

with st.container():
    book_titles = st.multiselect(label="Select the books to delete", options=list(book_ids.keys()))

    submit = st.button(label="Delete books")

    if submit:
        for book_title in book_titles:
            with st.spinner(f"Deleting {book_title}..."):
                response = requests.delete(f"{url}/{book_ids[book_title]}", headers=headers)
            if response.status_code == 200:
                st.success(f"{book_title} deleted successfully")
            else:
                st.error(f"Failed to delete {book_title}: {response.json().get("detail")}")