#!/usr/bin/env python
# coding: utf-8

# In[20]:


# pip install streamlit-folium


# In[19]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import folium
import streamlit as st
from folium import plugins
from folium import IFrame




# In[3]:


import requests
import pandas as pd

# Define the API URL
api_url = "https://api.openchargemap.io/v3/poi/"

# Define parameters for the API request with a large maxresults value
params = {
    'output': 'json',
    'countrycode': 'NL',
    'maxresults': 10000,  # Set a large number
    'compact': 'true',
    'verbose': 'false',
    'key': '49603f59-44ce-4ddf-91b2-7d06f4e9c937'
}

# Make the API request
response = requests.get(api_url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data from the response
    data = response.json()

    # Convert to a DataFrame
    openchargemap = pd.json_normalize(data)

    # Display the DataFrame
    print(openchargemap.head())

else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code}")
    print(response.text)


# In[4]:


print(openchargemap.shape)
print(openchargemap.columns)


# In[5]:


print(openchargemap[['AddressInfo.Latitude', 'AddressInfo.Longitude', 'UsageCost']].isna().sum())


# In[6]:


import folium
from folium import plugins

# Assuming openchargemap is your DataFrame
# Convert relevant columns to numeric types and fill NaN values
openchargemap[['AddressInfo.Latitude', 'AddressInfo.Longitude', 'UsageCost']] = openchargemap[['AddressInfo.Latitude', 'AddressInfo.Longitude', 'UsageCost']].apply(pd.to_numeric, errors='coerce')
openchargemap[['AddressInfo.Latitude', 'AddressInfo.Longitude', 'UsageCost']] = openchargemap[['AddressInfo.Latitude', 'AddressInfo.Longitude', 'UsageCost']].fillna(0)

# Create a folium map centered around the Netherlands
map_center = [52.1326, 5.2913]  # Latitude and Longitude for the center of the Netherlands
charging_map = folium.Map(location=map_center, zoom_start=7)

# Create TileLayer for CartoDB Positron
carto_layer = folium.TileLayer('cartodbpositron', name='CartoDB Positron', control=False)
carto_layer.add_to(charging_map)

# Create a MarkerCluster
marker_cluster = plugins.MarkerCluster().add_to(charging_map)

# Add CircleMarkers for each charging point to the MarkerCluster
for _, row in openchargemap.iterrows():
    lat = row['AddressInfo.Latitude']
    lon = row['AddressInfo.Longitude']
    cost = row['UsageCost']
    address_id = row['AddressInfo.ID']
    address_title = row['AddressInfo.Title']
    
    # Set color based on charging cost
    color = 'blue' if cost <= 0.2 else 'cyan' if cost <= 0.4 else 'lime' if cost <= 0.6 else 'yellow' if cost <= 0.8 else 'red'
    
    # Customize popup content
    popup_content = f"ID: {address_id}<br>Title: {address_title}<br>Cost: {'unknown' if cost == 0 else cost}"
    
    # Add CircleMarker to the MarkerCluster
    folium.CircleMarker(location=[lat, lon], radius=5, color=color, fill=True, fill_color=color, fill_opacity=0.7, popup=popup_content).add_to(marker_cluster)

# Show CartoDB Positron by default
carto_layer.layer_name = 'CartoDB Positron'
charging_map.add_child(carto_layer)

# Add LayerControl to enable switching between map layers
folium.LayerControl().add_to(charging_map)

# # Save the map as an HTML file (optional)
# charging_map.save("charging_map_default_cartodbpositron.html")

# Display the map in Jupyter Notebook
charging_map


# In[7]:


unique_country_codes = openchargemap['AddressInfo.CountryID'].unique()
print(unique_country_codes)


# In[8]:


import re

# Extract numerical values from the 'AddressInfo.Postcode' column
numeric_postcodes = openchargemap['AddressInfo.Postcode'].apply(lambda x: re.findall(r'\d+', str(x)))

# Flatten the list of lists into a single list
numeric_postcodes = [int(num) for sublist in numeric_postcodes for num in sublist if num]

# Find the range
postcode_range = (min(numeric_postcodes), max(numeric_postcodes))

# Print the range
print(f"Numerical range of values in 'AddressInfo.Postcode': {postcode_range}")


# In[9]:


import matplotlib.pyplot as plt
import re

# Extract numerical values from the 'AddressInfo.Postcode' column
numeric_postcodes = openchargemap['AddressInfo.Postcode'].apply(lambda x: re.findall(r'\d+', str(x)))

# Flatten the list of lists into a single list and convert to integers
numeric_postcodes = [int(num) for sublist in numeric_postcodes for num in sublist if num]

# Create a boxplot
plt.figure(figsize=(10, 6))
plt.boxplot(numeric_postcodes, vert=False)
plt.xlabel('Numerical Values in Postcode')
plt.title('Boxplot of Numerical Values in Postcode')
plt.show()


# In[10]:


# Find the row where the 'AddressInfo.Postcode' is equal to 75389
row_with_postcode_75389 = openchargemap[openchargemap['AddressInfo.Postcode'] == '75389']

# Extract the title from the corresponding row
title_of_postcode_75389 = row_with_postcode_75389['AddressInfo.Title'].values[0]

# Print the title
print(f"The title corresponding to the postal code 75389 is: {title_of_postcode_75389}")


# In[11]:


# Drop the row where 'AddressInfo.Postcode' is equal to 75389
openchargemap = openchargemap[openchargemap['AddressInfo.Postcode'] != '75389']

# Reset the index after dropping the row
openchargemap.reset_index(drop=True, inplace=True)

# Check the modified DataFrame
print(openchargemap.shape)  # To verify the number of rows after dropping


# In[12]:


import matplotlib.pyplot as plt
import re

# Extract numerical values from the 'AddressInfo.Postcode' column
numeric_postcodes = openchargemap['AddressInfo.Postcode'].apply(lambda x: re.findall(r'\d+', str(x)))

# Flatten the list of lists into a single list and convert to integers
numeric_postcodes = [int(num) for sublist in numeric_postcodes for num in sublist if num]

# Create a boxplot
plt.figure(figsize=(10, 6))
plt.boxplot(numeric_postcodes, vert=False)
plt.xlabel('Numerical Values in Postcode')
plt.title('Boxplot of Numerical Values in Postcode')
plt.show()


# In[13]:


import re

# Extract numerical values from the 'AddressInfo.Postcode' column
numeric_postcodes = openchargemap['AddressInfo.Postcode'].apply(lambda x: re.findall(r'\d+', str(x)))

# Flatten the list of lists into a single list
numeric_postcodes = [int(num) for sublist in numeric_postcodes for num in sublist if num]

# Find the range
postcode_range = (min(numeric_postcodes), max(numeric_postcodes))

# Print the range
print(f"Numerical range of values in 'AddressInfo.Postcode': {postcode_range}")


# In[14]:


# Count of NaN and non-NaN values in 'AccessComments' column
access_comments_counts = openchargemap['AddressInfo.AccessComments'].isna().value_counts()

# Display the counts
print(access_comments_counts)


# In[17]:


import folium
from folium import plugins
from folium import IFrame
import pandas as pd

# Assuming openchargemap is your DataFrame
# Convert relevant columns to numeric types and fill NaN values
openchargemap[['AddressInfo.Latitude', 'AddressInfo.Longitude', 'UsageCost']] = openchargemap[['AddressInfo.Latitude', 'AddressInfo.Longitude', 'UsageCost']].apply(pd.to_numeric, errors='coerce')
openchargemap[['AddressInfo.Latitude', 'AddressInfo.Longitude', 'UsageCost']] = openchargemap[['AddressInfo.Latitude', 'AddressInfo.Longitude', 'UsageCost']].fillna(0)

# Create a folium map centered around the Netherlands
map_center = [52.1326, 5.2913]  # Latitude and Longitude for the center of the Netherlands
charging_map = folium.Map(location=map_center, zoom_start=7)

# Add TileLayer for CartoDB Positron as the default layer
folium.TileLayer('cartodbpositron', name='CartoDB Positron').add_to(charging_map)

# Use MarkerCluster to prevent overlapping markers
marker_cluster = plugins.MarkerCluster().add_to(charging_map)

# Add CircleMarkers for each charging point
for _, row in openchargemap.iterrows():
    lat = row['AddressInfo.Latitude']
    lon = row['AddressInfo.Longitude']
    cost = row['UsageCost']
    address_id = row['AddressInfo.ID']
    address_title = row['AddressInfo.Title']
    access_comments = row['AddressInfo.AccessComments']
    num_points = row['NumberOfPoints']
    status_type = row['StatusTypeID']
    last_status_update_time = pd.to_datetime(row['DateLastStatusUpdate']).strftime('%B %d, %Y, %H:%M:%S %Z')
    
    # Set color based on charging cost
    color = 'blue' if cost <= 0.2 else 'cyan' if cost <= 0.4 else 'lime' if cost <= 0.6 else 'yellow' if cost <= 0.8 else 'red'
    
    # Customize popup content without images
    popup_content = (
        f"<b>ID:</b> {address_id}<br>"
        f"<b>Title:</b> {address_title}<br>"
        f"<b>Access Comments:</b> {access_comments if pd.notna(access_comments) else 'No additional info'}<br>"
        f"<b>Latitude:</b> {lat}<br>"
        f"<b>Longitude:</b> {lon}<br>"
        f"<b>Cost:</b> {cost}<br>"
        f"<b>Number of Points:</b> {num_points}<br>"
        f"<b>Status Type:</b> {status_type}<br>"
        f"<b>Last Status Update Time:</b> {last_status_update_time}<br>"
    )
    
    # Add CircleMarker to the MarkerCluster
    folium.CircleMarker(location=[lat, lon], radius=5, color=color, fill=True, fill_color=color, fill_opacity=0.7, popup=folium.Popup(IFrame(popup_content, width=300, height=200))).add_to(marker_cluster)

# Add LayerControl to enable switching between map layers
folium.LayerControl().add_to(charging_map)

# Display the map in Jupyter Notebook
charging_map

st_folium(charging_map)


# In[ ]:




