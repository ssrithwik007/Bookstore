import streamlit as st
import requests
from config import API_URL

col1, col2, col3 = st.columns(3)

with col2:
    with st.form(key="new user form", enter_to_submit=False):
        st.header("Create Account")

        username = st.text_input(label="Username", placeholder="Enter username")
        email = st.text_input(label="Email", placeholder="xyz@email.com")
        password = st.text_input(label="Password", placeholder="Enter password (atleast 8 characters)", type="password")
        if password.__len__() < 8:
            st.warning("Password length must be atleast 8 characters long")
        re_password = st.text_input(label="Re-Enter Password", placeholder="Re-Enter password", type="password")

        role = st.selectbox(label="Choose your role", options=["user", "trail_admin"])

        submit = st.form_submit_button(label="Log in")

    if submit:
        if not username or not email or not password or not re_password:
            if not username:
                st.warning("Please enter username")
            if not email:
                st.warning("Please enter email")
            if not password:
                st.warning("Please enter password")
            if not re_password:
                st.warning("Please re-enter password")
        elif (password and re_password) and (password != re_password):
            st.warning("The two passwords are not matching")
        else:
            data = {
                "username": username,
                "email": email,
                "password": password,
                "role": role
            }
            response = requests.post(f"{API_URL}/users", json=data)

            if response.status_code == 201:
                st.success("Account created successfully!")
                st.session_state.go_to_login = True
                st.page_link(page="app.py", label="Click here to log in")
            elif response.status_code == 409:
                st.error(response.json().get("detail", "Account already exists"))
            else:
                st.error("Failed to create account, please try again")

