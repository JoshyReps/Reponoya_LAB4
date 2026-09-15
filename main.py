import mysql.connector
import pandas as pd
import warnings


password5252 = "Hotdogthgang!"
password6525 = "west3rnGang@!"
password5252 = "n0rthgang!"
password5251 = "#!@%!@%!@%!"
password5352 = "Southgang!!"
password5253 = "west0lock!"



# 1. Connect to MySQL Server
# Update 'user' and 'password' with your local MySQL credentials
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password5252,
    database="healthcare_inventory"
)
cursor = conn.cursor()


# 2. Create Tables (MySQL Syntax)
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory_batches (
    batch_id VARCHAR(50) PRIMARY KEY,
    item_name VARCHAR(100),
    category VARCHAR(50),
    current_stock INT,
    reorder_threshold INT,
    expiration_date DATE
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS sales_transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    item_name VARCHAR(100),
    quantity_sold INT,
    transaction_date DATE
)
''')


# Clear tables in case you re-run the script during testing
cursor.execute("TRUNCATE TABLE inventory_batches")
cursor.execute("TRUNCATE TABLE sales_transactions")


# 3. Insert Sample Data (Using %s for MySQL placeholders)
sql_inventory = """
INSERT INTO inventory_batches
(batch_id, item_name, category, current_stock, reorder_threshold, expiration_date)
VALUES (%s, %s, %s, %s, %s, %s)
"""
val_inventory = [
    ('B101', 'Oral Rehydration Solution', 'Clinical Nutrition', 15, 20, '2026-10-01'),
    ('B102', 'Vitamin C 1000mg', 'Supplements', 45, 15, '2026-09-25'),
    ('B103', 'Whey Protein Powder', 'Clinical Nutrition', 5, 10, '2026-12-15'),
    ('B104', 'Chia Seeds 250g', 'Health Foods', 30, 10, '2026-09-20'),
    ('B105', 'Clinical Thermometer', 'Medical Supplies', 8, 10, '2027-01-10')
]
cursor.executemany(sql_inventory, val_inventory)


sql_sales = """
INSERT INTO sales_transactions
(item_name, quantity_sold, transaction_date)
VALUES (%s, %s, %s)
"""
val_sales = [
    ('Oral Rehydration Solution', 5, '2026-09-10'),
    ('Oral Rehydration Solution', 10, '2026-09-12'),
    ('Vitamin C 1000mg', 3, '2026-09-11'),
    ('Whey Protein Powder', 4, '2026-09-13'),
    ('Chia Seeds 250g', 2, '2026-09-14')
]
cursor.executemany(sql_sales, val_sales)
conn.commit()


warnings.filterwarnings('ignore', 'pandas only supports SQLAlchemy connectable') # Hides the warning for clean output


# Query 1: Track Shelf-Life (Batches expiring within 15 days)
query_shelflife = """
SELECT batch_id, item_name, current_stock, expiration_date
FROM inventory_batches
WHERE expiration_date <= '2026-09-30'
ORDER BY expiration_date ASC;
"""
print("--- Shelf-Life Report (Expiring Soon) ---")
print(pd.read_sql_query(query_shelflife, conn))


# Query 2: Track User Consumption Patterns
query_consumption = """
SELECT item_name, SUM(quantity_sold) AS total_consumed
FROM sales_transactions
GROUP BY item_name
ORDER BY total_consumed DESC;
"""
print("\n--- User Consumption Patterns ---")
print(pd.read_sql_query(query_consumption, conn))


# Backend Function: Inventory Logging & Restock Alerts
def inventory_logging_and_alerts(conn, observation_days=7):
    df_inventory = pd.read_sql_query("SELECT * FROM inventory_batches", conn)
    df_sales = pd.read_sql_query("SELECT * FROM sales_transactions", conn)
   
    usage = df_sales.groupby('item_name')['quantity_sold'].sum().reset_index()
    usage['daily_usage_rate'] = usage['quantity_sold'] / observation_days
   
    df_analysis = pd.merge(df_inventory, usage[['item_name', 'daily_usage_rate']], on='item_name', how='left').fillna(0)
    df_analysis['days_until_depletion'] = (df_analysis['current_stock'] / df_analysis['daily_usage_rate'].replace(0, 1)).round(1)
    df_analysis['trigger_alert'] = df_analysis['current_stock'] <= df_analysis['reorder_threshold']
   
    return df_analysis


# Run module and output alerts
df_results = inventory_logging_and_alerts(conn)
print("\n--- Restock Alert Service Output ---")
alerts = df_results[df_results['trigger_alert'] == True]
print(alerts[['item_name', 'current_stock', 'reorder_threshold', 'daily_usage_rate', 'days_until_depletion']])


# Trend Calculation Service
def trend_calculation_service(df_results):
    fast_moving = df_results.sort_values(by='daily_usage_rate', ascending=False)
    print("\n--- Trend Analysis: Top Consumed Items ---")
    print(fast_moving[['item_name', 'category', 'daily_usage_rate']])


trend_calculation_service(df_results)


# Close connection when done
cursor.close()
conn.close()




















