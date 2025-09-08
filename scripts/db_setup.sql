-- scripts/db_setup.sql

-- Drop tables if they exist to start fresh
DROP TABLE IF EXISTS interactions, products, users, sales_summary;

-- Products Table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INT,
    country VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User Interactions Table (raw data)
CREATE TABLE interactions (
    interaction_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    product_id INT REFERENCES products(product_id),
    event_type VARCHAR(50), -- e.g., 'view', 'add_to_cart', 'purchase'
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Aggregated Sales Summary Table (for the dashboard)
CREATE TABLE sales_summary (
    summary_id SERIAL PRIMARY KEY,
    sale_date DATE NOT NULL UNIQUE, -- The word UNIQUE must be here
    total_sales DECIMAL(15, 2),
    unique_customers INT,
    total_products_sold INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for faster queries
CREATE INDEX idx_interactions_user_id ON interactions(user_id);
CREATE INDEX idx_interactions_product_id ON interactions(product_id);