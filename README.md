# End-to-End E-commerce Analytics Platform

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?style=for-the-badge&logo=postgresql&logoColor=white)![Pandas](https://img.shields.io/badge/Pandas-2.2-blue?style=for-the-badge&logo=pandas&logoColor=white)![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.4-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask&logoColor=white)![Dash](https://img.shields.io/badge/Dash-2.16-blue?style=for-the-badge&logo=plotly&logoColor=white)

### Project Summary

This project is a complete, end-to-end data platform that simulates and analyzes an e-commerce business. It showcases proficiency in data engineering, backend development, and data visualization, making it an ideal project for top-tier campus placements. The system features a full data pipeline: ingesting simulated user data, processing it via an ETL script, storing it in a PostgreSQL database, and visualizing key metrics on an interactive dashboard. It is further enhanced by a machine learning-powered recommendation engine served via a REST API.

---

### Key Features

-   **Data Simulation & Ingestion:** A Python script generates realistic user, product, and interaction data (views, cart additions, purchases) to populate the database.
-   **Relational Data Warehouse:** Utilizes PostgreSQL to store raw data and aggregated analytical summaries in a well-defined schema for efficient querying.
-   **ETL (Extract, Transform, Load) Pipeline:** A robust Python script extracts raw interaction data, transforms it into daily performance summaries using Pandas, and loads it into a clean, analytics-ready table.
-   **Interactive Analytics Dashboard:** A dynamic web dashboard built with **Dash** and **Plotly** provides at-a-glance business intelligence, visualizing KPIs like sales trends, unique customers, and product performance.
-   **RESTful Recommendation API:** A **Flask** API serves real-time product recommendations using a user-based collaborative filtering model built with **Scikit-learn**.

---

### Data Architecture Flow

The project follows a logical, multi-stage data flow from generation to insight:

```
[Data Simulator (Python/Faker)]
       |
       v
[PostgreSQL Database (Raw Tables: users, products, interactions)]
       |
       +----------------------> [Recommendation API (Flask / Scikit-learn)] -> [GET /recommendations/:id]
       |
       v
[ETL Pipeline (Python/Pandas)]
       |
       v
[PostgreSQL Database (Summary Table: sales_summary)]
       |
       v
[Analytics Dashboard (Dash / Plotly)]
```

---

### Tech Stack & Skills Demonstrated

| Domain                    | Technologies & Concepts                                        |
| ------------------------- | -------------------------------------------------------------- |
| **Data Engineering**      | ETL Pipeline Development, Data Modeling, Database Schema Design|
| **Backend Development**   | Python, Flask, RESTful API Design                              |
| **Database Management**   | PostgreSQL, SQL, Query Optimization, Stored Procedures (Conceptual) |
| **Data Science & ML**     | Collaborative Filtering, Scikit-learn, Pandas, NumPy           |
| **Data Visualization**    | Dash, Plotly, Dash Bootstrap Components                        |
| **DevOps & Tools**        | Git, GitHub, Virtual Environments (`venv`)                     |

---

### Local Development Setup

Follow these steps to set up and run the project on your local machine.

#### 1. Prerequisites
-   Python 3.8+
-   PostgreSQL 14+ installed and running.
-   Git installed and configured.

#### 2. Clone the Repository
```bash
git clone https://github.com/maheshmeena01/ecommerce-analytics-pipeline.git
cd ecommerce-analytics-pipeline
```

#### 3. Set Up Virtual Environment & Install Dependencies
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
The scripts are configured for `user: postgres` and `password: admin`.

1.  **Create the Database:**
    -   Navigate to your PostgreSQL `bin` directory (e.g., `C:\Program Files\PostgreSQL\17\bin`).
    -   Run the command below and enter `admin` when prompted for a password.
    ```powershell
    .\createdb.exe -U postgres ecommerce_db
    ```
2.  **Create Tables & Schema:**
    -   From the same `bin` directory, run the `db_setup.sql` script. **Replace the file path** with the absolute path to the file on your machine.
    ```powershell
    .\psql.exe -U postgres -d ecommerce_db -f "C:\Users\mahes\Documents\ecommerce_analytics\scripts\db_setup.sql"
    ```

---

### How to Run the Project

The pipeline must be run in order from the project's root directory.

#### 1. Populate the Database
This script populates the raw data tables.
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
> Navigate to **`http://127.0.0.1:8050/`** in your web browser.

#### 4. Run the Recommendation API
Open a **separate** terminal, activate the virtual environment, and run:
```powershell
python api/app.py
```
> The API will be available at `http://127.0.0.1:5001/`.

### API Usage Example

-   **Endpoint:** `GET /recommendations/<user_id>`
-   **Example:** To get recommendations for user with ID 25, visit `http://127.0.0.1:5001/recommendations/25` in your browser.
