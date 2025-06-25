import streamlit as st
import pandas as pd
import requests
from config import API_URL
from menu import menu_with_redirect

st.set_page_config(
    page_title="Delete Account",
    layout="centered",
    initial_sidebar_state="auto",
)

menu_with_redirect()

url = f"{API_URL}/users"

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
        
        st.error("Are you sure you want to delete the account?")
        if st.session_state.role == "user":
            st.text("All of you purchases and cart will be deleted")
        if st.session_state.role == "trail_admin":
            st.text("All the books which you have added will be deleted")
        
        col1, col2 = st.columns([1,1])

        with col1:
            if st.button("No, Keep my account", key="redirect"):
                st.switch_page("pages/home.py")

        with col2:
            if st.button("Yes, Delete my account", type="primary", key="delete"):

                with st.spinner("Deleting account, please do not exit"):
                    del_response = requests.delete(f"{url}/me", headers=headers)

                if del_response.status_code == 200:
                    st.success("Deleted Account successfully, Redirecting to Login")
                    st.session_state.role = None
                    st.switch_page("app.py")

                else:
                    if del_response.headers.get("Content-Type") == "application/json":
                        error_detail = del_response.json().get("detail")
                    else:
                        error_detail = del_response.text

                    st.error(f"Failed to update details: {error_detail}")

else:
    st.error(f"Failed to fetch user: {response.json().get('detail')}")