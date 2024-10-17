# import os
# import textwrap
# import streamlit as st
# import pandas as pd
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.docstore.document import Document

# # Set Hugging Face API token if needed
# os.environ["HUGGINGFACEHUB_API_TOKEN"] = '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'

# # Load the CSV data
# FILE_PATH = "cleaned.csv"
# data = pd.read_csv(FILE_PATH)

# # Combine relevant columns into a single text field for embeddings
# def combine_columns(row):
#     return f"Trek Name: {row['Trek Name']}, Difficulty: {row['Difficulty']}, Season: {row['Best Travel Time']}, Weather: {row['Weather Conditions']}, Group Size: {row['Trekking Group Size']}"

# # Create a new column combining relevant info for embedding search
# data['combined_text'] = data.apply(combine_columns, axis=1)

# # Preprocessing function to wrap long text while preserving newlines
# def wrap_text_preserve_newlines(text, width=110):
#     lines = text.split("\n")
#     wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
#     wrapped_texts = '\n'.join(wrapped_lines)
#     return wrapped_texts

# # Convert the combined text into Document objects
# docs = [Document(page_content=text) for text in data['combined_text'].tolist()]

# # Embedding with HuggingFace and FAISS
# embeddings = HuggingFaceEmbeddings()
# db = FAISS.from_documents(docs, embeddings)

# # Streamlit interface for user interaction
# st.title("Trekking Guide Chatbot")

# # User query input
# query = st.text_input("Ask anything about trekking:")

# # Helper function to extract relevant fields from a matching document
# def extract_relevant_info(document_text, query):
#     # Simple keyword matching to identify intent and provide relevant information
#     if "season" in query.lower():
#         return document_text.split(",")[2]  # Best Travel Time
#     elif "difficulty" in query.lower():
#         return document_text.split(",")[1]  # Difficulty
#     elif "weather" in query.lower():
#         return document_text.split(",")[3]  # Weather Conditions
#     elif "group size" in query.lower():
#         return document_text.split(",")[4]  # Trekking Group Size
#     else:
#         # Return a default summary if the question is too vague
#         return document_text

# # Answer generation based on user query
# if query:
#     doc = db.similarity_search(query)

#     if doc:
#         relevant_info = extract_relevant_info(doc[0].page_content, query)
#         st.write("Answer:")
#         st.write(wrap_text_preserve_newlines(relevant_info))
#     else:
#         st.write("No relevant information found.")
 

import pandas as pd
import streamlit as st

# Load your cleaned trekking dataset
data = pd.read_csv("cleaned.csv")

# Set up the Streamlit app
st.title("Trekking Guide - Find Treks Within Your Budget")

# Ask for user input: Budget
budget = st.number_input("Enter your budget (in USD):", min_value=0, step=100)

# Filter the treks based on the user input
filtered_data = data[data['cost'] <= budget]

# Display the filtered treks
if budget > 0:
    if not filtered_data.empty:
        st.write(f"Treks within your budget of ${budget}:")
        # Show the relevant trek columns for the user
        st.write(filtered_data[['trek', 'cost', 'time', 'trip_grade', 'max_altitude', 'best_travel_time']])
    else:
        st.write("Sorry, no treks are available within your budget.")
else:
    st.write("Please enter a valid budget.")

# Optional: Add a sidebar for users to fine-tune the budget range
st.sidebar.title("Filter Options")
min_cost, max_cost = st.sidebar.slider("Select your budget range", 0, int(data['cost'].max()), (0, int(data['cost'].max())))

filtered_data_range = data[(data['cost'] >= min_cost) & (data['cost'] <= max_cost)]

if not filtered_data_range.empty:
    st.sidebar.write(f"Treks within ${min_cost} to ${max_cost} range:")
    st.sidebar.write(filtered_data_range[['trek', 'cost', 'time', 'trip_grade']])
else:
    st.sidebar.write("No treks available in this range.")

