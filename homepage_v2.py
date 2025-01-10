import time
import streamlit as st
import hashlib
from dotenv import load_dotenv
from utils.db_functions import get_connection, fetch_shelters, login_user
from utils.custom_menu import streamlit_menu
# from sub_pages.manage_user import admin_page
from sub_pages.contact import display_about_us
from sub_pages.search_v2 import search_page
from sub_pages.manager import manager_page
from sub_pages.admin import admin_page
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit as st
import extra_streamlit_components as stx

# Initialize the CookieManager
def get_manager():
    return stx.CookieManager()
cookie_manager = get_manager()

# Set up session states
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.refresh_page = False
    # cookie_manager.set('is_logged_in', False, key= "4")



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
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_info = login_user(username, password)
        if user_info:

            st.session_state.is_logged_in = True
            st.session_state.role = user_info["role_name"]
            st.session_state.username = user_info["username"]

            cookie_manager.set('is_logged_in', True, key= "0")
            cookie_manager.set('username', user_info["username"], key= "1")
            cookie_manager.set('role', user_info["role_name"], key= "2")

            st.session_state.refresh_page = True  # Trigger a "refresh"
            st.success(f"Welcome, {user_info['username']}! You are logged in as {user_info['role_name']}.")
        else:
            st.error("Invalid username or password.")


    
def logout():
    # Clear cookies for session persistence
    st.session_state.is_logged_in = False
    st.session_state.role = None
    st.session_state.username = None

    print(f"before delete:{cookie_manager.get('is_logged_in')}")
    cookie_manager.delete('is_logged_in', key= "0")
    cookie_manager.delete('username',  key= "1")
    cookie_manager.delete('role', key="2")
    print(f"after delete:{cookie_manager.get('is_logged_in')}")

    st.session_state.refresh_page = True  # Reload the page to reset session

def manage_page():
    if st.session_state.role == "admin":
        admin_page()
    elif st.session_state.role == "manager":
        manager_page(st.session_state.username)

# Main navigation function
def main():
    
    # Check for refresh flag to simulate page reload
    # print(f"before reload:{cookie_manager.get('is_logged_in')}")
    if st.session_state.refresh_page:
        st.session_state.refresh_page = False
        st.rerun()
    
 
    st.title("Shelter Management")
    selected = streamlit_menu(option=2)
    
    if selected == "Home":
        time.sleep(0.3)
        search_page()
    if selected == "Manage":
        if st.session_state.is_logged_in:
            st.button("Logout", on_click=logout)
            manage_page()
        else:
            login_form()
    elif selected == "Contact":
        display_about_us()

    print(selected)
    print(f"after reload:{cookie_manager.get('is_logged_in')}")

# Run the app
if __name__ == "__main__":
    
    # Update session from cookies at the start of each session
    main()
    if cookie_manager.get('is_logged_in'):
        st.session_state.is_logged_in = True
        st.session_state.role = cookie_manager.get("role")
        st.session_state.username = cookie_manager.get("username")
    