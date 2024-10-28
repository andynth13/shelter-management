import streamlit as st
import psycopg2
import hashlib
from dotenv import load_dotenv
import os
import pandas as pd


# Database connection function
def get_connection():
    load_dotenv(override=True)
    return psycopg2.connect(
        host=os.environ['DATABASE_HOST'],
        port=os.environ['DATABASE_PORT'],
        database=os.environ['DATABASE_NAME'],
        user=os.environ['DATABASE_USER'],
        password=os.environ['DATABASE_PASSWORD']
    )


# Function to fetch shelter data with pagination
def fetch_shelters(page, items_per_page=20):
    conn = get_connection()
    cur = conn.cursor()
    offset = (page - 1) * items_per_page
    cur.execute("SELECT id, name, website, address, contact_email, contact_phone,total_beds, description_short FROM shelters ORDER BY id LIMIT %s OFFSET %s;", (items_per_page, offset))
    shelters = cur.fetchall()
    cur.close()
    conn.close()
    return pd.DataFrame(shelters, columns=["id", "Name", "website", "address", "contact_email","contact_phone","total_beds","description_short"])


#Login function
def login_user(username, password):
    conn = get_connection()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        with conn.cursor() as cur:
            query = """
                SELECT u.id, u.username, u.email, u.password_hash, r.role_name 
                FROM users u 
                INNER JOIN roles r ON r.id = u.role_id 
                WHERE u.username = %s;
            """
            cur.execute(query, (username,))
            user = cur.fetchone()

            if user and password_hash == user[3]:
                return {
                    "user_id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "role_name": user[4]
                }
            return None
    except Exception as e:
        st.error(f"Login error: {e}")
    finally:
        conn.close()