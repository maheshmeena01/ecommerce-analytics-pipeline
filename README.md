# Real-Time E-commerce Analytics and Recommendation Engine

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?style=for-the-badge&logo=postgresql&logoColor=white)![Pandas](https://img.shields.io/badge/Pandas-2.2-blue?style=for-the-badge&logo=pandas&logoColor=white)![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.4-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask&logoColor=white)![Dash](https://img.shields.io/badge/Dash-2.16-blue?style=for-the-badge&logo=plotly&logoColor=white)

### Project Overview

This project is a comprehensive, full-stack data platform designed to simulate and analyze an e-commerce business. It features a complete data pipeline that ingests user interaction data, processes it through an ETL script, stores it in a relational database, and serves the aggregated insights through a dynamic analytics dashboard. Additionally, it includes a machine learning-powered recommendation engine exposed via a RESTful API to provide personalized product suggestions.

This project demonstrates a robust understanding of data engineering, backend development, database management, and data visualization, making it an ideal showcase for technical skills.

### Live Dashboard Screenshot

*To add your screenshot, replace the file `dashboard_screenshot.png` in the root directory with your own image.*

![E-commerce Analytics Dashboard](./dashboard_screenshot.png)

---

### Key Features

*   **Automated Data Pipeline:** A Python script simulates real-time user events (views, add-to-carts, purchases), populating the database with realistic data.
*   **Scalable Data Warehouse:** Utilizes PostgreSQL to store raw interaction data and aggregated analytics summaries, with a schema designed for efficient querying.
*   **Automated ETL Processing:** A Python script runs as a batch job to **E**xtract raw data, **T**ransform it into meaningful daily sales summaries, and **L**oad it into an analytics-ready table.
*   **Interactive Analytics Dashboard:** A web-based dashboard built with Dash and Plotly provides key business intelligence, visualizing KPIs like total sales, unique customers, and products sold over time.
*   **RESTful Recommendation API:** A Flask-based API serves real-time product recommendations using a user-based collaborative filtering model trained on user interaction data.

### Project Architecture

The project follows a standard multi-tiered data architecture:

1.  **Data Ingestion & Simulation:**
    *   `scripts/data_simulator.py` generates fake user and product data and simulates user interactions (clicks, purchases), inserting them into the raw database tables.

2.  **Data Storage (PostgreSQL Database):**
    *   **Raw Tables:** `users`, `products`, `interactions` store the granular, unprocessed data.
    *   **Summary Table:** `sales_summary` stores the aggregated daily results from the ETL process, enabling fast dashboard queries.

3.  **Data Processing (ETL):**
    *   `scripts/etl_pipeline.py` reads from the raw `interactions` table, performs aggregations using Pandas, and "upserts" the daily summary into the `sales_summary` table.

4.  **Application Layer:**
    *   **Analytics Dashboard (`dashboard/app.py`):** Queries the `sales_summary` table to visualize historical trends and KPIs.
    *   **Recommendation Engine (`api/`):**
        *   The model in `recommendation_model.py` is trained on data from the `interactions` table.
        *   The Flask app in `app.py` exposes the trained model via a simple API endpoint.

---

### Tech Stack

| Category                  | Technologies                                                                          |
| ------------------------- | ------------------------------------------------------------------------------------- |
| **Backend & Scripting**   | Python                                                                                |
| **Database**              | PostgreSQL                                                                            |
| **Data Processing & ML**  | Pandas, NumPy, Scikit-learn, SciPy                                                    |
| **API**                   | Flask                                                                                 |
| **Dashboard & Frontend**  | Dash, Plotly, Dash Bootstrap Components                                               |
| **Database Interaction**  | SQLAlchemy, psycopg2-binary                                                           |

---

### Local Development Setup

Follow these steps to set up and run the project on your local machine.

#### 1. Prerequisites
*   Python 3.8+
*   PostgreSQL 14+ installed and running.
*   Git

#### 2. Clone the Repository
```bash
git clone <your-repository-url>
cd ecommerce_analytics
```

#### 3. Set Up Virtual Environment & Install Dependencies
It is highly recommended to use a virtual environment.

**On Windows (PowerShell):**
```powershell
# Create a virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Install all required packages
pip install -r requirements.txt
```

#### 4. Database Configuration
You need to create the database and the tables. Make sure your credentials are set to `user: postgres` and `password: admin` in all scripts, or update the scripts to match your configuration.

1.  **Create the Database:**
    *   Navigate to your PostgreSQL `bin` directory in a new terminal (e.g., `C:\Program Files\PostgreSQL\17\bin`).
    *   Run the command below and enter your admin password when prompted.
    ```powershell
    .\createdb.exe -U postgres ecommerce_db
    ```
2.  **Create Tables & Schema:**
    *   From that same `bin` directory, run the `db_setup.sql` script. **Replace the file path** with the absolute path to the file on your machine.
    ```powershell
    .\psql.exe -U postgres -d ecommerce_db -f "C:\path\to\your\project\ecommerce_analytics\scripts\db_setup.sql"
    ```

---

### How to Run the Project

The pipeline must be run in order from the project's root directory.

#### 1. Populate the Database
This script simulates user activity and populates the raw data tables.
```powershell
python scripts/data_simulator.py
```

#### 2. Run the ETL Pipeline
This script processes the raw data and populates the `sales_summary` table.
```powershell
python scripts/etl_pipeline.py
```

#### 3. Run the Analytics Dashboard
Open a terminal, activate the virtual environment, and run:
```powershell
python dashboard/app.py
```
Navigate to **`http://127.0.0.1:8050/`** in your web browser.

#### 4. Run the Recommendation API
Open a **separate** terminal, activate the virtual environment, and run:
```powershell
python api/app.py
```
The API will be available at `http://127.0.0.1:5001/`.

### API Endpoints

#### Get Product Recommendations

*   **Endpoint:** `GET /recommendations/<user_id>`
*   **Description:** Returns a list of personalized product recommendations for a given `user_id`.
*   **Example Usage:**
    *   Open your browser and navigate to `http://127.0.0.1:5001/recommendations/15` to get 5 recommendations for the user with ID 15.

---

### Future Improvements

*   **Containerization:** Containerize each component (API, Dashboard, Database) using Docker and manage them with Docker Compose for easier deployment and scalability.
*   **Cloud Deployment:** Deploy the application to a cloud platform like AWS or GCP, using services like RDS for PostgreSQL, EC2 for hosting, and S3 for data storage.
*   **Workflow Orchestration:** Use a tool like Apache Airflow to schedule and manage the ETL pipeline, providing better monitoring, retries, and dependency management.
*   **Advanced Recommendation Model:** Implement a more advanced model like Matrix Factorization (SVD) or a deep learning-based model to handle scalability and the cold-start problem more effectively.