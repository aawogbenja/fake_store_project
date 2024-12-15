import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os
import sys
from scraper.fetch_products import fetch_products
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "scraper")))

# Connect to the database and load data into a DataFrame
def load_data():
    db_path = "db/products.db"

    # Check if the database file exists
    if not os.path.exists(db_path):
        st.error(f"Database file not found at {db_path}. Please ensure the file exists.")
        return pd.DataFrame()

    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql("SELECT * FROM products", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load the data
df = load_data()

# Streamlit App Title
st.title("🛒 E-commerce Products Dashboard")

# Refresh Button
if st.button("Refresh Data"):
    with st.spinner("Fetching data..."):
        fetch_products()
        st.success("Data refreshed successfully!")
        df = load_data()

# Display the data
if not df.empty:
    st.dataframe(df)
else:
    st.write("No data available.")

# Search bar to filter products by title
search_query = st.text_input("Search for a product by title:")
if search_query:
    df = df[df['title'].str.contains(search_query, case=False, na=False)]

# Price range slider
if 'price' in df.columns and not df.empty:
    min_price, max_price = st.slider(
        "Price Range", 
        float(df['price'].min()), 
        float(df['price'].max()), 
        (float(df['price'].min()), float(df['price'].max()))
    )
    df = df[(df['price'] >= min_price) & (df['price'] <= max_price)]
else:
    st.error("The 'price' column is missing from the data.")

# Category filter
if 'category' in df.columns and not df.empty:
    categories = st.multiselect("Select Categories", df['category'].unique(), default=df['category'].unique())
    df = df[df['category'].isin(categories)]
else:
    st.error("The 'category' column is missing from the data.")

# Display filtered data
st.write(df)

# Bar Chart of Product Categories
if 'category' in df.columns and not df.empty:
    category_count = df['category'].value_counts()
    fig = px.bar(category_count, x=category_count.index, y=category_count.values, 
                 labels={'x': 'Category', 'y': 'Count'}, title='Product Categories')
    st.plotly_chart(fig)

# Detailed Product View
if not df.empty:
    selected_product = st.selectbox("Select a product to view details:", df['title'].unique())
    if selected_product:
        product_details = df[df['title'] == selected_product].iloc[0]
        st.write(f"**Title:** {product_details['title']}")
        st.write(f"**Price:** ${product_details['price']}")
        st.write(f"**Category:** {product_details['category']}")
        st.write(f"**Description:** {product_details['description']}")
        st.image(product_details['image'], width=300)
else:
    st.write("No products available for detailed view.")
