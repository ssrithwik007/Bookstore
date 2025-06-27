import streamlit as st
from menu import menu_with_redirect
from utils import delete_account

st.set_page_config(
    page_title="Delete Account",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon=":books:"
)

menu_with_redirect()

with st.container(border=True):
    st.error("Are you sure you want to delete the account?")
    with st.container():
        if st.session_state.role == "user":
            st.text("All the items in your cart will be deleted and all the books you have purchased will be refunded")
        if st.session_state.role == "trail_admin":
            st.text("All the books which you have added will be deleted")
    st.markdown("---")
    with st.container():
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("No, Keep my account", type="primary", key="redirect", use_container_width=True):
                st.switch_page("app_pages/home.py")
        with col2:
            if st.button("Yes, Delete my account", key="delete", on_click=delete_account, use_container_width=True):
                st.switch_page("app_pages/home.py")
