import pandas as pd
import streamlit as st

# Importing data from Excel
df = pd.read_excel("rawdata.xlsx")

# Filtering data for 'inside' positions
df1 = df[df['position'] == 'inside']
df1['time_hour'] = pd.to_datetime(df1['time'], format='%H:%M:%S').dt.hour
df1['time_minute'] = pd.to_datetime(df1['time'], format='%H:%M:%S').dt.minute
df1["total_time"] = df1['time_hour'] * 60 + df1['time_minute']  # Calculate total time in minutes
inside_datewise_duration_in_minutes = df1.groupby('date')['total_time'].mean()

# Filtering data for 'outside' positions
df2 = df[df['position'] == 'outside']
df2['time_hour'] = pd.to_datetime(df2['time'], format='%H:%M:%S').dt.hour
df2['time_minute'] = pd.to_datetime(df2['time'], format='%H:%M:%S').dt.minute
df2["total_time"] = df2['time_hour'] * 60 + df2['time_minute']  # Calculate total time in minutes
outside_datewise_duration_in_minutes = df2.groupby('date')['total_time'].mean()

# Count of activities
activity_counts = df['activity'].value_counts()

# Filtering data for 'placed' activities
df_placed = df[df['activity'] == 'placed']
placed_count = df_placed.groupby('date')['activity'].count()

# Filtering data for 'picked' activities
df_picked = df[df['activity'] == 'picked']
picked_count = df_picked.groupby('date')['activity'].count()

# Streamlit app interface
st.title("Activity Dashboard")

# Display the loaded DataFrame for debugging
st.write("Loaded DataFrame:")
st.write(df.head())

# Display inside datewise duration in minutes
st.header('Inside Datewise Duration in Minutes')
st.dataframe(inside_datewise_duration_in_minutes)

# Display outside datewise duration in minutes
st.header('Outside Datewise Duration in Minutes')
st.dataframe(outside_datewise_duration_in_minutes)

# Display placed count
st.header('Placed Count')
st.dataframe(placed_count)

# Display picked count
st.header('Picked Count')
st.dataframe(picked_count)
