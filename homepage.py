import streamlit as st
import hashlib
from dotenv import load_dotenv
from utils.db_functions import get_connection, fetch_shelters, login_user
from utils.custom_menu import streamlit_menu
from sub_pages.manage_user import admin_page
from sub_pages.contact import display_about_us
import pandas as pd
import streamlit as st
import streamlit_cookies_manager




if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
    st.session_state.role = None


# Display shelters with pagination
def display_shelters():
    st.title("All Shelters")
    st.write("Public users can search for shelters without logging in.")
    
    page = st.number_input("Page", min_value=1, value=1)
    shelters_df = fetch_shelters(page)
    
    if not shelters_df.empty:
        st.write(shelters_df)
    else:
        st.write("No shelters found.")


# Display login form and set session state for user roles
def login_form():
        # Display login form if not logged in
    placeholder = st.empty()
    placeholder.title("Login")
    
    
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials:")
        username  = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        user_info = login_user(username, password)
        if user_info:
            st.session_state.is_logged_in = True
            st.session_state["username"] = user_info["username"]
            st.session_state["role"] = user_info["role_name"]



            placeholder.empty()
            st.success(f"Welcome, {user_info['username']}! You are logged in as {user_info['role_name']}.")
        else:
            st.error("Invalid username or password.")

    if "username" in st.session_state:
        # Role-based content after login
        print(st.session_state["username"])
        if st.session_state["role"] == "admin":
            admin_page()
        elif st.session_state["role"] == "manager":
            st.write("Manager can view and edit shelters assigned to them.")
        else:
            pass
        return 
    
def logout():
    st.session_state.is_logged_in = False
    st.session_state.username = None
    st.session_state.role = None


# Main navigation function
def main():
    st.title("Shelter Management")
    selected = streamlit_menu(option=3)
    if st.session_state.is_logged_in:
        st.sidebar.button("Logout", on_click=logout)

    if selected == "Home":
        display_shelters()
    if selected == "Manage":
        if st.session_state.is_logged_in:
           admin_page()
        else:
            login_form()
    if selected == "Contact":
        display_about_us()
    

# Run the app
if __name__ == "__main__":
    # Initialize session state
    if "role" not in st.session_state:
        st.session_state.role = "public"
    main()
