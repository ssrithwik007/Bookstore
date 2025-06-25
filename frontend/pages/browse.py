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

def add_book(book_id: int):
    data = {"book_id": book_id, "quantity": 1}
    
    with st.spinner("Adding to cart"):
        res = requests.post(cart_url, json=data, headers=headers)

    if res.status_code == 201:
        st.toast("Book added to cart")
    else:
        st.toast("Error: Could not add book to cart")
        st.error(f"{res.json().get("detail")}")

def buy_now(book_id):
    data = {"book_id": book_id, "quantity": 1}
    with st.spinner("Buying book"):
        res = requests.post(purchase_url, json=data, headers=headers)
    if res.status_code == 201:
        st.toast("Book purchased successfully!")
    else:
        st.toast("Error: Could not purchase book")
        st.error(f"{res.json().get("detail")}")

def fetch_books():
    with st.spinner("Fetching books"):
        response = requests.get(url)
        cart_response = requests.get(cart_url, headers=headers)
        purchase_response = requests.get(purchase_url, headers=headers)
    if response.status_code == 200 and cart_response.status_code == 200 and purchase_response.status_code == 200:
        books = response.json()
        cart = cart_response.json()
        purchases = purchase_response.json()
        cart_ids = {item["book"]["id"] for item in cart}
        purchase_ids = {item["book"]["id"] for item in purchases}
        books_to_display = [book for book in books if book["id"] not in cart_ids and book["id"] not in purchase_ids]
        return books_to_display
    else:
        return False

books = fetch_books()
if books:
    books_per_col = 3
    for i in range(0, len(books), books_per_col):
        cols = st.columns(books_per_col, border=True)

        for col, book in zip(cols, books[i:i+books_per_col]):
            with col:
                with st.container(height=270, border=False):
                    st.markdown(f"### {book['name']}")
                    st.markdown(f"**Author:** {book['author']}")
                    st.markdown(f"**Genre:** {book['genre']}")
                    st.markdown(f"**Description:** {book['description']}")
                    st.markdown(f"**Price:** ₹{book['price']}")
                st.markdown("---")
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([1, 5, 1, 5, 1], vertical_alignment="bottom")
                    with col2:
                        st.button("Add to cart", key=f"add_book_{book["id"]}", on_click=add_book, args=(book['id'],))
                    with col4:
                        st.button("\u00A0\u00A0Buy now\u00A0\u00A0", key=f"buy_now_{book["id"]}", on_click=buy_now, args=(book['id'],))

else:
    st.error(f"Failed to fetch books.")