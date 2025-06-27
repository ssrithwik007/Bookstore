import streamlit as st
from menu import menu_with_redirect

st.set_page_config(
    page_title="Home",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon=":books:"
)

menu_with_redirect()

if st.session_state.role == "user":
    st.title(f"Hello {st.session_state.username}!")
    st.markdown(f"### You are logged in as User")
    st.markdown("---")
    st.markdown("### What would you like to do today?")  
    st.page_link("pages/browse.py", label="Browse Books", use_container_width=True)
    st.page_link("pages/view_cart.py", label="View Cart", use_container_width=True)
    st.page_link("pages/purchase.py", label="View Purchases", use_container_width=True)
    st.markdown("---")
    st.markdown("### Need to update your account?")
    st.page_link("pages/update_account.py", label="Update Account", use_container_width=True)
    st.page_link("pages/delete_account.py", label="Delete Account", use_container_width=True)

elif st.session_state.role == "trail_admin":
    st.title(f"Hello {st.session_state.username}!")
    st.markdown(f"### You are logged in as Trail Admin")
    st.markdown("---")
    st.markdown("### What would you like to do today?")  
    st.page_link("pages/view_books.py", label="View books", use_container_width=True)
    st.page_link("pages/add_books.py", label="Add books", use_container_width=True)
    st.page_link("pages/update_books.py", label="Update books", use_container_width=True)
    st.page_link("pages/delete_books.py", label="Delete books", use_container_width=True)
    st.markdown("---")
    st.markdown("### Need to update your account?")
    st.page_link("pages/update_account.py", label="Update Account", use_container_width=True)
    st.page_link("pages/delete_account.py", label="Delete Account", use_container_width=True)

elif st.session_state.role == "admin":
    st.title(f"Hello {st.session_state.username}!")
    st.markdown(f"### You are logged in as Admin")
    st.markdown("---")
    st.markdown("### What would you like to do today?")  
    st.page_link("pages/view_books.py", label="View books", use_container_width=True)
    st.page_link("pages/add_books.py", label="Add books", use_container_width=True)
    st.page_link("pages/update_books.py", label="Update books", use_container_width=True)
    st.page_link("pages/delete_books.py", label="Delete books", use_container_width=True)
    st.page_link("pages/get_users.py", label="View users", use_container_width=True)
    st.markdown("---")