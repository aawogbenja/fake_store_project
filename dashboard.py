import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os
from scraper.fetch_products import fetch_products

# Load data from the database
def load_data():
    db_path = "db/products.db"
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

# Refresh Button
if st.button("Refresh Data"):
    with st.spinner("Fetching data..."):
        fetch_products()
        st.success("Data refreshed successfully!")
        df = load_data()

# Filters
st.title("🛒 E-commerce Products Dashboard")

selected_categories = st.multiselect("Filter by Categories", df['category'].unique(), default=df['category'].unique())
filtered_df = df[df['category'].isin(selected_categories)]

if 'price' in filtered_df.columns and not filtered_df.empty:
    min_price, max_price = st.slider("Price Range", float(filtered_df['price'].min()), float(filtered_df['price'].max()), (float(filtered_df['price'].min()), float(filtered_df['price'].max())))
    filtered_df = filtered_df[(filtered_df['price'] >= min_price) & (filtered_df['price'] <= max_price)]

# Display Data
st.dataframe(filtered_df)

# Bar Chart with Tooltips
if 'category' in filtered_df.columns and not filtered_df.empty:
    category_count = filtered_df['category'].value_counts()
    fig_bar = px.bar(category_count, x=category_count.index, y=category_count.values, labels={'x': 'Category', 'y': 'Count'}, title='Product Categories', text=category_count.values)
    fig_bar.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(fig_bar)

# Line Chart for Prices
if 'price' in filtered_df.columns and not filtered_df.empty:
    fig_line = px.line(filtered_df, x='category', y='price', color='title', title='Product Prices by Category', markers=True)
    st.plotly_chart(fig_line)

# Image Gallery
st.write("### Product Image Gallery")
if not filtered_df.empty:
    cols = st.columns(3)
    for i, row in enumerate(filtered_df.itertuples()):
        with cols[i % 3]:
            st.image(row.image, caption=row.title, use_container_width=True)
