import streamlit as st
from menu import menu_with_redirect
from utils import add_book_to_cart, buy_now_from_browse, fetch_books

st.set_page_config(
    page_title="Browse Books",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon=":books:"
)

menu_with_redirect()

st.title("BOOKS")

@st.dialog("Buy Book?")
def buy_book_dialog(book):
    st.warning(f"Are you sure you want to buy {book['name']}?")
    col1, col2 = st.columns([1, 1], vertical_alignment="center")
    with col1:
        if st.button("✅ Yes, Buy", type="primary", use_container_width=True):
            buy_now_from_browse(book['id'])
            st.rerun()
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()

books = fetch_books()
if books:
    books_per_col = 3
    for i in range(0, len(books), books_per_col):
        cols = st.columns(books_per_col, border=True)

        for col, book in zip(cols, books[i:i+books_per_col]):
            with col:
                with st.container(height=250, border=False):
                    col1, col2 = st.columns([4, 1], vertical_alignment="center")
                    with col1:
                        st.markdown(f"### {book['name']}")
                    with col2:
                        st.markdown(f"**₹{book['price']}**")
                    st.markdown(f"**Author:** {book['author']}")
                    st.markdown(f"**Genre:** {book['genre']}")
                    st.markdown(f"**Description:** {book['description']}")
                st.markdown("---")
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([1, 4, 1, 4, 1], vertical_alignment="bottom")
                    with col2:
                        st.button("Add to cart", key=f"add_book_{book["id"]}", on_click=add_book_to_cart, args=(book['id'],), use_container_width=True)
                    with col4:
                        st.button("Buy now", key=f"buy_now_{book["id"]}", on_click=buy_book_dialog, args=(book,), use_container_width=True)

else:
    st.error("Failed to fetch books.")