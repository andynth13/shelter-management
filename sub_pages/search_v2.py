import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit.components.v1 import html

# Load shelter data
shelter_data = pd.read_csv('./data/complete_shelter_details_new.csv')

# Streamlit App
def search_page():
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

# Show the results in List View with expandable details
def show_list_view(results):
    st.subheader(f"Found {len(results)} shelters")
    
    for index, row in results.iterrows():
        # Display only shelter name and provider name initially
        shelter_name = row['Shelter Name']
        provider_name = row['Service Provider'] if 'Service Provider' in row else "Unknown Provider"
        
        # Expander to show details on click
        with st.expander(f"{shelter_name} (Provider: {provider_name}) Details +"):
            col1, col2 = st.columns([2, 1])
            
            # Left column: Full description and mini-map
            with col1:
                st.markdown(f"<h3><b>{shelter_name}</b></h3>", unsafe_allow_html=True)
                st.write(f"**Provider:** {provider_name}")
                st.write(f"**Description:** {row.get('ResultCard Description', 'No description available')}")

                # Generate a small Folium map for each shelter location
                latitude, longitude = row['Latitude'], row['Longitude']
                mini_map = folium.Map(location=[latitude, longitude], zoom_start=15, width=300, height=200)
                folium.Marker([latitude, longitude], popup=shelter_name).add_to(mini_map)
                
                # Render the map as HTML
                map_html = mini_map._repr_html_()
                st.components.v1.html(map_html, height=250)

                # URLs for Google Maps and Directions
                google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
                directions_url = row.get("Google Directions Link", "#")

                # Display the buttons side by side
                st.markdown(
                    f"""
                    <div style="display: flex; gap: 10px; margin-top: -10px;">
                        <a href="{google_maps_url}" target="_blank">
                            <button style="padding: 8px 16px; font-size: 16px;">View on Google Maps</button>
                        </a>
                        <a href="{directions_url}" target="_blank">
                            <button style="padding: 8px 16px; font-size: 16px;">Get Directions</button>
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Right column: Contact details (Website, Address, Phone, Email)
            with col2:
                st.markdown("### Website")
                st.write(f"[{row['Website']}]({row['Website']})")
                
                st.markdown("### Address")
                st.write(f"{row['Address']}")
                
                st.markdown("### Contact")
                st.write(f"Phone 1: {row['Phone 1']}")
                if pd.notna(row.get('Phone 2')):
                    st.write(f"Phone 2: {row['Phone 2']}")
                if pd.notna(row.get('Email')):
                    st.write(f"Email: {row['Email']}")
                
            st.markdown("---")

# Show the results in Map View
def show_map_view(results):
    st.subheader("Shelter Locations")
    
    # Set the initial map center to the first shelter location in the filtered results
    map_center = [results['Latitude'].iloc[0], results['Longitude'].iloc[0]]
    m = folium.Map(location=map_center, zoom_start=12)

    # Add shelter locations to the map with detailed popups
    for index, row in results.iterrows():
        shelter_name = row['Shelter Name']
        address = row['Address']
        website = row['Website']
        directions_link = row.get("Google Directions Link", "#")
        
        # Construct the popup content with links
        popup_content = (
            f"<b>{shelter_name}</b><br>{address}<br>"
            f"<a href='{website}' target='_blank'>Website</a><br>"
            f"<a href='{directions_link}' target='_blank'>Get Directions</a>"
        )
        
        # Add the marker with the customized popup
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_content, max_width=300)
        ).add_to(m)

    # Render the map as an HTML string
    map_html = m._repr_html_()
    
    # Display the map in Streamlit as an HTML component
    html(map_html, width=700, height=500)

