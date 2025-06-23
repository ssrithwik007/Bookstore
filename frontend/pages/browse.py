import streamlit as st
import requests
from config import API_URL
from menu import menu_with_redirect

menu_with_redirect()

response = requests.get(API_URL+"/books")

if response.status_code == 200:
    books = response.json()
    for book in books:
        with st.expander(label=book["name"]):
            st.text(f"Author: {book["author"]}")
            st.text(f"Genre: {book["genre"]}")
            st.text(f"Description: {book["description"]}")
            st.text(f"Price: {str(book["price"])}")

            add_button = st.button(label="Add to cart")
            if add_button:
                data = {
                    "book_id": book["id"],
                    "quantity": 1
                }
                response = requests.post(f"{API_URL}/users/me/cart")
else:
    st.error(f"Failed to fetch books. Status code: {response.status_code}")