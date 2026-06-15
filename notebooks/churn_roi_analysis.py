import sqlite3
import pandas as pd
from IPython.display import display

# ==========================================
# 1. CONFIGURATION & PARAMETERS
# ==========================================
# Menyimpan variabel statis di atas memudahkan update di masa depan
# tanpa perlu membongkar atau mencari-cari di dalam query SQL.
DB_PATH = 'data/churn_roi_project.db' # Asumsi database ada di folder data/
CUTOFF_DATE = '2026-06-15'
CHURN_THRESHOLD_DAYS = 60

# ==========================================
# 2. DATA EXTRACTION LAYER
# ==========================================
def fetch_churn_data(db_path: str, cutoff_date: str, churn_days: int) -> pd.DataFrame:
    """
    Fetches and aggregates customer churn data from the SQLite database.
    A customer is flagged as 'churned' if their last transaction is 
    older than the specified churn_days threshold from the cutoff_date.
    """
    # Menggunakan f-string untuk menyuntikkan parameter dinamis ke dalam SQL
    query = f"""
    WITH user_last_transaction AS (
        SELECT 
            user_id,
            MAX(transaction_date) AS last_tx_date
        FROM transactions
        GROUP BY user_id
    ),
    user_churn_status AS (
        SELECT 
            u.user_id,
            u.acquisition_channel,
            u.location,
            CASE 
                WHEN (julianday('{cutoff_date}') - julianday(t.last_tx_date)) > {churn_days} THEN 1 
                ELSE 0 
            END AS is_churn
        FROM users u
        LEFT JOIN user_last_transaction t ON u.user_id = t.user_id
    )
    SELECT 
        location AS [Location],
        acquisition_channel AS [Acquisition Channel],
        COUNT(user_id) AS [Total Customers],
        SUM(is_churn) AS [Churned Customers],
        ROUND(AVG(is_churn) * 100, 2) AS [Churn Rate (%)]
    FROM user_churn_status
    GROUP BY location, acquisition_channel
    ORDER BY location, [Churn Rate (%)] DESC;
    """
    
    # Penggunaan 'with' (Context Manager) memastikan koneksi database 
    # selalu tertutup otomatis meskipun terjadi error pada query.
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(query, conn)
        return df
    except sqlite3.Error as e:
        print(f"⚠️ Database Execution Error: {e}")
        return pd.DataFrame() # Mengembalikan DataFrame kosong jika gagal

# ==========================================
# 3. DATA PRESENTATION LAYER (STYLING)
# ==========================================
def apply_professional_styling(df: pd.DataFrame):
    """
    Applies CSS/HTML styling to the Pandas DataFrame for a clean, 
    business-ready presentation in Jupyter Notebooks.
    """
    return df.style\
        .background_gradient(cmap='Reds', subset=['Churn Rate (%)'])\
        .bar(subset=['Total Customers'], color='#A8DADC')\
        .format({
            'Churn Rate (%)': '{:.2f}%', 
            'Total Customers': '{:,}', 
            'Churned Customers': '{:,}'
        })\
        .set_properties(**{
            'text-align': 'center', 
            'font-family': 'Segoe UI, Helvetica, sans-serif'
        })\
        .set_table_styles([
            {'selector': 'th', 'props': [
                ('background-color', '#1D3557'), 
                ('color', 'white'), 
                ('font-weight', 'bold'),
                ('text-align', 'center')
            ]}
        ])

# ==========================================
# 4. MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    # Ekstraksi Data
    df_breakdown = fetch_churn_data(DB_PATH, CUTOFF_DATE, CHURN_THRESHOLD_DAYS)
    
    # Render & Tampilkan Tabel jika data berhasil ditarik
    if not df_breakdown.empty:
        styled_df = apply_professional_styling(df_breakdown)
        display(styled_df)
    else:
        print("Dataframe is empty. Please check the database connection.")
