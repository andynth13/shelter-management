import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
from utils.custom_menu import streamlit_menu

# Load shelter data
shelter_data = pd.read_csv('./data/complete_shelter_details_new.csv')

# Streamlit App
def search_page():
    
    st.title("Emergency Shelter Finder")

    # Search options
    search_option = st.radio("Search by:", ["Location", "Service Provider"], horizontal=True, key= '111')
    if search_option == "Location":
        search_input = st.text_input("Enter a location (e.g., New Westminster, Kamloops)")
    else:
        search_input = st.text_input("Enter a Service Provider (e.g., RainCity Housing)")

    # Choose view: List View or Map View
    view_option = st.radio("Choose View", ['List View', 'Map View'], key= '112')

    # Filter results based on search
    if st.button('Search'):
        results = filter_shelters(search_option, search_input)
        if len(results) > 0:
            if view_option == 'List View':
                show_list_view(results)
            elif view_option == 'Map View':
                show_map_view(results)
        else:
            st.write("No shelters found with the selected criteria.")

# Filter shelters based on location or service provider
def filter_shelters(search_option, search_input):
    filtered_data = shelter_data
    if search_option == "Location" and search_input:
        filtered_data = filtered_data[filtered_data['Address'].str.contains(search_input, case=False, na=False)]
    elif search_option == "Service Provider" and search_input:
        filtered_data = filtered_data[filtered_data['Service Provider'].str.contains(search_input, case=False, na=False)]
    return filtered_data

# Show the results in List View with toggle functionality
def show_list_view(results):
    st.subheader(f"Found {len(results)} shelters")
    
    for index, row in results.iterrows():
        # Check session state for the current shelter's expanded state
        is_expanded = st.session_state.get(f"expanded_{index}", False)

        # Create two columns: Left for main info, Right for contact details
        col1, col2 = st.columns([2, 1])

        with col1:
            # Display the shelter name and provider
            st.markdown(f"**{row['Shelter Name']}**")
            st.markdown(f"**Provided by:** {row['Service Provider']}")
            
            # Show short description when collapsed, full description when expanded
            if is_expanded:
                st.write(row['ResultCard Description Full'])
            else:
                st.write(row['ResultCard Description'])
            
            # Google Maps link
            st.markdown(f"[Open in Google Maps]({row['Google Directions Link']})")
            
            # Toggle button for expanding/collapsing
            if st.button("Less" if is_expanded else "More", key=f"toggle_{index}"):
                st.session_state[f"expanded_{index}"] = not is_expanded

        with col2:
            st.markdown("### Website")
            st.write(f"[{row['Website']}]({row['Website']})")
            
            st.markdown("### Address")
            st.write(row['Address'])

            # Contact details (only show in expanded mode)
            if is_expanded:
                st.markdown("### Contact")
                st.write(f"Phone 1: {row['Phone 1']}")
                if pd.notna(row['Phone 2']):
                    st.write(f"Phone 2: {row['Phone 2']}")
                if pd.notna(row['Email']):
                    st.write(f"Email: {row['Email']}")

        st.markdown("---")  # Divider between shelters

# Show the results in Map View
def show_map_view(results):
    st.subheader("Shelter Locations")
    
    # Center map at a general location (you can adjust this based on the first result or a default)
    map_center = [49.2827, -123.1207]  # Example center: Vancouver
    m = folium.Map(location=map_center, zoom_start=12)

    # Add shelter locations to the map
    for index, row in results.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"<b>{row['Shelter Name']}</b><br>{row['Address']}<br><a href='{row['Website']}'>Website</a>"
        ).add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=700)


