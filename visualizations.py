import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load your cleaned trekking dataset
data = pd.read_csv("cleaned.csv")

# Set up the Streamlit app
st.title("Trekking Data Visualization")

# Display the first few rows of the dataset
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.write(data)

# 1. Cost Distribution
st.subheader("Cost Distribution")
st.text("This histogram shows the distribution of trekking costs. The KDE line indicates the estimated probability density function.")
plt.figure(figsize=(10, 5))
sns.histplot(data['cost'], bins=30, kde=True)
st.pyplot(plt)

# 2. Trip Grade Count
st.subheader("Trip Grade Count")
st.text("This bar plot represents the count of treks for each trip grade, showing how many treks fall into each difficulty level.")
plt.figure(figsize=(10, 5))
sns.countplot(x='trip_grade', data=data)
st.pyplot(plt)

# 3. Max Altitude vs Cost
st.subheader("Max Altitude vs Cost")
st.text("This scatter plot illustrates the relationship between maximum altitude and cost of the treks. Each point represents a trek.")
plt.figure(figsize=(10, 5))
sns.scatterplot(x='max_altitude', y='cost', data=data)
st.pyplot(plt)

# 4. Average Cost per Trip Grade
st.subheader("Average Cost per Trip Grade")
st.text("This bar plot shows the average cost of treks for each trip grade. It provides insight into how trek difficulty impacts pricing.")
avg_cost_trip_grade = data.groupby('trip_grade')['cost'].mean().reset_index()
plt.figure(figsize=(10, 5))
sns.barplot(x='trip_grade', y='cost', data=avg_cost_trip_grade)
st.pyplot(plt)

# 5. Equipment Used Distribution (if applicable)
if 'equipment_used' in data.columns:
    st.subheader("Equipment Used Distribution")
    st.text("This horizontal bar plot shows the distribution of different equipment used for treks, indicating popular gear among trekkers.")
    plt.figure(figsize=(10, 5))
    sns.countplot(y='equipment_used', data=data)
    st.pyplot(plt)

# Show some additional statistics
st.subheader("Statistics")
st.write(data.describe())
