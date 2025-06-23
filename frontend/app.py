import streamlit as st
import requests
from config import API_URL
from menu import menu

st.set_page_config(
    page_title="Rithwik's Bookstore",
    page_icon=":books:",
    layout="wide"
)

if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "role" not in st.session_state:
    st.session_state.role = None

st.session_state._role = st.session_state.role

def set_role():
    st.session_state.role = st.session_state._role

col1, col2, col3 = st.columns(3)

with col2:
    st.title("Welcome to Rithwik's Bookstore!")

    if st.session_state.get("go_to_login"):
        st.session_state.go_to_login = False
        st.session_state.access_token = None
        st.session_state.role = None
        st.success("Account created! Please log in below")

    with st.form(enter_to_submit=False, border=True, key="login form"):
        c1,c2,c3 = st.columns(3)
        with c2:
            st.header("Log in")
        username = st.text_input(label="Username", placeholder="Enter username")
        password = st.text_input(label="Password", placeholder="Enter password", type="password")
        
        submit = st.form_submit_button(label="Log in")

        st.page_link(page="pages/create-account.py", label="New user? Create Account", help="click here to create a new account")

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
            response_data = response.json()

            if response.status_code == 200:
                st.session_state.access_token = response_data["access_token"]
                st.session_state.role = response_data["role"]
                st.success("Login successful!")
                menu()
                st.switch_page("pages/home.py")
            else:
                st.error(response_data["detail"])

