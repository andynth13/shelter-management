import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Load shelter data
shelter_data = pd.read_csv('./data/complete_shelter_details7f.csv')

# Streamlit App
def main():
    st.title("Emergency Shelter Finder")

    # Search by location
    location = st.text_input('Enter a location (e.g., New Westminster, Kamloops)')

    # Choose view: List View or Map View
    view_option = st.radio("Choose View", ['List View', 'Map View'])

    # Filter results based on search
    if st.button('Search'):
        results = filter_shelters(location)
        if len(results) > 0:
            if view_option == 'List View':
                show_list_view(results)
            elif view_option == 'Map View':
                show_map_view(results)
        else:
            st.write("No shelters found with the selected criteria.")

# Filter shelters based on location
def filter_shelters(location):
    filtered_data = shelter_data
    if location:
        filtered_data = filtered_data[filtered_data['Address'].str.contains(location, case=False, na=False)]
    return filtered_data

# Show the results in List View
def show_list_view(results):
    st.subheader(f"Found {len(results)} shelters")
    
    for index, row in results.iterrows():
        with st.expander(f"**{row['Shelter Name']}**", expanded=True):  # Expand each shelter's section
            # Create two columns: Left for description, Right for contact details
            col1, col2 = st.columns([2, 1])  # Left (description) is wider than right (contacts)
            
            # Left column: Description and Google Maps link
            with col1:
                st.markdown(f"<h3><b>{row['Shelter Name']}</b></h3>", unsafe_allow_html=True)  # Shelter name in bold, larger font
                st.write(f"**Description:** {row['ResultCard Description']}")
                st.markdown(f"[Open in Google Maps](https://www.google.com/maps/search/?api=1&query={row['Map Link']})")  # Only the map link
            
            # Right column: Contact details (Website, Address, Phone, Email)
            with col2:
                st.markdown("### Website")
                st.write(f"[{row['Website']}]({row['Website']})")
                
                st.markdown("### Address")
                st.write(f"{row['Address']}")
                
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
            location=[row['Latitude'], row['Longitude']],  # You can adjust these columns if needed
            popup=f"<b>{row['Shelter Name']}</b><br>{row['Address']}<br><a href='{row['Website']}'>Website</a>"
        ).add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=700)

if __name__ == "__main__":
    main()
