import streamlit as st
from menu import menu_with_redirect
from utils import fetch_books_for_admin_pages, delete_book

st.set_page_config(
    page_title="View Books",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon=":books:"
)

menu_with_redirect()

st.title("BOOKS")

books = fetch_books_for_admin_pages()

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
                    col1, col2 = st.columns([1,1])
                    with col1:
                        if st.button(label="Update Book", key=f"update{book['id']}", use_container_width=True):
                            st.session_state.book_to_update = book
                            st.switch_page("pages/update_books.py")
                    with col2:
                        if st.button(label="Delete Book", key=f"delete{book['id']}", use_container_width=True):
                            delete_book(book["id"])
else:
    st.error(f"Failed to fetch books")