import streamlit as st
from menu import menu_with_redirect
from utils import fetch_cart, remove_book_from_cart, buy_now_from_cart, checkout_cart, clear_cart

st.set_page_config(
    page_title="View Cart",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon=":books:"
)

menu_with_redirect()

st.title("CART")

@st.dialog("Clear Cart?")
def clear_cart_dialog():
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        if st.button("✅ Yes, Clear", use_container_width=True):
            clear_cart()
            st.rerun()
    with col3:
        if st.button("❌ Cancel",type="primary", use_container_width=True):
            st.stop()

@st.dialog("Checkout?")
def checkout_dialog():
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        if st.button("✅ Yes, Checkout", type="primary",use_container_width=True):
            checkout_cart()
            st.rerun()
    with col3:
        if st.button("❌ Cancel", use_container_width=True):
            st.stop()

cart = fetch_cart()

if cart:
    books = [item["book"] for item in cart]
    
    for book in books:
        with st.container():
            col1, col2, col3, col4 = st.columns([6,2,2,1], vertical_alignment="center")
            with col1:
                st.markdown(f"#### {book['name']}")            
            with col2:
                st.button("Remove Book", key=f"remove_book_{book['id']}", on_click=remove_book_from_cart, args=(book['id'],))
            with col3:
                st.button("Buy now", key=f"buy_now_{book['id']}", on_click=buy_now_from_cart, args=(book['id'],))
            with col4:
                st.markdown(f"₹{book['price']}")
            st.markdown("---")

    c1, c2, c3 = st.columns([6,2,1])
    with c1:
        clear, checkout = st.columns([1, 1])
        with clear:
            with st.container():
                st.button("Clear Cart", type="primary", on_click=clear_cart_dialog)
        with checkout:
            with st.container():
                st.button("Checkout", type="primary", on_click=checkout_dialog)
    with c2:
        st.markdown("### Total")
    with c3:
        total = sum(book["price"] for book in books)
        st.markdown(f"₹{total}")

else:
    st.markdown("## Your cart is empty, Browse some books and add them to yout cart")
    st.page_link("pages/browse.py", label="Browse Books")



