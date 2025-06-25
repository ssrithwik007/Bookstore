import streamlit as st
import pandas as pd
import requests
from config import API_URL
from menu import menu_with_redirect

menu_with_redirect()

# Protected route
url = f"{API_URL}/users"

# Check if token exists
if "access_token" not in st.session_state:
    st.warning("You must be logged in to view this page.")
    st.stop()

headers = {
    "Authorization": f"Bearer {st.session_state.access_token}"
}

with st.spinner("Fetching users from the database"):
    response = requests.get(url, headers=headers)

users = response.json()

df = pd.DataFrame([{
    "ID": user["id"],
    "Username": user["username"],
    "Email": user["email"],
    "Role": user["role"]
    } for user in users])   

if response.status_code == 200:
    st.table(df)
else:
    error_detail = response.json().get("detail", "Something went wrong.")
    st.error(f"Error {response.status_code}: {error_detail}")