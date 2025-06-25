import streamlit as st
import requests
from config import API_URL
from menu import menu_with_redirect

st.set_page_config(
    page_title="View Cart",
    page_icon=":books:",
    layout="wide"
)

menu_with_redirect()

st.title("CART")

url = f"{API_URL}/users/me/cart"

headers = {
    "Authorization": f"Bearer {st.session_state.access_token}"
}

def fetch_cart():
    with st.spinner("Fetching your cart"):
        response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.json() != []:
        return response.json()
    elif response.status_code == 200 and response.json() == []:
        return []
    else:
        st.error(f"Failed to fetch cart")

book_to_remove_id = None
for key in st.session_state.keys():
    if key.startswith("remove_book_") and st.session_state[key]:
        book_to_remove_id = int(key.replace("remove_book_", ""))
        st.session_state[key] = False
        break

if book_to_remove_id is not None:
    data = {"book_id": book_to_remove_id, "quantity": 1}

    with st.spinner("Removing book from cart"):
        cart_response = requests.delete(url, json=data, headers=headers)

    if cart_response.status_code == 200:
        st.toast("Book removed from cart")
        st.rerun()
    else:
        st.toast("Error: Could not remove book from cart")


cart = fetch_cart()

if cart:
    books = [item["book"] for item in cart]
    book_ids = {book["name"]:book["id"] for book in books}
    book_lookup = {book["id"]:book for book in books}
    
    for book in books:
        with st.container():
            col1, col2, col3 = st.columns([6,2,1])
            with col1:
                st.markdown(f"{book['name']}")            
            with col2:
                st.button("Remove Book", key=f"remove_book_{book['id']}")
            with col3:
                st.markdown(f"***₹{book['price']}***")
            st.markdown("---")

    c1, c2, c3 = st.columns([6,2,1])
    with c2:
        st.markdown("### Total")
    with c3:
        total = sum(book["price"] for book in books)
        st.markdown(f"***₹{total}***")
else:
    st.markdown("## Your cart is empty, Browse some books and add them to yout cart")
    st.page_link("pages/browse.py", label="Browse Books")



