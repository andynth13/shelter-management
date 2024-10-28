import streamlit as st

# Display about us page
def display_about_us():
    st.title("About Us")
    st.write("Welcome to the Shelter Management System!")
    
    # Subsections for additional information
    st.header("About the Team")
    st.write("We are a dedicated team committed to improving shelter accessibility and management.")
    
    st.header("Contact Us")
    st.write("For more information, please contact us at: shelter-management@langara.ca")

