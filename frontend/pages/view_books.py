import streamlit as st
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

headers = {
    "Authorization": f"Bearer {st.session_state.access_token}"
}

with st.spinner("Fetching books"):
    response = requests.get(url)

if response.status_code == 200:
    books = response.json()
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

                    col1, col2 = st.columns([1,1])

                    with col1:
                        if st.button(label="Update Book", key=f"update{book['id']}"):
                            st.session_state.book_id = book["id"]
                            st.switch_page("pages/update_books.py")
                    with col2:
                        if st.button(label="Delete Book", key=f"delete{book['id']}"):
                            with st.spinner("Deleting book"):
                                del_response = requests.delete(f"{url}/{book["id"]}", headers=headers)
                            if del_response.status_code == 200:
                                st.toast(f"{book["name"]} deleted successfully", icon="✅")
                                st.rerun()
                            else:
                                st.toast(f"Failed to delete {book['name']}: {del_response.json().get('detail')}", icon="❌")
else:
    st.error(f"Failed to fetch books. Status code: {response.status_code}")