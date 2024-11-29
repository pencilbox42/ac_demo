import streamlit as st
import folium
from folium import CircleMarker
from streamlit_folium import st_folium

# Coordinates for the five cities
cities = {
    'Berlin': [52.5200, 13.4050],
    'Munich': [48.1351, 11.5820],
    'Hamburg': [53.5511, 9.9937],
    'Frankfurt': [50.1109, 8.6821],
    'Stuttgart': [48.7758, 9.1829]
}

# Create a map centered in Germany (around the country center)
map_center = [51.1657, 10.4515]  # Latitude and longitude of Germany
m = folium.Map(location=map_center, zoom_start=6, control_scale=True)

# Add red solid circles for each city
for city, coords in cities.items():
    folium.CircleMarker(
        location=coords,  # Coordinates for the city
        radius=40,  # Radius of the circle
        color='red',  # Border color
        fill=True,  # Fill the circle
        fill_color='red',  # Fill color
        fill_opacity=0.5,  # Transparency level
        popup=city  # Show city name when clicked
    ).add_to(m)

# Display the map in the Streamlit app using folium
st.title("Balancing Energy Supply and Demand")

# Embed the folium map into Streamlit
st_folium(m, width=725)

#################################

# Initialize session state to store energy demand and supply
if 'energy_demand' not in st.session_state:
    st.session_state.energy_demand = 50  # default value
if 'energy_supply' not in st.session_state:
    st.session_state.energy_supply = st.session_state.energy_demand + 3  # supply is 3 more than demand

# Define the energy demand slider (0-100)
energy_demand = st.slider(
    "Energy Demand (%)", 0, 100, st.session_state.energy_demand, 1, help="Adjust the energy demand level"
)

# Ensure energy supply is always 3 more than energy demand, and set max value to 100
energy_supply = st.slider(
    "Energy Supply (%)", 
    0,  # minimum value is energy demand
    100,  # max value is 100
    energy_demand + 3,  # default value is energy demand + 3
    1,  # step size of the slider
    help="Energy supply is always 3% more than energy demand"
)

# Ensure the energy supply value is always 3 more than the energy demand value
if energy_supply != energy_demand + 3:
    st.session_state.energy_supply = energy_demand + 3
else:
    st.session_state.energy_supply = energy_supply

# Update energy demand in session state
st.session_state.energy_demand = energy_demand

# Display the values
st.write(f"### Energy Demand: {energy_demand}%")
st.write(f"### Energy Supply: {st.session_state.energy_supply}%")

# Color the energy demand value (light red) and supply value (light green)
st.markdown(f'<div style="background-color: lightcoral; padding: 10px; color: white;">Energy Demand: {energy_demand}%</div>', unsafe_allow_html=True)
st.markdown(f'<div style="background-color: lightgreen; padding: 10px; color: black;">Energy Supply: {st.session_state.energy_supply}%</div>', unsafe_allow_html=True)
