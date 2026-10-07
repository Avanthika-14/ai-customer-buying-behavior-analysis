import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

# ---------- STEP 1: Create Blinkit-style dataset (Aug = last month, Sep = this month) ----------
catalog = {
    "Dairy": [("Milk 500ml", 30), ("Curd 400g", 45), ("Paneer 200g", 90), ("Butter 100g", 58)],
    "Snacks": [("Lays Chips", 20), ("Kurkure", 20), ("Biscuits", 30), ("Namkeen 200g", 60)],
    "Beverages": [("Cold Drink 750ml", 40), ("Packaged Juice 1L", 110), ("Energy Drink", 125), ("Tea 250g", 120)],
    "Fruits & Vegetables": [("Tomato 1kg", 40), ("Onion 1kg", 35), ("Banana 1 dozen", 60), ("Apple 1kg", 180)],
    "Staples": [("Rice 5kg", 380), ("Atta 5kg", 250), ("Toor Dal 1kg", 160), ("Sunflower Oil 1L", 140)],
    "Personal Care": [("Shampoo 340ml", 220), ("Toothpaste", 95), ("Soap 4pk", 150), ("Face Wash", 180)],
    "Sweets & Festive": [("Laddu Box", 250), ("Dry Fruits 500g", 550), ("Chocolates Box", 300), ("Pooja Kit", 120)],
}
categories = list(catalog.keys())

weights = {
    "2026-08": [0.18, 0.16, 0.20, 0.18, 0.12, 0.08, 0.08],
    "2026-09": [0.19, 0.15, 0.13, 0.17, 0.14, 0.08, 0.14],
}
orders_per_month = {"2026-08": 4000, "2026-09": 4400}
hour_w = np.array([1, 1, 1, 1, 1, 2, 3, 6, 8, 7, 5, 5, 6, 6, 5, 4, 5, 6, 8, 9, 9, 7, 4, 2], dtype=float)
hour_w /= hour_w.sum()
payments = ["UPI", "Card", "COD", "Wallet"]
cities = ["Madurai", "Chennai", "Coimbatore", "Trichy"]

rows = []
order_id = 1
for month, n_orders in orders_per_month.items():
    year, mon = map(int, month.split("-"))
    days = 31 if mon == 8 else 30
    for _ in range(n_orders):
        cust = int(rng.integers(1, 1501))
        date = pd.Timestamp(year, mon, int(rng.integers(1, days + 1)))
        hour = int(rng.choice(24, p=hour_w))
        pay = str(rng.choice(payments, p=[0.55, 0.2, 0.15, 0.1]))
        city = str(rng.choice(cities, p=[0.3, 0.35, 0.2, 0.15]))
        for _ in range(int(rng.integers(1, 6))):
            cat = str(rng.choice(categories, p=weights[month]))
            product, price = catalog[cat][int(rng.integers(0, 4))]
            qty = int(rng.integers(1, 4))
            rows.append([order_id, cust, date, hour, city, cat, product, qty, price, qty * price, pay])
        order_id += 1

cols = ["order_id", "customer_id", "order_date", "order_hour", "city",
        "category", "product", "quantity", "unit_price", "item_total", "payment_method"]
df = pd.DataFrame(rows, columns=cols)
df.to_csv("blinkit_orders.csv", index=False)
print(f"Dataset created: {len(df)} rows, {df.order_id.nunique()} orders\n")

# ---------- STEP 2: Data cleaning ----------
df = pd.read_csv("blinkit_orders.csv", parse_dates=["order_date"])
print("Missing values:\n", df.isnull().sum(), "\n")
df = df.drop_duplicates()
df["month"] = df["order_date"].dt.to_period("M").astype(str)
last_m, this_m = sorted(df["month"].unique())
print(f"Comparing  LAST MONTH = {last_m}  vs  THIS MONTH = {this_m}\n")

# ---------- STEP 3: Overall comparison ----------
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)
order_totals = df.groupby(["month", "order_id"])["item_total"].sum().reset_index()
summary = pd.DataFrame({
    "total_orders": df.groupby("month")["order_id"].nunique(),
    "unique_customers": df.groupby("month")["customer_id"].nunique(),
    "total_revenue": df.groupby("month")["item_total"].sum(),
    "avg_order_value": order_totals.groupby("month")["item_total"].mean().round(2),
    "items_sold": df.groupby("month")["quantity"].sum(),
})
summary.loc["change_%"] = ((summary.loc[this_m] - summary.loc[last_m]) / summary.loc[last_m] * 100).round(2)
print("=== OVERALL SUMMARY ===\n", summary, "\n")

# ---------- STEP 4: Category-wise comparison ----------
cat = df.pivot_table(index="category", columns="month", values="item_total", aggfunc="sum", fill_value=0)
cat["change_%"] = ((cat[this_m] - cat[last_m]) / cat[last_m] * 100).round(2)
cat["trend"] = np.where(cat["change_%"] > 0, "UP", "DOWN")
cat = cat.sort_values("change_%", ascending=False)
print("=== CATEGORY-WISE CHANGE ===\n", cat, "\n")

# ---------- STEP 5: Product-wise comparison ----------
prod = df.pivot_table(index="product", columns="month", values="quantity", aggfunc="sum", fill_value=0)
prod["change_%"] = ((prod[this_m] - prod[last_m]) / prod[last_m] * 100).round(2)
prod = prod.sort_values("change_%", ascending=False)
print("=== TOP 5 PRODUCTS BOUGHT MORE ===\n", prod.head(5), "\n")
print("=== TOP 5 PRODUCTS BOUGHT LESS ===\n", prod.tail(5), "\n")

# ---------- STEP 6: Buying behavior ----------
hourly = df.groupby(["order_hour", "month"])["order_id"].nunique().unstack(fill_value=0)
print("Peak ordering hour:", hourly.idxmax().to_dict(), "\n")

orders_per_cust = df.groupby(["month", "customer_id"])["order_id"].nunique().reset_index()
print("Avg orders per customer:\n", orders_per_cust.groupby("month")["order_id"].mean().round(2), "\n")

pay = df.groupby(["month", "payment_method"])["order_id"].nunique().unstack(0)
print("Payment method usage:\n", pay, "\n")

# ---------- STEP 7: Charts + save ----------
colors = ["green" if v > 0 else "red" for v in cat["change_%"]]
plt.figure(figsize=(9, 5))
plt.barh(cat.index, cat["change_%"], color=colors)
plt.axvline(0, color="black", linewidth=0.8)
plt.xlabel("Change in revenue (%)")
plt.title(f"Category-wise Change: {last_m} vs {this_m}")
plt.tight_layout()
plt.savefig("chart_category_change.png", dpi=150)
plt.close()

hourly.plot(figsize=(9, 4), marker="o")
plt.xlabel("Hour of day")
plt.ylabel("Orders")
plt.title("Orders by Hour: Last Month vs This Month")
plt.tight_layout()
plt.savefig("chart_hourly_orders.png", dpi=150)
plt.close()

with pd.ExcelWriter("analysis_results.xlsx") as xw:
    summary.to_excel(xw, sheet_name="overall")
    cat.to_excel(xw, sheet_name="category_change")
    prod.to_excel(xw, sheet_name="product_change")
print("Saved: blinkit_orders.csv, analysis_results.xlsx, chart_category_change.png, chart_hourly_orders.png")