import sqlite3
import pandas as pd
from IPython.display import display

# --- Configuration ---
DB_PATH = 'data/churn_roi_project.db'
CUTOFF_DATE = '2026-06-15'
CHURN_THRESHOLD_DAYS = 60

def get_churn_analysis():
    """Extracts and formats customer churn breakdown."""
    query = f"""
    WITH user_last_transaction AS (
        SELECT user_id, MAX(transaction_date) AS last_tx_date
        FROM transactions GROUP BY user_id
    ),
    user_churn_status AS (
        SELECT u.user_id, u.acquisition_channel, u.location,
            CASE WHEN (julianday('{CUTOFF_DATE}') - julianday(t.last_tx_date)) > {CHURN_THRESHOLD_DAYS} THEN 1 ELSE 0 END AS is_churn
        FROM users u LEFT JOIN user_last_transaction t ON u.user_id = t.user_id
    )
    SELECT location AS [Location], acquisition_channel AS [Acquisition Channel],
           COUNT(user_id) AS [Total Customers], SUM(is_churn) AS [Churned Customers],
           ROUND(AVG(is_churn) * 100, 2) AS [Churn Rate (%)]
    FROM user_churn_status
    GROUP BY location, acquisition_channel
    ORDER BY location, [Churn Rate (%)] DESC;
    """
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn)
    
    return df.style.background_gradient(cmap='Reds', subset=['Churn Rate (%)'])\
        .bar(subset=['Total Customers'], color='#A8DADC')\
        .format({'Churn Rate (%)': '{:.2f}%', 'Total Customers': '{:,}', 'Churned Customers': '{:,}'})\
        .set_table_styles([{'selector': 'th', 'props': [('background-color', '#1D3557'), ('color', 'white')]}])

# Execute
display(get_churn_analysis())
