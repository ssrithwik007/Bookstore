import requests
import streamlit as st
from config import API_URL, BOOKS_URL, CART_URL, PURCHASE_URL, CHECKOUT_URL

def get_headers():
    if "access_token" not in st.session_state:
        st.warning("You must be logged in to view this page.")
        st.stop()
    return {
        "Authorization": f"Bearer {st.session_state.access_token}"
    }

# VIEW BOOKS PAGE

def fetch_books_for_admin_pages():
    headers = get_headers()
    with st.spinner("Fetching books..."):
        response = requests.get(BOOKS_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        if response.headers.get("Content-Type") == "application/json":
            error_detail = response.json().get("detail")
        else:
            error_detail = response.text
        st.error(f"Failed to fetch books: {error_detail}")

def delete_book(book_id: int):
    headers = get_headers()
    with st.spinner("Deleting book"):
        del_response = requests.delete(f"{BOOKS_URL}/{book_id}", headers=headers)
    if del_response.status_code == 200:
        st.toast(f"Book deleted successfully", icon="✅")
        st.rerun()
    else:
        if del_response.headers.get("Content-Type") == "application/json":
            error_detail = del_response.json().get("detail")
        else:
            error_detail = del_response.text
        st.toast(f"Failed to delete book: {error_detail}", icon="❌")

# BROWSE PAGE

def add_book_to_cart(book_id: int):
    headers = get_headers()
    data = {"book_id": book_id, "quantity": 1}
    with st.spinner("Adding to cart..."):
        res = requests.post(CART_URL, json=data, headers=headers)
    if res.status_code == 201:
        st.toast("Book added to cart", icon="✅")
    else:
        st.toast("Error: Could not add book to cart", icon="❌")
        if res.headers.get("Content-Type") == "application/json":
            error_detail = res.json().get("detail")
        else:
            error_detail = res.text
        st.toast(f"Failed to add book to cart: {error_detail}", icon="❌")

def buy_now_from_browse(book_id):
    headers = get_headers()
    data = {"book_id": book_id, "quantity": 1}
    with st.spinner("Buying book..."):
        res = requests.post(PURCHASE_URL, json=data, headers=headers)
    if res.status_code == 201:
        st.toast("Book purchased successfully!", icon="✅")
        st.balloons()
    else:
        if res.headers.get("Content-Type") == "application/json":
            error_detail = res.json().get("detail")
        else:
            error_detail = res.text
        st.toast(f"Failed to purchase book: {error_detail}", icon="❌")

def fetch_books():
    headers = get_headers()
    with st.spinner("Fetching books..."):
        response = requests.get(BOOKS_URL)
        cart_response = requests.get(CART_URL, headers=headers)
        purchase_response = requests.get(PURCHASE_URL, headers=headers)
    if response.status_code == 200 and cart_response.status_code == 200 and purchase_response.status_code == 200:
        books = response.json()
        cart = cart_response.json()
        purchases = purchase_response.json()
        cart_ids = {item["book"]["id"] for item in cart}
        purchase_ids = {item["book"]["id"] for item in purchases}
        books_to_display = [book for book in books if book["id"] not in cart_ids and book["id"] not in purchase_ids]
        return books_to_display
    else:
        return False

# VIEW CART PAGE

def fetch_cart():
    headers = get_headers()
    with st.spinner("Fetching your cart..."):
        response = requests.get(CART_URL, headers=headers)
    if response.status_code == 200 and response.json() != []:
        return response.json()
    elif response.status_code == 200 and response.json() == []:
        return []
    else:
        if response.headers.get("Content-Type") == "application/json":
            error_detail = response.json().get("detail")
        else:
            error_detail = response.text
        st.error(f"Failed to fetch cart: {error_detail}")

def remove_book_from_cart(book_id: int):
    headers = get_headers()
    data = {"book_id": book_id, "quantity": 1}
    with st.spinner("Removing book from cart..."):
        cart_response = requests.delete(CART_URL, json=data, headers=headers)
    if cart_response.status_code == 200:
        st.toast("Book removed from cart", icon="✅")
    else:
        if cart_response.headers.get("Content-Type") == "application/json":
            error_detail = cart_response.json().get("detail")
        else:
            error_detail = cart_response.text
        st.toast(f"Failed to remove book from cart: {error_detail}", icon="❌")

def clear_cart():
    headers = get_headers()
    with st.spinner("Clearing Cart..."):
        res = requests.delete(f"{CART_URL}/clear", headers=headers)
    if res.status_code == 200:
        st.toast("Cart cleared", icon="✅")
        st.rerun()
    else:
        if res.headers.get("Content-Type") == "application/json":
            error_detail = res.json().get("detail")
        else:
            error_detail = res.text
        st.toast(f"Failed to clear cart: {error_detail}", icon="❌")

def buy_now_from_cart(book_id):
    headers = get_headers()
    data = {"book_id": book_id, "quantity": 1}
    remove_book_from_cart(book_id)
    with st.spinner("Buying book..."):
        res = requests.post(PURCHASE_URL, json=data, headers=headers)
    if res.status_code == 201:
        st.toast("Book purchased successfully!", icon="✅")
        st.balloons()
    else:
        if res.headers.get("Content-Type") == "application/json":
            error_detail = res.json().get("detail")
        else:
            error_detail = res.text
        st.toast(f"Failed to purchase book: {error_detail}", icon="❌")

def checkout_cart():
    headers = get_headers()
    with st.spinner("Checking out cart..."):
        res = requests.post(CHECKOUT_URL, headers=headers)
    if res.status_code == 201:
        st.toast("Cart checked out", icon="✅")
        st.balloons()
        st.rerun()
    else:
        if res.headers.get("Content-Type") == "application/json":
            error_detail = res.json().get("detail")
        else:
            error_detail = res.text
        st.toast(f"Failed to checkout cart: {error_detail}", icon="❌")

# VIEW PURCHASES PAGE

def refund_book(book_id):
    headers = get_headers()
    refund_url = f"{PURCHASE_URL}/{book_id}"
    with st.spinner("Processing refund..."):
        res = requests.delete(refund_url, headers=headers)
    if res.status_code == 200:
        st.toast("Book refunded successfully!", icon="✅")
    else:
        if res.headers.get("Content-Type") == "application/json":
            error_detail = res.json().get("detail")
        else:
            error_detail = res.text
        st.toast(f"Failed to refund book: {error_detail}", icon="❌")

def fetch_purchases():
    headers = get_headers()
    with st.spinner("Fetching your purchases..."):
        response = requests.get(PURCHASE_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        if response.headers.get("Content-Type") == "application/json":
            error_detail = response.json().get("detail")
        else:
            error_detail = response.text
        st.error(f"Failed to fetch purchases: {error_detail}")

def refund_all_books(books):
    headers = get_headers()
    failed_refunds = []
    with st.spinner("Processing refunds..."):
        for book in books:
            refund_url = f"{PURCHASE_URL}/{book['id']}"
            res = requests.delete(refund_url, headers=headers)
            if res.status_code == 200:
                st.toast(f"{book['name']} refunded successfully!")
            else:
                failed_refunds.append(book)
    if failed_refunds:
        raise Exception(f"Failed to refund {len(failed_refunds)} books: {failed_refunds}")
    else:
        st.toast("All books refunded successfully!")

# DELETE ACCOUNT PAGE

def delete_account():
    headers = get_headers()
    with st.spinner("Deleting account, please do not exit"):
        purchases = fetch_purchases()
        if purchases:
            try:
                books = [item["book"] for item in purchases]
                refund_all_books(books)
            except Exception as e:
                st.error(f"Failed to refund books: {e}", icon="❌")
                st.error("Stopped the process, please refresh the page and try again")
                st.stop()
        del_response = requests.delete(f"{API_URL}/users/me", headers=headers)

    if del_response.status_code == 200:
        st.success("Deleted Account successfully, Redirecting to Login")
        st.session_state.role = None
        st.switch_page("app.py")
    else:
        if del_response.headers.get("Content-Type") == "application/json":
            error_detail = del_response.json().get("detail")
        else:
            error_detail = del_response.text
        st.error(f"Failed to delete account: {error_detail}", icon="❌")