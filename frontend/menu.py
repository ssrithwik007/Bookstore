import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/home.py", label="Home")
    st.sidebar.page_link("app.py", label="Log out")
    if st.session_state.role in ["admin", "trail_admin"]:
        st.sidebar.page_link("pages/view_books.py", label="View books")
        st.sidebar.page_link("pages/add_books.py", label="Add books")
        st.sidebar.page_link("pages/get_users.py", label="View users", disabled=st.session_state.role != "admin")
        # st.sidebar.page_link("pages/update_books.py", label="Update books")
        # st.sidebar.page_link("pages/delete_books.py", label="Delete books")


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