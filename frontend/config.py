import streamlit as st

try:
    API_URL = st.secrets["api"]["url"]
except KeyError:
    st.error("API URL not found in secrets.toml. Please ensure it's configured under [api] url.")
    st.stop()

BOOKS_URL = f"{API_URL}/books"

USERS_URL = f"{API_URL}/users/me"

CART_URL = f"{API_URL}/users/me/cart"

PURCHASE_URL = f"{API_URL}/users/me/purchases"

CHECKOUT_URL = f"{API_URL}/users/me/checkout"

