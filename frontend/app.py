import streamlit as st
import requests
from config import API_URL
from menu import menu

st.set_page_config(
    page_title="Rithwik's Bookstore",
    page_icon=":books:",
    layout="centered"
)

if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "role" not in st.session_state:
    st.session_state.role = None

st.session_state._role = st.session_state.role

def set_role():
    st.session_state.role = st.session_state._role

c1, c2, c3 = st.columns([1.7, 51, 1.7])

with c2:
    st.markdown("# Welcome to Rithwik's Bookstore")

    if st.session_state.get("go_to_login"):
        st.session_state.go_to_login = False
        st.session_state.access_token = None
        st.session_state.role = None
        st.success("Account created! Please log in below")

col1, col2, col3 = st.columns([1, 5, 1])

with col2:
    with st.container(border=True):
        c1, c2, c3 = st.columns([1.5, 1.2, 1.5])
        with c2:
            st.header("Log in")
        username = st.text_input(label="Username", placeholder="Enter username", value=None)
        password = st.text_input(label="Password", placeholder="Enter password", type="password", value=None)
        st.markdown("---")

        submit = st.button(label="Log in", use_container_width=True, type="primary")

        c1, c2, c3 = st.columns([1.2, 2, 1.2])
        with c2:
            st.page_link(page="pages/create-account.py", label="\u00A0\u00A0New user? Create Account", use_container_width=True)

    if submit:
        if not username or not password:
            if not username:
                st.warning("Please enter username")
            if not password:
                st.warning("Please enter password")
        else:
            data = {
                "username": username,
                "password": password
            }
            response = requests.post(API_URL+"/login", data=data)
            if response.headers.get("Content-Type", "").startswith("application/json") and response.text.strip():
                response_data = response.json()
            else:
                response_data = {}

            if response.status_code == 200:
                st.session_state.access_token = response_data["access_token"]
                st.session_state.role = response_data["role"]
                st.success("Login successful!")
                menu()
                st.switch_page("pages/home.py")
            else:
                if response.headers.get("Content-Type") == "application/json":
                    error_detail = response.json().get("detail", "Unknown error")
                else:
                    error_detail = response.text

                st.error(f"Failed to log in: {error_detail}")

