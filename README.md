# AI-Driven Customer Buying Behavior Analysis: Last Month vs This Month

## Dataset
- Blinkit-style simulated data, 2 months (Aug = last month, Sep = this month)
- 8,400 orders, 25,000+ rows
- Columns: order_id, customer_id, order_date, order_hour, city, category, product, quantity, unit_price, item_total, payment_method
- File: blinkit_orders.csv

## Data Analysis
1. Cleaning: missing values and duplicates checked
2. Overall: orders 4,000 -> 4,400 (+10%), avg order value Rs.673 -> Rs.774 (+15%)
3. Category-wise: Sweets & Festive +104%, Staples +26%, Beverages -28.7%
4. Product-wise: Dry Fruits, Chocolates, Laddu increased; Cold Drink, Juice, Tea decreased
5. Behavior: Peak ordering hour is 7 PM
6. Charts: chart_category_change.png, chart_hourly_orders.png

Formula: Change % = (this month - last month) / last month x 100

## Conclusion
Festival season increases demand for sweets and staples, while beverage demand drops. Platforms should plan stock accordingly.

## How to run
pip install pandas numpy matplotlib openpyxl
python blinkit_analysis.py