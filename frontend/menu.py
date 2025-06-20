import streamlit as st

def authenticated_menu():
    st.sidebar.page_link("1_login", "Logout", "Logout from your account")
    st.sidebar.page_link("pages/2_browse.py", "Browse Books", "Browse available books")