import streamlit as st
from functools import partial
import requests
from config import API_URL
from menu import menu_with_redirect

st.set_page_config(
    page_title="View Books",
    page_icon=":books:",
    layout="wide"
)

menu_with_redirect()

st.title("BOOKS")

url = f"{API_URL}/books"
cart_url = f"{API_URL}/users/me/cart"
purchase_url = f"{API_URL}/users/me/purchases"

headers = {
    "Authorization": f"Bearer {st.session_state.access_token}"
}

def fetch_books():
    with st.spinner("Fetching books"):
        response = requests.get(url)
        cart_response = requests.get(cart_url, headers=headers)
        purchase_response = requests.get(purchase_url, headers=headers)
    if response.status_code == 200 and cart_response.status_code == 200 and purchase_response.status_code == 200:
        books = response.json()
        cart = cart_response.json()
        cart_books = [item["book"] for item in cart] if cart else []
        purchases = purchase_response.json()
        cart_ids = {book["id"] for book in cart_books}
        purchase_ids = {book["id"] for book in purchases}
        books_to_display = [book for book in books if book["id"] not in cart_ids and book["id"] not in purchase_ids]
        return books_to_display
    else:
        return False

book_to_add_id = None
for key in st.session_state.keys():
    if key.startswith("add_book_") and st.session_state[key]:
        book_to_add_id = int(key.replace("add_book_", ""))
        st.session_state[key] = False
        break

if book_to_add_id is not None:
    data = {"book_id": book_to_add_id, "quantity": 1}

    with st.spinner("Adding to cart"):
        res = requests.post(cart_url, json=data, headers=headers)

    if res.status_code == 201:
        st.toast("Book added to cart")
        st.rerun()
    else:
        st.toast("Error: Could not add book to cart")
        st.error(f"{res.json().get("detail")}")

books = fetch_books()
if books:
    books_per_col = 3
    for i in range(0, len(books), books_per_col):
        cols = st.columns(books_per_col, border=True)

        for col, book in zip(cols, books[i:i+books_per_col]):
            with col:
                with st.container():
                    st.markdown(f"### {book['name']}")
                    st.markdown(f"**Author:** {book['author']}")
                    st.markdown(f"**Genre:** {book['genre']}")
                    st.markdown(f"**Description:** {book['description']}")
                    st.markdown(f"**Price:** ₹{book['price']}")

                    st.button("Add to cart", key=f"add_book_{book["id"]}")

else:
    st.error(f"Failed to fetch books.  {books}")