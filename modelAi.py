import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

# Load your cleaned trekking dataset
data = pd.read_csv("cleaned.csv")

# Handle missing values (NaN) by filling numerical columns with the median and categorical columns with 'Unknown'
data['cost'].fillna(data['cost'].median(), inplace=True)
data['max_altitude'].fillna(data['max_altitude'].median(), inplace=True)
data['trip_grade'].fillna('Unknown', inplace=True)
data['fitness_level'].fillna('Unknown', inplace=True)

# Preprocessing: Select relevant features for recommendations (including trip_grade, fitness_level as categorical)
features = ['cost', 'trip_grade', 'fitness_level', 'max_altitude']

# One-Hot Encode categorical columns (trip_grade, fitness_level)
encoder = OneHotEncoder(sparse_output=False)  # Updated from sparse=False to sparse_output=False
encoded_cats = encoder.fit_transform(data[['trip_grade', 'fitness_level']])

# Concatenate the encoded categorical columns with the numerical columns
data_for_similarity = pd.concat(
    [data[['cost', 'max_altitude']].reset_index(drop=True), 
     pd.DataFrame(encoded_cats, columns=encoder.get_feature_names_out())], 
    axis=1
)

# Normalize the data for better comparison (only for numerical columns)
scaler = StandardScaler()
normalized_data = scaler.fit_transform(data_for_similarity)

# Cosine similarity calculation for trek recommendations
similarity_matrix = cosine_similarity(normalized_data)

# Set up the Streamlit app
st.title("AI Trekking Guide - Find Treks & Get Recommendations")

# Ask for user input: Budget, trip grade, fitness level
budget = st.number_input("Enter your budget (in USD):", min_value=0, step=100)
trip_grade = st.selectbox("Select Trip Grade:", data['trip_grade'].unique())
fitness_level = st.selectbox("Select Fitness Level:", data['fitness_level'].unique())

# Filter the treks based on the user input
filtered_data = data[(data['cost'] <= budget) & 
                     (data['trip_grade'] == trip_grade) &
                     (data['fitness_level'] == fitness_level)]

# Display the filtered treks when user clicks 'Search'
if st.button("Search"):
    if not filtered_data.empty:
        st.write(f"Treks within your budget of ${budget}, with {trip_grade} trip grade and {fitness_level} fitness level:")
        # Show the relevant trek columns for the user
        st.write(filtered_data[['trek', 'cost', 'time', 'trip_grade', 'fitness_level', 'max_altitude', 'trekking_group_size', 'equipment_used', 'review/satisfaction']])
        
        # Recommend similar treks based on user's first selected trek
        st.write("Recommended Treks for You:")
        # Get the index of the first trek from the filtered data
        first_trek_idx = filtered_data.index[0]
        # Find similar treks
        similar_indices = similarity_matrix[first_trek_idx].argsort()[::-1][1:6]  # Top 5 similar treks
        recommended_treks = data.iloc[similar_indices]

        st.write(recommended_treks[['trek', 'cost', 'time', 'trip_grade', 'fitness_level', 'max_altitude', 'trekking_group_size', 'eqiptment_used', 'review/satisfaction']])
    else:
        st.write("Sorry, no treks are available within your criteria.")

