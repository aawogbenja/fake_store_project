import streamlit as st
import sqlite3
import pandas as pd
import os

# Connect to the database and load data into a DataFrame

def load_data():
    db_path = r"C:\Users\user\fake_store_project\db\products.db"

    # Check if the database file exists
    if not os.path.exists(db_path):
        st.error(f"Database file not found at {db_path}. Please ensure the file exists.")
        return pd.DataFrame()  # Return an empty DataFrame to prevent app crashing

    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql("SELECT * FROM products", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Load data
df = load_data()

# Display the data
if not df.empty:
    st.dataframe(df)
else:
    st.write("No data available.")

# Streamlit App Title
st.title("🛒 E-commerce Products Dashboard")

# Search bar
search_query = st.text_input("Search for a product")
if search_query:
    df = df[df['title'].str.contains(search_query, case=False, na=False)]

# Price range slider
min_price, max_price = st.slider("Price Range", float(df['price'].min()), float(df['price'].max()), (float(df['price'].min()), float(df['price'].max())))
df = df[(df['price'] >= min_price) & (df['price'] <= max_price)]

# Category filter
categories = st.multiselect("Select Categories", df['category'].unique(), default=df['category'].unique())
df = df[df['category'].isin(categories)]

# Display the filtered data
st.write("### Filtered Products")
st.dataframe(df)

# Visualizations
st.write("### Price Distribution")
st.bar_chart(df[['title', 'price']].set_index('title'))

# Pie chart for categories
st.write("### Product Categories")
category_count = df['category'].value_counts()
st.write(category_count)
st.write(category_count.plot.pie(autopct='%1.1f%%'))
