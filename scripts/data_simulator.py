import psycopg2
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# --- Database Connection (Corrected) ---
DB_NAME = "ecommerce_db"
DB_USER = "postgres"  # Corrected username
DB_PASSWORD = "admin"     # Your correct password
DB_HOST = "localhost"
DB_PORT = "5432"

# --- Configuration ---
NUM_USERS = 100
NUM_PRODUCTS = 50
NUM_INTERACTIONS = 1000

fake = Faker()

# --- Data Generation Functions (Corrected) ---
def generate_products():
    products = []
    for _ in range(NUM_PRODUCTS):
        products.append({
            'name': fake.bs().title(),  # CORRECTED: Use fake.bs() for product-like names
            'category': fake.word().capitalize(), # CORRECTED: Use fake.word() for a random category
            'price': round(random.uniform(10.0, 500.0), 2)
        })
    return pd.DataFrame(products)

def generate_users():
    users = []
    for _ in range(NUM_USERS):
        users.append({
            'email': fake.unique.email(),
            'age': random.randint(18, 65),
            'country': fake.country()
        })
    return pd.DataFrame(users)

def generate_interactions(user_ids, product_ids):
    interactions = []
    event_types = ['view', 'add_to_cart', 'purchase']
    for _ in range(NUM_INTERACTIONS):
        start_date = datetime.now() - timedelta(days=90)
        random_date = start_date + timedelta(seconds=random.randint(0, 90*24*60*60))
        interactions.append({
            'user_id': random.choice(user_ids),
            'product_id': random.choice(product_ids),
            'event_type': random.choices(event_types, weights=[0.6, 0.3, 0.1], k=1)[0],
            'timestamp': random_date
        })
    return pd.DataFrame(interactions)


# --- Main Execution ---
if __name__ == "__main__":
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        cur = conn.cursor()

        # Generate and insert products
        products_df = generate_products()
        for _, row in products_df.iterrows():
            cur.execute(
                "INSERT INTO products (name, category, price) VALUES (%s, %s, %s)",
                (row['name'], row['category'], row['price'])
            )
        print(f"Inserted {len(products_df)} products.")

        # Generate and insert users
        users_df = generate_users()
        for _, row in users_df.iterrows():
            cur.execute(
                "INSERT INTO users (email, age, country) VALUES (%s, %s, %s)",
                (row['email'], row['age'], row['country'])
            )
        print(f"Inserted {len(users_df)} users.")

        conn.commit()

        cur.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT product_id FROM products")
        product_ids = [row[0] for row in cur.fetchall()]

        interactions_df = generate_interactions(user_ids, product_ids)
        for _, row in interactions_df.iterrows():
            cur.execute(
                "INSERT INTO interactions (user_id, product_id, event_type, timestamp) VALUES (%s, %s, %s, %s)",
                (row['user_id'], row['product_id'], row['event_type'], row['timestamp'])
            )
        print(f"Inserted {len(interactions_df)} interactions.")

        conn.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        print("Database connection closed.")