# Reponoya_LAB4

============ Pip Dependencies to Install ============
Run Command in Terminal → _pip install pandas mysql-connector-python_
=====================================================


Sample Output :

--- Shelf-Life Report (Expiring Soon) ---
  batch_id         item_name  current_stock expiration_date
0     B104   Chia Seeds 250g             30      2026-09-20
1     B102  Vitamin C 1000mg             45      2026-09-25

--- User Consumption Patterns ---
                   item_name  total_consumed
0  Oral Rehydration Solution            15.0
1        Whey Protein Powder             4.0
2           Vitamin C 1000mg             3.0
3            Chia Seeds 250g             2.0

--- Restock Alert Service Output ---
                   item_name  ...  days_until_depletion
0  Oral Rehydration Solution  ...                   7.0
2        Whey Protein Powder  ...                   8.8
4       Clinical Thermometer  ...                   8.0

[3 rows x 5 columns]

--- Trend Analysis: Top Consumed Items ---
                   item_name            category  daily_usage_rate
0  Oral Rehydration Solution  Clinical Nutrition          2.142857
2        Whey Protein Powder  Clinical Nutrition          0.571429
1           Vitamin C 1000mg         Supplements          0.428571
3            Chia Seeds 250g        Health Foods          0.285714
4       Clinical Thermometer    Medical Supplies          0.000000
