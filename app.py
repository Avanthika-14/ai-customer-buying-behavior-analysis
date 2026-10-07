from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from datetime import datetime

SEGMENT_FILE = "customer_segments.csv"

segments_df = pd.read_csv(SEGMENT_FILE)
DEMAND_FILE = "demand_prediction.csv"
demand_df = pd.read_csv(DEMAND_FILE)

app = Flask(__name__)
app.secret_key = "ai_customer_analytics_secret"

# Customer activity tracking
customer_activity = {}

# Customer cart
customer_cart = {}

# Customer orders
customer_orders = []

DATA_FILE = "blinkit_orders.csv"

df = pd.read_csv(DATA_FILE)

df["order_date"] = pd.to_datetime(df["order_date"])

@app.route("/customer-login", methods=["GET", "POST"])
def customer_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        if email == "customer@gmail.com" and password == "customer123":

            session["customer_logged_in"] = True
            session["customer_email"] = email
            session["customer_id"] = 1

            # Record customer login activity
            customer_activity[email] = {
                "customer_id": 1,
                "email": email,
                "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "Online"
            }

            return redirect(url_for("customer_dashboard"))

        return render_template(
            "customer_login.html",
            error="Invalid email or password"
        )

    return render_template("customer_login.html")

@app.route("/products")
def products():

    if not session.get("customer_logged_in"):
        return redirect(url_for("customer_login"))

    products_data = (
        df[["product", "category"]]
        .dropna()
        .drop_duplicates()
        .sort_values("product")
    )

    products = products_data.to_dict("records")

    categories = sorted(
        df["category"].dropna().unique().tolist()
    )

    return render_template(
        "products.html",
        products=products,
        categories=categories
    )

@app.route("/product/<product_name>")
def product_details(product_name):

    if not session.get("customer_logged_in"):
        return redirect(url_for("customer_login"))

    # Selected product data
    product_data = df[
        df["product"] == product_name
    ].copy()

    if product_data.empty:
        return "Product not found"

    # Product statistics
    total_quantity = int(product_data["quantity"].sum())
    total_customers = int(product_data["customer_id"].nunique())
    average_price = float(product_data["unit_price"].mean())

    return render_template(
        "product_details.html",
        product_name=product_name,
        total_quantity=total_quantity,
        total_customers=total_customers,
        average_price=average_price
    )

@app.route("/add-to-cart/<product_name>", methods=["POST"])
def add_to_cart(product_name):

    if not session.get("customer_logged_in"):
        return redirect(url_for("customer_login"))

    email = session.get("customer_email")

    if email not in customer_cart:
        customer_cart[email] = []

    customer_cart[email].append({
        "product": product_name,
        "quantity": 1
    })

    return redirect(url_for("cart"))

@app.route("/cart")
def cart():

    if not session.get("customer_logged_in"):
        return redirect(url_for("customer_login"))

    email = session.get("customer_email")

    cart_items = customer_cart.get(email, [])

    return render_template(
        "cart.html",
        cart_items=cart_items
    )

@app.route("/place-order", methods=["POST"])
def place_order():

    if not session.get("customer_logged_in"):
        return redirect(url_for("customer_login"))

    email = session.get("customer_email")
    customer_id = session.get("customer_id")

    cart_items = customer_cart.get(email, [])

    if not cart_items:
        return redirect(url_for("cart"))

    order_id = "ORD" + datetime.now().strftime("%Y%m%d%H%M%S")

    order = {
        "order_id": order_id,
        "customer_id": customer_id,
        "email": email,
        "items": cart_items.copy(),
        "order_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Placed"
    }

    customer_orders.append(order)

    # Clear cart after purchase
    customer_cart[email] = []

    return render_template(
        "order_success.html",
        order=order
    )

@app.route("/remove-from-cart/<int:item_index>", methods=["POST"])
def remove_from_cart(item_index):

    if not session.get("customer_logged_in"):
        return redirect(url_for("customer_login"))

    email = session.get("customer_email")

    cart_items = customer_cart.get(email, [])

    if 0 <= item_index < len(cart_items):
        cart_items.pop(item_index)

    return redirect(url_for("cart"))

@app.route("/customer-dashboard")
def customer_dashboard():

    if not session.get("customer_logged_in"):
        return redirect(url_for("customer_login"))

    customer_id = 1

    customer = segments_df[
        segments_df["customer_id"] == customer_id
    ]

    if customer.empty:
        return render_template("customer_dashboard.html")

    customer = customer.iloc[0]

    # Customer order history
    customer_orders = df[
        df["customer_id"] == customer_id
    ].copy()

    customer_orders["order_date"] = (
        customer_orders["order_date"].dt.strftime("%Y-%m-%d")
    )

    orders = customer_orders.to_dict("records")

    return render_template(
        "customer_dashboard.html",
        customer_id=int(customer["customer_id"]),
        total_orders=int(customer["total_orders"]),
        total_spend=float(customer["total_spend"]),
        avg_order_value=float(customer["avg_order_value"]),
        segment=customer["segment"],
        orders=orders
    )

@app.route("/customer-logout")
def customer_logout():

    email = session.get("customer_email")

    if email in customer_activity:
        customer_activity[email]["status"] = "Offline"

    session.pop("customer_logged_in", None)
    session.pop("customer_email", None)
    session.pop("customer_id", None)

    return redirect(url_for("customer_login"))

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        if email == "admin@gmail.com" and password == "admin123":

            session["admin_logged_in"] = True

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid email or password"
        )

    return render_template("login.html")
@app.route("/")
def dashboard():
    if not session.get("admin_logged_in"):
      return redirect(url_for("login"))

    # Overall metrics
    total_orders = int(df["order_id"].nunique())
    total_customers = int(df["customer_id"].nunique())
    total_revenue = float(df["item_total"].sum())

    order_revenue = df.groupby("order_id")["item_total"].sum()
    average_order_value = order_revenue.mean()

    # Find available months
    months = sorted(
        df["order_date"].dt.to_period("M").unique()
    )

    this_month = months[-1]

    if len(months) >= 2:
        last_month = months[-2]
    else:
        last_month = months[-1]

    # Last month
    last_df = df[
        df["order_date"].dt.to_period("M") == last_month
    ]

    last_orders = int(last_df["order_id"].nunique())
    last_customers = int(last_df["customer_id"].nunique())
    last_revenue = float(last_df["item_total"].sum())

    # This month
    this_df = df[
        df["order_date"].dt.to_period("M") == this_month
    ]

    this_orders = int(this_df["order_id"].nunique())
    this_customers = int(this_df["customer_id"].nunique())
    this_revenue = float(this_df["item_total"].sum())

    # Average Order Value

    last_order_revenue = last_df.groupby("order_id")["item_total"].sum()
    last_aov = last_order_revenue.mean()

    this_order_revenue = this_df.groupby("order_id")["item_total"].sum()
    this_aov = this_order_revenue.mean()
        # -----------------------------
    # Category-wise Analysis
    # -----------------------------

    category_sales = (
        df.groupby("category")["item_total"]
        .sum()
        .sort_values(ascending=False)
    )

    category_names = category_sales.index.tolist()
    category_values = [float(x) for x in category_sales.values]

        # -----------------------------
    # Customer Segmentation
    # -----------------------------

    segment_counts = (
        segments_df["segment"]
        .value_counts()
    )

    segment_names = segment_counts.index.tolist()
    segment_values = [int(x) for x in segment_counts.values]
        # -----------------------------
    # Demand Prediction
    # -----------------------------

    demand_categories = demand_df["category"].tolist()
    predicted_demand = [float(x) for x in demand_df["predicted_next_month"]]

    return render_template(
        "dashboard.html",

        total_orders=total_orders,
        total_customers=total_customers,
        total_revenue=total_revenue,
        average_order_value=average_order_value,

        last_month=str(last_month),
        this_month=str(this_month),

        last_orders=last_orders,
        this_orders=this_orders,

        last_customers=last_customers,
        this_customers=this_customers,

        last_revenue=last_revenue,
        this_revenue=this_revenue,

        last_aov=last_aov,
        this_aov=this_aov,

        category_names=category_names,
        category_values=category_values,

        demand_categories=demand_categories,
        predicted_demand=predicted_demand,

        segment_names=segment_names,
        segment_values=segment_values,

        customer_activity=list(customer_activity.values()),

        active_customers=sum(
            1
            for customer in customer_activity.values()
            if customer["status"] == "Online"
        ),

        total_customer_logins=len(customer_activity),
                customer_orders=customer_orders
    )

@app.route("/ai-insights")
def ai_insights():
    return render_template("ai_insights.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/customers")
def customers():
    return render_template("customers.html", customers=segments_df.to_dict("records"))

@app.route("/segmentation")
def segmentation():
    segment_counts = segments_df["segment"].value_counts()

    segment_names = segment_counts.index.tolist()
    segment_values = [int(x) for x in segment_counts.values]

    return render_template(
        "segmentation.html",
        segment_names=segment_names,
        segment_values=segment_values
    )

@app.route("/month-comparison")
def month_comparison():
    months = sorted(df["order_date"].dt.to_period("M").unique())

    this_month = months[-1]

    if len(months) >= 2:
        last_month = months[-2]
    else:
        last_month = months[-1]

    last_df = df[
        df["order_date"].dt.to_period("M") == last_month
    ]

    this_df = df[
        df["order_date"].dt.to_period("M") == this_month
    ]

    last_orders = int(last_df["order_id"].nunique())
    this_orders = int(this_df["order_id"].nunique())

    last_customers = int(last_df["customer_id"].nunique())
    this_customers = int(this_df["customer_id"].nunique())

    last_revenue = float(last_df["item_total"].sum())
    this_revenue = float(this_df["item_total"].sum())

    return render_template(
        "month_comparison.html",
        last_orders=last_orders,
        this_orders=this_orders,
        last_customers=last_customers,
        this_customers=this_customers,
        last_revenue=last_revenue,
        this_revenue=this_revenue
    )

@app.route("/demand-prediction")
def demand_prediction():
    demand_categories = demand_df["category"].tolist()
    predicted_demand = [
        float(x) for x in demand_df["predicted_next_month"]
    ]

    return render_template(
        "demand_prediction.html",
        demand_categories=demand_categories,
        predicted_demand=predicted_demand
    )

if __name__ == "__main__":
    app.run(debug=True)