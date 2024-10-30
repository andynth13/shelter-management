import streamlit as st
import psycopg2
import pandas as pd
from utils.custom_menu import streamlit_menu
from utils.db_functions import create_user, get_connection, list_all_users


def admin_page():
    st.title("Admin Page of Emergency Shelter")

    # Create connection to the database
    conn = get_connection()
    
    if conn is None:
        st.error("Unable to connect to the database.")
        return
    
    mycursor = conn.cursor()

    # Display Options for CRUD Operations
    option = streamlit_menu(option = 10)

    # Perform Selected CRUD Operations
    if option == "Create":
        st.subheader("Assign a Shelter Manager")
        user_id = st.number_input("Enter User ID", min_value=1)
        shelter_id = st.number_input("Enter Shelter ID", min_value=1)

        if st.button("Assign Manager"):
            try:
                sql = "INSERT INTO shelter_managers (user_id, shelter_id) VALUES (%s, %s)"
                val = (user_id, shelter_id)
                mycursor.execute(sql, val)
                conn.commit()
                st.success("Shelter Manager Assigned Successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
                conn.rollback()

        st.subheader("Current Shelter Managers list")
        try:
            # SQL query to fetch shelters list
            sql = """
                SELECT sm.user_id, sm.shelter_id, sm.assigned_at
                FROM shelter_managers sm
            """
            mycursor.execute(sql)
            result = mycursor.fetchall()

            # Define column headers for the result
            columns = ['User ID', 'Shelter ID', 'Assigned at']
            shelters_manager_df = pd.DataFrame(result, columns=columns)

            # Display the data as a table in Streamlit
            st.dataframe(shelters_manager_df)

        except Exception as e:
            st.error(f"Error fetching shelter-manager assignments: {e}")
        
        st.subheader("Current Shelters list")
        try:
            # SQL query to fetch shelters list
            sql = """
                SELECT *
                FROM shelters s
            """
            mycursor.execute(sql)
            result = mycursor.fetchall()

            # Define column headers for the result
            columns = ['Shelter ID', 'Shelter name', 'Provider', 'Website', 'Address',
                       'Mailing address', 'Email', 'Phone', 'Manager phone', 'Fax', 'Total beds', 'Description short',
                       'Description full', 'Created at']
            shelters_df = pd.DataFrame(result, columns=columns)

            # Display the data as a table in Streamlit
            st.write(shelters_df)

        except Exception as e:
            st.error(f"Error fetching shelter-manager assignments: {e}")

    elif option == "Read":
        st.subheader("View Shelter Managers and Associated Shelters")
        try:
            # SQL JOIN query to fetch data from shelter_managers and shelters tables
            sql = """
                SELECT sm.shelter_id, sm.user_id, 
                    s.name, s.address, s.contact_phone_manager, s.website, s.mailing_address
                FROM shelter_managers sm
                JOIN shelters s ON sm.shelter_id = s.id
            """
            mycursor.execute(sql)
            result = mycursor.fetchall()

            # Define column headers based on the result of the join
            columns = ['Shelter ID', 'User ID', 'Shelter Name', 'Shelter Address', 'Manager phone', 'Website','Mailing address']
            managers_df = pd.DataFrame(result, columns=columns)

            # Display the joined data as a table in Streamlit
            st.write(managers_df)

        except Exception as e:
            st.error(f"Error fetching data: {e}")


    elif option == "Update":
        st.subheader("Update Shelter Manager Assignment")
        user_id = st.number_input("Enter User ID", min_value=1)
        new_shelter_id = st.number_input("Enter New Shelter ID", min_value=1)

        if st.button("Update Assignment"):
            try:
                sql = "UPDATE shelter_managers SET shelter_id = %s WHERE user_id = %s"
                val = (new_shelter_id, user_id)
                mycursor.execute(sql, val)
                conn.commit()
                st.success("Shelter Manager's Assignment Updated Successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
                conn.rollback()

        # Displaying the list of shelters and their respective managers
        st.subheader("View Shelter Managers and Associated Shelters")
        try:
            # SQL JOIN query to fetch data from shelter_managers and shelters tables
            sql = """
                SELECT sm.shelter_id, sm.user_id, 
                    s.name, s.address, s.contact_phone_manager, s.website, s.mailing_address
                FROM shelter_managers sm
                JOIN shelters s ON sm.shelter_id = s.id
            """
            mycursor.execute(sql)
            result = mycursor.fetchall()

            # Define column headers based on the result of the join
            columns = ['Shelter ID', 'User ID', 'Shelter Name', 'Shelter Address', 'Manager phone', 'Website','Mailing address']
            managers_df = pd.DataFrame(result, columns=columns)

            # Display the joined data as a table in Streamlit
            st.write(managers_df)

        except Exception as e:
            st.error(f"Error fetching data: {e}")





        st.subheader("Update Shelter and Bed Availability")

        # User input for selecting the shelter to update
        shelter_id = st.number_input("Enter Shelter ID", min_value=1)

        # Dropdown to select which table and field to update
        table_option = st.selectbox("Select Table to Update", ["shelters", "beds_availability"])
        
        # Dictionary of fields for each table
        fields = {
            "shelters": ['Shelter ID', 'Shelter name', 'Provider', 'Website', 'Address',
                       'Mailing address', 'Email', 'Phone', 'Manager phone', 'Fax', 'Total beds', 'Description short',
                       'Description full', 'Created at'],
            'beds_availability': ["available_beds", "last_updated"]
        }
        
        # Select field to update based on chosen table
        field_to_update = st.selectbox("Select Field to Update", fields[table_option])
        new_value = st.text_input(f"Enter New Value for {field_to_update}")

        # Button to perform update
        if st.button("Update"):
            try:
                # Construct SQL update statement based on user selection
                if table_option == "shelters":
                    sql = f"UPDATE shelters SET {field_to_update} = %s WHERE shelter_id = %s"
                    val = (new_value, shelter_id)
                elif table_option == "beds_availability":
                    sql = f"UPDATE beds_availability SET {field_to_update} = %s WHERE shelter_id = %s"
                    val = (new_value, shelter_id)
                
                # Execute the update
                mycursor.execute(sql, val)
                conn.commit()
                st.success(f"{field_to_update} updated successfully in {table_option} table!")
            
            except Exception as e:
                st.error(f"Error: {e}")
                conn.rollback()

    elif option == "Delete":
        delete_option = st.selectbox("Select What to Delete", ("Shelter Manager", "Shelter"))

        if delete_option == "Shelter Manager":
            st.subheader("Delete Shelter Manager")
            user_id = st.number_input("Enter User ID of Manager to Delete", min_value=1)

            if st.button("Delete Manager"):
                # Show confirmation message
                st.warning("Are you sure you want to delete this manager? This action cannot be undone.")
                
                # Display a confirm delete button
                confirm_delete = st.button("Confirm Delete")
                
                # If confirm delete button is pressed, proceed with deletion
                if confirm_delete:
                    try:
                        sql = "DELETE FROM shelter_managers WHERE user_id = %s"
                        val = (user_id,)
                        mycursor.execute(sql, val)
                        conn.commit()
                        st.success("Shelter Manager Deleted Successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                        conn.rollback()

        elif delete_option == "Shelter":
            st.subheader("Delete Shelter")
            shelter_id = st.number_input("Enter Shelter ID to Delete", min_value=1)

            if st.button("Delete Shelter"):
                # Show confirmation message
                st.warning("Are you sure you want to delete this shelter? This action cannot be undone.")
                
                # Display a confirm delete button
                confirm_delete = st.button("Confirm Delete Shelter")
                
                # If confirm delete button is pressed, proceed with deletion
                if confirm_delete:
                    try:
                        sql = "DELETE FROM shelters WHERE shelter_id = %s"
                        val = (shelter_id,)
                        mycursor.execute(sql, val)
                        conn.commit()
                        st.success("Shelter Deleted Successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                        conn.rollback()
                
        # Displaying the list of shelters and their respective managers
        st.subheader("Current Shelter and Manager Assignments")
        try:
            # SQL query to fetch shelters and their assigned managers
            sql = """
                SELECT sm.user_id, sm.assigned_at,
                    s.name, s.address
                FROM shelter_managers sm
                JOIN shelters s ON sm.shelter_id = s.id
            """
            mycursor.execute(sql)
            result = mycursor.fetchall()

            # Define column headers for the result
            columns = ['User ID', 'Assigned At', 'Shelter Name', 'Shelter Address']
            shelter_manager_df = pd.DataFrame(result, columns=columns)

            # Display the data as a table in Streamlit
            st.write(shelter_manager_df)

        except Exception as e:
            st.error(f"Error fetching shelter-manager assignments: {e}")

    # Close the connection and cursor after use
    mycursor.close()
    conn.close()
