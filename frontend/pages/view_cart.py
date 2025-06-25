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
checkout_url = f"{API_URL}/users/me/checkout"
purchase_url = f"{API_URL}/users/me/purchases"

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

def remove_book(book_id: int):
    data = {"book_id": book_id, "quantity": 1}
    with st.spinner("Removing book from cart"):
        cart_response = requests.delete(url, json=data, headers=headers)
    if cart_response.status_code == 200:
        st.toast("Book removed from cart")
    else:
        st.toast("Error: Could not remove book from cart")

def clear_cart():
    with st.spinner("Clearing Cart"):
        res = requests.delete(f"{url}/clear", headers=headers)
    if res.status_code == 200:
        st.toast("Cart cleared")
        st.rerun()
    else:
        st.toast("Could not clear cart")

def buy_now(book_id):
    data = {"book_id": book_id, "quantity": 1}
    remove_book(book_id)
    with st.spinner("Buying book"):
        res = requests.post(purchase_url, json=data, headers=headers)
    if res.status_code == 201:
        st.toast("Book purchased successfully!")
    else:
        st.toast("Error: Could not purchase book")
        st.error(f"{res.json().get("detail")}")

def checkout_cart():
    with st.spinner("Checking out cart"):
        res = requests.post(checkout_url, headers=headers)
    if res.status_code == 201:
        st.toast("Cart checked out")
        st.rerun()
    else:
        st.toast("Could not checkout")

cart = fetch_cart()

if cart:
    books = [item["book"] for item in cart]
    
    for book in books:
        with st.container():
            col1, col2, col3, col4 = st.columns([6,2,2,1], vertical_alignment="center")
            with col1:
                st.markdown(f"#### {book['name']}")            
            with col2:
                st.button("Remove Book", key=f"remove_book_{book['id']}", on_click=remove_book, args=(book['id'],))
            with col3:
                st.button("Buy now", key=f"buy_now_{book['id']}", on_click=buy_now, args=(book['id'],))
            with col4:
                st.markdown(f"₹{book['price']}")
            st.markdown("---")

    if "confirm_clear" not in st.session_state:
        st.session_state.confirm_clear = False
    if "confirm_check_out" not in st.session_state:
        st.session_state.confirm_check_out = False

    c1, c2, c3 = st.columns([6,2,1])
    with c1:
        clear, checkout = st.columns([1, 1])
        with clear:
            with st.container():
                if st.session_state.confirm_clear:
                    st.warning("Are you sure you want to clear the cart?")
                    col_a, col_b = st.columns([1, 1])
                    with col_a:
                        if st.button("Yes, Clear"):
                            st.session_state.confirm_clear = False
                            clear_cart()
                    with col_b:
                        if st.button("Cancel"):
                            st.session_state.confirm_clear = False
                else:
                    if st.button("Clear Cart", type="primary"):
                        st.session_state.confirm_clear = True
        with checkout:
            with st.container():
                if st.session_state.confirm_check_out:
                    st.warning("Are you sure you want to checkout?")
                    col_a, col_b = st.columns([1, 1])
                    with col_a:
                        if st.button("Yes, Checkout"):
                            st.session_state.confirm_check_out = False
                            checkout_cart()
                    with col_b:
                        if st.button("Cancel"):
                            st.session_state.confirm_check_out = False
                else:
                    if st.button("Checkout", type="primary"):
                        st.session_state.confirm_check_out = True
    with c2:
        st.markdown("### Total")
    with c3:
        total = sum(book["price"] for book in books)
        st.markdown(f"₹{total}")

else:
    st.markdown("## Your cart is empty, Browse some books and add them to yout cart")
    st.page_link("pages/browse.py", label="Browse Books")



