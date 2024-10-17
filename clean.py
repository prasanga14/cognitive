
import pandas as pd
import numpy as np

data = pd.read_csv('dataset.csv')

print("Initial Data:")
print(data.head())

# Check for missing values
print("\nMissing Values Before Imputation:")
print(data.isnull().sum())

data.columns = data.columns.str.lower().str.replace(' ', '_').str.replace(r'[^a-zA-Z0-9_]', '')

print(data.columns)

# Clean the 'Cost' column by removing unwanted characters and converting to float
data['cost'] = data['cost'].str.replace('[$,]', '', regex=True).str.replace(' USD', '').astype(float)

data['Time'] = data['Time'].str.extract('(\d+)').astype(float)  # Extract numeric part and convert to float

# Define an expanded mapping for trip grades
trip_grade_mapping = {
    'Easy': 'Easy',
    'Easy to Moderate': 'Moderate',
    'Easy To Moderate': 'Moderate',  # New addition
    'Moderate': 'Moderate',
    'Moderate + Demanding': 'Demanding',
    'Moderate+Demanding': 'Demanding',  # New addition
    'Demanding': 'Demanding',
    'Very Demanding': 'Very Demanding',
    'Strenuous': 'Strenuous',  # Keep as it is
    'Light+Moderate': 'Moderate',  # New addition
    'Demanding+Challenging': 'Demanding',  # New addition
    'Light': 'Easy',  # New addition
    'Moderate-Hard': 'Hard',  # New addition
    'Easy-Moderate': 'Moderate'  # New addition
    # Add other mappings as needed
}

# Apply the mapping to the 'Trip Grade' column
data['trip_grade'] = data['trip_grade'].replace(trip_grade_mapping)

# Check unique values after mapping
print("\nUnique values in 'Trip Grade' after standardization:")
print(data['trip_grade'].unique())

# Check for any missing values after mapping
print("\nMissing Values After Trip Grade Standardization:")
print(data['trip_grade'].isnull().sum())

# Convert the 'max_altitude' column to string, in case it contains numeric values
data['max_altitude'] = data['max_altitude'].astype(str)

# Remove ' m' and commas if they exist
data['max_altitude'] = data['max_altitude'].str.replace(' m', '', regex=False)  # Remove ' m'
data['max_altitude'] = data['max_altitude'].str.replace(',', '', regex=False)   # Remove commas

# Convert the cleaned 'max_altitude' column back to numeric, handling errors
data['max_altitude'] = pd.to_numeric(data['max_altitude'], errors='coerce')

# Define a mapping for standardizing accommodation types
accommodation_mapping = {
    'Hotel/Guesthouse': 'Hotel',
    'Hotel/Teahouse': 'Teahouse',
    'Hotel/Teahouses': 'Teahouse',
    'Hotel/Guest Houses': 'Guesthouse',
    'Hotel/Guesthouses': 'Guesthouse',
    'Teahouses/Lodges': 'Teahouse',
    'Hotel/Lodges': 'Lodge',
    'Hotel/Luxury Lodges': 'Luxury Lodge',
    'Teahouses': 'Teahouse',
    # Add more mappings if needed
}

# Clean the Accomodation column by mapping the values
data['accomodation'] = data['accomodation'].replace(accommodation_mapping)

# Optionally, remove any trailing or leading whitespace
data['accomodation'] = data['accomodation'].str.strip()

# Function to map the 'Best Travel Time' to seasons
def map_season(travel_time):
    # Check for Spring and Fall months
    if ('March' in travel_time or 'April' in travel_time or 'May' in travel_time) and \
       ('Sept' in travel_time or 'Oct' in travel_time or 'Nov' in travel_time or 'Dec' in travel_time):
        return 'Spring/Fall'
    # Check for Spring only
    elif 'March' in travel_time or 'April' in travel_time or 'May' in travel_time:
        return 'Spring'
    # Check for Fall only
    elif 'Sept' in travel_time or 'Oct' in travel_time or 'Nov' in travel_time or 'Dec' in travel_time:
        return 'Fall'
    # Check for Winter (Jan-Feb)
    elif 'Jan' in travel_time or 'Feb' in travel_time:
        return 'Winter'
    else:
        # If for some reason, none of the above fits, assign 'Spring/Fall' as default
        return 'Spring/Fall'

# Apply the function to the 'Best Travel Time' column
data['best_travel_time'] = data['best_travel_time'].apply(map_season)

# Check the unique values after mapping
print("Unique values in 'Best Travel Time' after mapping:")
print(data['best_travel_time'].unique())

# Define a mapping for Employment Type
employment_type_mapping = {
    'Government Sector': 'Public Sector',
    'Private Sector/Self Employed': 'Private Sector'
}

# Apply the mapping to the 'Employment Type' column
data['employment_type'] = data['employment_type'].replace(employment_type_mapping)

# Impute missing values with the mean of the column
mean_review = data['review/satisfaction'].mean()
data['review/satisfaction'] = data['review/satisfaction'].fillna(mean_review)

# Ensure all values are within the range [1, 5]
# Any value outside this range can be treated as NaN
data['review/satisfaction'] = data['review/satisfaction'].apply(
    lambda x: x if 1 <= x <= 5 else np.nan
)

# Impute NaN values again if they were created by the range check
data['review/satisfaction'] = data['review/satisfaction'].fillna(mean_review)

# Check unique values after cleaning
print("\nUnique values in 'Review/Satisfaction' after cleaning:")
print(data['review/satisfaction'].unique())

# Check for any missing values after cleaning
print("\nMissing Values After Review/Satisfaction Cleaning:")
print(data['review/satisfaction'].isnull().sum())

# Fill missing values with the mode or a default value
mode_health_incidents = data['health_incidents'].mode()[0]  # Get the mode (most frequent value)
data['health_incidents'] = data['health_incidents'].fillna(mode_health_incidents)

# Optionally, if you want to replace None or empty strings specifically
data['health_incidents'] = data['health_incidents'].replace(['None', ''], mode_health_incidents)

# Check unique values after cleaning
print("\nUnique values in 'Health Incidents' after cleaning:")
print(data['health_incidents'].unique())

# Check for any missing values after cleaning
print("\nMissing Values After Health Incidents Cleaning:")
print(data['health_incidents'].isnull().sum())

print(data['Best Travel Time'].unique())

# Check unique values before cleaning
print("Unique values in 'Equipment Used' before cleaning:")
print(data['equipment_used'].unique())

# Standardize values: convert 'None', empty strings, and spaces to np.nan
data['equipment_used'] = data['equipment_used'].replace(['None', '', ' ', None], np.nan)

# Check unique values after replacing with NaN
print("\nUnique values in 'Equipment Used' after standardization:")
print(data['equipment_used'].unique())

# Fill missing values with the mode (most common value)
mode_equipment = data['equipment_used'].mode()[0]  # Get the mode (most frequent value)

# Avoiding chained assignment by using .loc to fill NaN values
data.loc[data['equipment_used'].isnull(), 'equipment_used'] = mode_equipment

# Final unique values and missing count
print("\nUnique values in 'Equipment Used' after filling:")
print(data['equipment_used'].unique())

print("\nMissing Values After Equipment Used Cleaning:")
print(data['equipment_used'].isnull().sum())

# Check unique values before cleaning
print("Unique values in 'Guide/No Guide' before cleaning:")
print(data['guide/no_guide'].unique())

# Standardize values: convert empty strings and spaces to np.nan
data['guide/no_guide'] = data['guide/no_guide'].replace(['', ' ', None], np.nan)

# Check unique values after replacing with NaN
print("\nUnique values in 'Guide/No Guide' after standardization:")
print(data['guide/no_guide'].unique())

# Fill missing values with the mode (most common value)
mode_guide = data['guide/no_guide'].mode()[0]  # Get the mode (most frequent value)

# Fill NaN values with the mode without using inplace
data['guide/no_guide'] = data['guide/no_guide'].fillna(mode_guide)

# Final unique values and missing count
print("\nUnique values in 'Guide/No Guide' after filling:")
print(data['guide/no_guide'].unique())

print("\nMissing Values After Guide/No Guide Cleaning:")
print(data['guide/no_guide'].isnull().sum())

# Check unique values before cleaning
print("Unique values in 'Purpose of Travel' before cleaning:")
print(data['purpose_of_travel'].unique())

# Standardize values: convert empty strings and spaces to np.nan
data['purpose_of_travel'] = data['purpose_of_travel'].replace(['', ' ', None], np.nan)

# Check unique values after replacing with NaN
print("\nUnique values in 'Purpose of Travel' after standardization:")
print(data['purpose_of_travel'].unique())

# Fill missing values with the mode (most common value)
mode_purpose = data['purpose_of_travel'].mode()[0]  # Get the mode (most frequent value)

# Fill NaN values with the mode without using inplace
data['purpose_of_travel'] = data['purpose_of_travel'].fillna(mode_purpose)

# Final unique values and missing count
print("\nUnique values in 'Purpose of Travel' after filling:")
print(data['purpose_of_travel'].unique())

print("\nMissing Values After Purpose of Travel Cleaning:")
print(data['purpose_of_travel'].isnull().sum())

# Check unique values before cleaning
print("Unique values in 'Trekking Group Size' before cleaning:")
print(data['trekking_group_size'].unique())

# Convert the column to numeric (this will turn any non-numeric values to NaN)
data['trekking_group_size'] = pd.to_numeric(data['trekking_group_size'], errors='coerce')

# Calculate the mean of the column, ignoring NaN values, and round it to the nearest integer
mean_group_size = round(data['trekking_group_size'].mean())

# Fill NaN values with the rounded mean using assignment to avoid the FutureWarning
data['trekking_group_size'] = data['trekking_group_size'].fillna(mean_group_size)

# Convert the filled column to integer type
data['trekking_group_size'] = data['trekking_group_size'].astype(int)

# Final unique values and missing count
print("\nUnique values in 'Trekking Group Size' after filling:")
print(data['trekking_group_size'].unique())

print("\nMissing Values After Trekking Group Size Cleaning:")
print(data['trekking_group_size'].isnull().sum())

# Check unique values before cleaning
print("Unique values in 'Weather Conditions' before cleaning:")
print(data['weather_conditions'].unique())

# Standardizing the column by stripping whitespace and replacing empty strings with NaN
data['weather_conditions'] = data['weather_conditions'].replace('', np.nan).str.strip()

# Calculate the mode of the column (the most frequent value)
mode_weather = data['weather_conditions'].mode()[0]

# Fill NaN values with the mode using assignment to avoid the FutureWarning
data['weather_conditions'] = data['weather_conditions'].fillna(mode_weather)

# Final unique values and missing count
print("\nUnique values in 'Weather Conditions' after filling:")
print(data['weather_conditions'].unique())

print("\nMissing Values After Weather Conditions Cleaning:")
print(data['weather_conditions'].isnull().sum())

# Check unique values before cleaning
print("Unique values in 'Fitness Level' before cleaning:")
print(data['fitness_level'].unique())

# Standardizing the column by replacing empty strings with NaN
data['fitness_level'] = data['fitness_level'].replace('', np.nan)

# Calculate the mode of the column (the most frequent value)
mode_fitness = data['fitness_level'].mode()[0]

# Fill NaN values with the mode using assignment to avoid the FutureWarning
data['fitness_level'] = data['fitness_level'].fillna(mode_fitness)

# Final unique values and missing count
print("\nUnique values in 'Fitness Level' after filling:")
print(data['fitness_level'].unique())

print("\nMissing Values After Fitness Level Cleaning:")
print(data['fitness_level'].isnull().sum())

# Display unique values before encoding
print("Unique values in 'FrequentFlyer' before encoding:")
print(data['frequentflyer'].unique())

# Apply one-hot encoding
data_encoded = pd.get_dummies(data, columns=['frequentflyer'], prefix='frequentflyer', drop_first=True)

# Display the new DataFrame with one-hot encoding
print("\nDataFrame after one-hot encoding:")
print(data_encoded)

data.to_csv('cleaned_dataset.csv', index=False)
print("Data cleaning completed. Cleaned dataset saved.")

