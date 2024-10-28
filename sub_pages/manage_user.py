import streamlit as st
import hashlib
from dotenv import load_dotenv
from utils.db_functions import get_connection
import pandas as pd

def create_user(username, email, password, role_id):
    # Hash the password before storing it (simple example using SHA-256)
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Connect to the database
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Insert a new user directly into the users table
        cur.execute("""
            INSERT INTO users (username, email, password_hash, role_id, created_at)
            VALUES (%s, %s, %s, %s, NOW());
        """, (username, email, password_hash, role_id))
        
        conn.commit()
        st.success(f"User '{username}' created successfully!")
    except Exception as e:
        conn.rollback()
        st.error(f"Failed to create user: {e}")
    finally:
        cur.close()
        conn.close()

def list_all_users():
    # Connect to the database
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Query all users directly from the users table
        cur.execute("""
            SELECT u.id, u.username, u.email, r.role_name, created_at 
            FROM users u
            INNER JOIN roles r
            ON u.role_id = r.id
            ORDER BY u.id;
        """)
        users = cur.fetchall()

        # Create a DataFrame to display the users
        df = pd.DataFrame(users, columns=["ID", "Username", "Email", "Role", "Created At"])
        return df

    except Exception as e:
        st.error(f"Failed to retrieve users: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if there's an error
    finally:
        cur.close()
        conn.close()

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
