import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("app_pages/home.py", label="Home")
    if st.session_state.role in ["admin", "trail_admin"]:
        st.sidebar.divider()
        st.sidebar.page_link("app_pages/view_books.py", label="View books")
        st.sidebar.page_link("app_pages/add_books.py", label="Add books")
        st.sidebar.page_link("app_pages/update_books.py", label="Update books")
        st.sidebar.page_link("app_pages/delete_books.py", label="Delete books")
        st.sidebar.divider()        
        st.sidebar.page_link("app_pages/get_users.py", label="View users", disabled=st.session_state.role != "admin", help="Only admins can view users")

    if st.session_state.role == "user":
        st.sidebar.divider()
        st.sidebar.page_link("app_pages/browse.py", label="Browse Books")
        st.sidebar.page_link("app_pages/view_cart.py", label="View Cart")
        st.sidebar.page_link("app_pages/purchase.py", label="View Purchases")

    if st.session_state.role in ["trail_admin", "user"]:
        st.sidebar.divider()
        st.sidebar.page_link("app_pages/update_account.py", label="Update Credentials")
        st.sidebar.page_link("app_pages/delete_account.py", label="Delete Account")
        st.sidebar.divider()

    st.sidebar.page_link("app.py", label="Log out")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()