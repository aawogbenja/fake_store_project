import requests
import sqlite3
import os

def fetch_products():
    url = "https://fakestoreapi.com/products"

    # Ensure the 'db' folder exists
    db_folder = "db"
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    db_path = os.path.join(db_folder, "products.db")

    try:
        # Fetch data from the Fake Store API
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        products = response.json()

        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create the products table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                title TEXT,
                price REAL,
                category TEXT,
                description TEXT,
                image TEXT
            )
        ''')

        # Insert products into the database
        cursor.executemany('''
            INSERT OR REPLACE INTO products (id, title, price, category, description, image)
            VALUES (:id, :title, :price, :category, :description, :image)
        ''', products)

        # Commit and close the database connection
        conn.commit()
        conn.close()

        print("Products successfully fetched and saved to the database.")

    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the function if the script is executed directly
if __name__ == "__main__":
    fetch_products()
