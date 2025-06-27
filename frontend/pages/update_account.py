import streamlit as st
import re
import requests
from config import API_URL
from menu import menu_with_redirect

st.set_page_config(
    page_title="Update Credentials",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon=":books:"
)

menu_with_redirect()

url = f"{API_URL}/users"
email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"

if "access_token" not in st.session_state:
    st.warning("You must be logged in to view this page.")
    st.stop()

headers = {
    "Authorization": f"Bearer {st.session_state.access_token}"
}

with st.spinner("Fetching user details"):
    response = requests.get(f"{url}/me", headers=headers)

if response.status_code == 200:
    user_data = response.json()

    with st.container(border=True):
        selected_options  = st.multiselect(label="Select the fields to be updated", options=["Username", "Email", "Password"], default=None)

        username = st.text_input(label="Username", placeholder="Enter username", value=user_data["username"], disabled= not ("Username" in selected_options))
        email = st.text_input(label="E-Mail", placeholder="Enter e-mail", value=user_data["email"], disabled= not ("Email" in selected_options))
        if "Email" in selected_options and not re.match(email_pattern, email or ""):
            st.warning("Enter a valid email address")
        password = st.text_input(label="Password", placeholder="Enter new password", type="password", disabled= not ("Password" in selected_options))
        re_password = st.text_input(label="Re-Enter Password", placeholder="Re-Enter password", type="password", disabled= not ("Password" in selected_options))
        if "Password" in selected_options and len(password) < 8:
            st.warning("Password length must be atleast 8 characters long")

        is_pwd_valid = ("Password" not in selected_options or ((len(password) >= 8) and (password == re_password)))
        is_email_valid = ("Email" not in selected_options or (re.match(email_pattern, email or "")))

        if st.button("Update", disabled= not(is_pwd_valid and is_email_valid)):
            if "Password" in selected_options and len(password) < 8:
                st.error("Password length must be atleast 8 characters long")
            elif "Password" in selected_options and (password and re_password) and (password != re_password):
                st.warning("The two passwords are not matching")
            else:
                data = {}
                if "Username" in selected_options:
                    data["username"] = username
                if "Email" in selected_options:
                    data["email"] = email
                if "Password" in selected_options and password.strip():
                    data["password"] = password

                with st.spinner("Updating account details..."):
                    update_response = requests.put(f"{url}/me", json=data, headers=headers)

                if update_response.status_code == 200:
                    st.success("Updated account details")
                else:
                    if update_response.headers.get("Content-Type") == "application/json":
                        error_detail = update_response.json().get("detail", "Unknown error")
                    else:
                        error_detail = update_response.text

                    st.error(f"Failed to update details: {error_detail}")

else:
    st.error(f"Failed to fetch user: {response.json().get('detail')}")