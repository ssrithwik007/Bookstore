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


try:
    books = fetch_books()
except Exception as e:
    st.error(f"Failed to fetch books: {e}")
    st.stop()


if books:
    genres = [book['genre'] for book in books]
    genres = sorted(list(set(genres)))
    genres.insert(0, "All")
    sort_by_options = ["None", "Price - Low to High", "Price - High to Low", "Title - A to Z", "Title - Z to A"]

    with st.container():
        col1, col2, col3 = st.columns([1,1,4])
        with col1:
            with st.container():
                filter_by = st.selectbox("Filter by", options=genres, index=0)
        with col2:
            with st.container():
                sort_by = st.selectbox("Sort by", options=sort_by_options, index=0)
        with col3:
            with st.container():
                search_by = st.text_input("Search by", placeholder="Search by title, author", value=None)

    if filter_by != "All":
        books = [book for book in books if book['genre'] == filter_by]
    if sort_by != "None":
        if sort_by == "Price - Low to High":
            books = sorted(books, key=lambda x: x['price'])
        elif sort_by == "Price - High to Low":
            books = sorted(books, key=lambda x: x['price'], reverse=True)
        elif sort_by == "Title - A to Z":
            books = sorted(books, key=lambda x: x['name'])
        elif sort_by == "Title - Z to A":
            books = sorted(books, key=lambda x: x['name'], reverse=True)

    if search_by:
        books = [book for book in books if search_by.lower() in book['name'].lower() or search_by.lower() in book['author'].lower()]

    if not books:
        st.error("No books found. Maybe try a different filter or search or Try searching in your cart or purchases")
        st.stop()

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
    st.error("No books found.")