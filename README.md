# AI Customer Buying Behavior Analysis

A Flask-based web application that analyzes customer purchasing behavior and provides data-driven insights into customer segments, product demand, monthly performance, and buying patterns.

The system combines **Python, Flask, Pandas, Machine Learning, HTML, CSS, JavaScript, and Chart.js** to provide an interactive analytics dashboard for administrators and a personalized shopping experience for customers.

## Key Features

* **Admin Dashboard** – Overview of orders, customers, revenue, and average order value.
* **Customer Segmentation** – Groups customers based on purchasing behavior such as Rare Buyers, Occasional Buyers, High Spenders, and Frequent Buyers.
* **Demand Prediction** – Analyzes product-category demand and provides predicted demand insights.
* **Month Comparison** – Compares monthly revenue and order performance.
* **AI Insights** – Generates data-driven insights from customer and sales patterns.
* **Customer Dashboard** – Displays personalized customer information and purchase history.
* **Product Browsing** – Customers can search and filter products by category.
* **Product Details** – Provides product-level purchase statistics.
* **Shopping Cart** – Allows customers to add products and manage their cart.
* **Order Management** – Supports customer purchase flow and order confirmation.
* **Reports** – Presents important business analytics in an easy-to-understand format.

## Technologies Used

* **Frontend:** HTML, CSS, JavaScript, Chart.js
* **Backend:** Python, Flask
* **Data Analysis:** Pandas
* **Machine Learning:** Customer Segmentation and Demand Prediction
* **Data Storage:** CSV
* **Development Tool:** VS Code
* **Version Control:** Git & GitHub

## Run it in VS Code

1. Clone the repository:

```bash
git clone https://github.com/Avanthika-14/ai-customer-buying-behavior-analysis.git
```

2. Open the project folder in VS Code.

3. Open the VS Code terminal:

```text
Ctrl + `
```

4. Create a virtual environment:

```bash
python -m venv venv
```

5. Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

6. Install the required packages:

```bash
pip install flask pandas
```

7. Run the Flask application:

```bash
python app.py
```

8. Open the application in your browser:

```text
http://127.0.0.1:5000/
```

## Project Structure

```text
ai-customer-buying-behavior-analysis/
│
├── app.py
├── blinkit_orders.csv
├── customer_segments.csv
├── demand_prediction.csv
│
├── blinkit_analysis.py
├── customer_segmentation.py
├── demand_prediction.py
├── monthly_ai_insights.py
├── dashboard.py
├── setup_database.py
│
├── analysis_results.xlsx
├── monthly_ai_insights.txt
│
├── chart_category_change.png
├── chart_customer_segments.png
├── chart_demand_prediction.png
├── chart_elbow_method.png
├── chart_hourly_orders.png
├── chart_segment_pie.png
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── customers.html
│   ├── segmentation.html
│   ├── month_comparison.html
│   ├── demand_prediction.html
│   ├── ai_insights.html
│   ├── reports.html
│   ├── customer_login.html
│   ├── customer_dashboard.html
│   ├── products.html
│   ├── product_details.html
│   ├── cart.html
│   └── order_success.html
│
└── static/
    └── css/
        ├── style.css
        ├── login.css
        └── js/
            └── dashboard.js
```

## Customer Segmentation

The application analyzes customer purchasing behavior using metrics such as:

* Total Orders
* Total Spending
* Average Order Value
* Purchase Frequency

Customers are categorized into meaningful segments:

* **Rare Buyers**
* **Occasional Buyers**
* **High Spenders**
* **Frequent Buyers**

These segments help identify different customer behaviors and support better business decisions.

## Demand Prediction

The demand prediction module analyzes historical order data to estimate future demand across product categories.

The system provides:

* Predicted demand
* Category-level analysis
* Demand trends
* Month-over-month comparison

This can help businesses plan inventory and understand changing customer demand.

## Admin & Customer Modules

### Admin

The administrator can:

* View business KPIs
* Analyze customers
* View customer segments
* Compare monthly performance
* View demand predictions
* Access AI-generated insights
* View reports

### Customer

Customers can:

* Log in
* View their dashboard
* Browse products
* Search products
* Filter products by category
* View product details
* Add products to cart
* Complete purchases
* View order information

## Objective

The main objective of this project is to transform customer transaction data into meaningful business insights using data analysis and machine learning while providing an interactive web-based analytics platform.

## Future Enhancements

* Real-time customer activity tracking
* Database integration using MySQL or PostgreSQL
* Advanced recommendation system
* Real-time demand forecasting
* Personalized product recommendations
* Cloud deployment
* Enhanced authentication and authorization
* Interactive business intelligence reports

## Author

**Avanthika V**

AI Customer Buying Behavior Analysis
Built using Python, Flask, Pandas & Machine Learning.
