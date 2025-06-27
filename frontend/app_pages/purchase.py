import streamlit as st
import requests
from menu import menu_with_redirect
from utils import fetch_purchases, refund_book, refund_all_books

st.set_page_config(
    page_title="View Purchases",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon=":books:"
)

menu_with_redirect()

@st.dialog("Refund All Books?")
def refund_all_books_dialog(books):
    st.warning("Are you sure you want to refund all books?")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        if st.button("✅ Yes, Refund All", use_container_width=True):
            refund_all_books(books)
            st.rerun()
    with col3:
        if st.button("❌ Cancel",type="primary", use_container_width=True):
            st.stop()

@st.dialog("Refund Book?")
def refund_book_dialog(book):
    st.warning(f"Are you sure you want to refund {book['name']}?")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        if st.button("✅ Yes, Refund", use_container_width=True):
            refund_book(book['id'])
            st.rerun()
    with col3:
        if st.button("❌ Cancel", type="primary", use_container_width=True):
            st.stop()

purchases = fetch_purchases()

if purchases:
    books = [item["book"] for item in purchases]
    books_per_col = 3

    with st.container():
        st.button("Refund All Books", type="primary", on_click=refund_all_books_dialog, args=(books,))

    for i in range(0, len(books), books_per_col):
        cols = st.columns(books_per_col, border=True)

        for col, book in zip(cols, books[i:i+books_per_col]):
            with col:
                with st.container(height=270, border=False):
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
                    col1, col2, col3 = st.columns([1,2,1], vertical_alignment="bottom")
                    with col2:  
                        st.button("Refund Book", key=f"refund_book_{book['id']}", type="primary", on_click=refund_book_dialog, args=(book,), use_container_width=True)
else:
    st.markdown("## You have not purchased any books yet, Browse some books and add purchase them")
    st.page_link("app_pages/browse.py", label="Browse Books")