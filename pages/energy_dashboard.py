import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set the path to the CSV file (relative path from /pages directory)
csv_file_path = os.path.join(os.path.dirname(__file__), '../data/history_day.csv')

# Load the CSV file
@st.cache_data
def load_data(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Convert the 'Last Changed' column to datetime format
    df['last_changed'] = pd.to_datetime(df['last_changed'])

    return df

# Load data from the CSV
data = load_data(csv_file_path)

# Show the dataframe to check
st.write(data)

# Plot the data using matplotlib
fig, ax = plt.subplots(figsize=(10, 6))

# Plot solar energy vs. time (Last Changed)
ax.plot(data['last_changed'], data['state'], marker='o', color='tab:purple')

# Label the plot
ax.set_xlabel('Time')
ax.set_ylabel('Solar Energy (kW)')
ax.set_title('Solar Energy Generation Over Time')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show the plot in Streamlit
st.pyplot(fig)



# Set the title of the page
st.title("Solar Energy Dashboard")

# Add a brief description
st.write("""Explore solar energy generation trends and track performance over time.""")

# Display images from the 'images' folder
st.image("images/day.png", caption="Generated energy of last day", use_column_width=True)
st.image("images/week.png", caption="Generated energy of last week", use_column_width=True)
st.image("images/month.png", caption="Generated energy of last month", use_column_width=True)
