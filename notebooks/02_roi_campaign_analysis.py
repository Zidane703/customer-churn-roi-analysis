import sqlite3
import pandas as pd
from IPython.display import display

# --- Configuration ---
DB_PATH = 'data/churn_roi_project.db'
TARGET_CAMPAIGN = 'Retention Promo Q1'

def get_campaign_roi():
    """Calculates ROI and success metrics for marketing campaigns."""
    query = f"""
    WITH user_last_transaction AS (
        SELECT user_id, MAX(transaction_date) AS last_tx_date FROM transactions GROUP BY user_id
    ),
    user_status AS (
        SELECT u.user_id, CASE WHEN (julianday('2026-06-15') - julianday(t.last_tx_date)) > 60 THEN 1 ELSE 0 END AS is_churn
        FROM users u LEFT JOIN user_last_transaction t ON u.user_id = t.user_id
    ),
    campaign_revenue AS (
        SELECT mc.user_id, mc.campaign_name, mc.campaign_cost, COALESCE(SUM(t.amount), 0) AS revenue_post_campaign
        FROM marketing_campaigns mc
        LEFT JOIN transactions t ON mc.user_id = t.user_id AND t.transaction_date > mc.campaign_date
        WHERE mc.campaign_name = '{TARGET_CAMPAIGN}'
        GROUP BY mc.user_id, mc.campaign_name, mc.campaign_cost
    )
    SELECT COUNT(cr.user_id) AS [Targeted Customers], 
           (COUNT(cr.user_id) - SUM(us.is_churn)) AS [Saved Customers],
           ROUND((COUNT(cr.user_id) - SUM(us.is_churn)) * 100.0 / COUNT(cr.user_id), 2) AS [Success Rate (%)],
           SUM(cr.campaign_cost) AS [Total Campaign Cost], 
           SUM(cr.revenue_post_campaign) AS [Total Revenue Generated],
           ROUND((SUM(cr.revenue_post_campaign) - SUM(cr.campaign_cost)) * 100.0 / SUM(cr.campaign_cost), 2) AS [ROI (%)]
    FROM campaign_revenue cr JOIN user_status us ON cr.user_id = us.user_id;
    """
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn)

    return df.style.format({'Success Rate (%)': '{:.2f}%', 'ROI (%)': '{:.2f}%', 'Total Campaign Cost': 'Rp{:,.0f}', 'Total Revenue Generated': 'Rp{:,.0f}', 'Targeted Customers': '{:,}'})\
        .set_table_styles([{'selector': 'th', 'props': [('background-color', '#2A9D8F'), ('color', 'white')]}])\
        .background_gradient(cmap='Greens', subset=['ROI (%)'])

# Execute
display(get_campaign_roi())
