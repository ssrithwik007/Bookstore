import streamlit as st
from menu import menu_with_redirect

menu_with_redirect()

st.title(f"You are now logged in as {st.session_state.role}")