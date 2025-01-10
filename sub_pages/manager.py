import streamlit as st
import psycopg2
import pandas as pd
from utils.db_functions import create_user, get_connection, list_all_users




def manager_page(username):
    st.title("Shelter Manager Interface")

    role_map = {
        1: "Admin",
        2: "Manager",
        # Add more roles as needed in the future
    }

    conn = get_connection()
    if conn is None:
        return

    mycursor = conn.cursor()

    try:
        # Fetch role_id from users table for the given user_id
        mycursor.execute("SELECT role_id FROM users WHERE username = %s", (username,))
        user_info = mycursor.fetchone()

        if user_info:
            role_id = user_info[0]
            role = role_map.get(role_id, f"Role ID {role_id} (Unknown Role)")
            st.write(f"Role for User - {username}: {role}")

            # Fetch shelter_id associated with this user_id from shelter_managers table
            mycursor.execute("SELECT sm.shelter_id FROM shelter_managers sm inner join  users u on sm.user_id = u.id WHERE u.username = %s", (username,))
            shelter_id_result = mycursor.fetchone()

            if shelter_id_result:
                shelter_id = shelter_id_result[0]
                st.write(f"Shelter ID associated with User: {username}: {shelter_id}")

                # Fetch shelter details from shelters table
                mycursor.execute("SELECT * FROM shelters WHERE id = %s", (shelter_id,))
                shelter_info = mycursor.fetchone()

                # Fetch total_beds from beds_availability table
                mycursor.execute("SELECT available_beds FROM beds_availability WHERE shelter_id = %s", (shelter_id,))
                beds_info = mycursor.fetchone()
                available_beds = beds_info[0] if beds_info else "Not Available"

                # Display shelter information if found
                if shelter_info:
                    # Define column headers based on the structure of the shelters table
                    columns = ['Shelter ID', 'Shelter name', 'Provider', 'Website', 'Address',
                       'Mailing address', 'Email', 'Phone', 'Manager phone', 'Fax', 'Total beds', 'Description short',
                       'Description full', 'Created at']

                    # Convert the fetched shelter data to a DataFrame for display
                    shelter_df = pd.DataFrame([shelter_info], columns=columns)
                    st.subheader("My Shelter Information")
                    st.write(shelter_df)

                    # Display total beds
                    st.write(f"Total Beds Available: {available_beds}")

                else:
                    st.warning("No shelter details found for this shelter ID.")
            else:
                st.warning("No shelter assigned to this User ID.")
        else:
            st.warning("No user information found for this User ID.")

    except Exception as e:
        st.error(f"Error fetching shelter information: {e}")

    finally:
        mycursor.close()
        conn.close()

