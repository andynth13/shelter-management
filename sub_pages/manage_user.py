import streamlit as st
from utils.db_functions import create_user, get_connection, list_all_users
import pandas as pd



def admin_page():
    st.title("Admin Dashboard")

    # Section to create a new user
    st.header("Create New User")
    username = st.text_input("New Username")
    email = st.text_input("Email")
    password = st.text_input("New password", type="password")
    role_id = st.number_input("Role ID", min_value=1)

    if st.button("Create User"):
        if username and email and password and role_id:
            create_user(username, email, password, role_id)
        else:
            st.error("Please fill in all the fields.")

    st.divider()  # Add a horizontal line separator

    # Section to display all users
    st.header("List of Users")
    users_df = list_all_users()
    if not users_df.empty:
        st.dataframe(users_df)
    else:
        st.write("No users found or an error occurred.")
