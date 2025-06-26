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



