import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text

# --- Database Connection ---
DB_NAME = "ecommerce_db"
DB_USER = "postgres"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "5432"

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def run_etl():
    """Extracts, transforms, and loads sales data."""
    try:
        engine = create_engine(DB_URL)

        # EXTRACT
        query = """
        SELECT
            i.timestamp::date AS sale_date,
            p.price,
            i.user_id
        FROM interactions i
        JOIN products p ON i.product_id = p.product_id
        WHERE i.event_type = 'purchase'
        """
        df = pd.read_sql(query, engine)

        if df.empty:
            print("No new purchase data to process.")
            return

        # TRANSFORM
        summary_df = df.groupby('sale_date').agg(
            total_sales=('price', 'sum'),
            unique_customers=('user_id', 'nunique'),
            total_products_sold=('price', 'count')
        ).reset_index()

        print("Transformed Data Summary:")
        print(summary_df)

        # LOAD
        with engine.connect() as conn:
            for _, row in summary_df.iterrows():
                # CORRECTED: Removed the redundant .date() call
                insert_query = text(f"""
                INSERT INTO sales_summary (sale_date, total_sales, unique_customers, total_products_sold)
                VALUES ('{row['sale_date']}', {row['total_sales']}, {row['unique_customers']}, {row['total_products_sold']})
                ON CONFLICT (sale_date) DO UPDATE SET
                    total_sales = EXCLUDED.total_sales,
                    unique_customers = EXCLUDED.unique_customers,
                    total_products_sold = EXCLUDED.total_products_sold;
                """)
                conn.execute(insert_query)
            conn.commit()
        
        print(f"Successfully loaded {len(summary_df)} rows into sales_summary.")

    except Exception as e:
        print(f"An error occurred during ETL process: {e}")

if __name__ == "__main__":
    run_etl()