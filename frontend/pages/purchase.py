import streamlit as st
import requests
from config import API_URL
from menu import menu_with_redirect

st.set_page_config(
    page_title="View Purchases",
    page_icon=":books:",
    layout="wide"
)

menu_with_redirect()

url = f"{API_URL}/users/me/purchases"

headers = {
    "Authorization": f"Bearer {st.session_state.access_token}"
}

def refund_book(book_id):
    refund_url = f"{url}/{book_id}"
    with st.spinner("Processing refund..."):
        res = requests.delete(refund_url, headers=headers)
    if res.status_code == 201:
        st.toast("Book refunded successfully!")
    else:
        st.error("Failed to refund book")

def fetch_purchases():
    with st.spinner("Fetching your purchases"):
        response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch purchases")

purchases = fetch_purchases()

if purchases:
    books = [item["book"] for item in purchases]
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

                    st.button("Refund Book", key=f"refund_book_{book['id']}", type="primary", on_click=refund_book, args=(book['id'],))
else:
    st.markdown("## You have not purchased any books yet, Browse some books and add purchase them")
    st.page_link("pages/browse.py", label="Browse Books")