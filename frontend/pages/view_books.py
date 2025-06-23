import streamlit as st
import requests
from config import API_URL
from menu import menu_with_redirect

menu_with_redirect()

st.title("BOOKS")

response = requests.get(f"{API_URL}/books")

if response.status_code == 200:
    books = response.json()
    for book in books:
        with st.expander(label=book["name"]):
            st.text(f"Author: {book["author"]}")
            st.text(f"Genre: {book["genre"]}")
            st.text(f"Description: {book["description"]}")
            st.text(f"Price: {str(book["price"])}")
else:
    st.error(f"Failed to fetch books. Status code: {response.status_code}")