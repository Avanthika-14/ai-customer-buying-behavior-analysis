"""
Task 4: Demand Prediction using Linear Regression
Predicts next month's (October) revenue per category based on the
daily trend seen across Aug-Sep in blinkit_orders.csv.
Run: python demand_prediction.py
Needs: pandas, numpy, matplotlib, scikit-learn
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
 
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)
 
# ---------------------------------------------------------------
# STEP 1: Load data, build a daily revenue series per category
# ---------------------------------------------------------------
df = pd.read_csv("blinkit_orders.csv", parse_dates=["order_date"])
 
daily = (
    df.groupby(["order_date", "category"])["item_total"]
    .sum()
    .reset_index()
)
 
# Fill in missing (date, category) combos with 0 so the trend line is clean
all_dates = pd.date_range(daily["order_date"].min(), daily["order_date"].max())
all_categories = df["category"].unique()
full_index = pd.MultiIndex.from_product([all_dates, all_categories], names=["order_date", "category"])
daily = daily.set_index(["order_date", "category"]).reindex(full_index, fill_value=0).reset_index()
daily["day_number"] = (daily["order_date"] - daily["order_date"].min()).dt.days
 
last_day = daily["day_number"].max()
future_days = np.arange(last_day + 1, last_day + 31)  # next 30 days = "October"
future_dates = pd.date_range(daily["order_date"].max() + pd.Timedelta(days=1), periods=30)
 
# ---------------------------------------------------------------
# STEP 2: Fit a Linear Regression model PER CATEGORY and predict
# ---------------------------------------------------------------
results = []
plt.figure(figsize=(10, 6))
 
for category in all_categories:
    cat_data = daily[daily["category"] == category]
    X = cat_data[["day_number"]].values
    y = cat_data["item_total"].values
 
    model = LinearRegression()
    model.fit(X, y)
 
    future_pred = model.predict(future_days.reshape(-1, 1))
    future_pred = np.clip(future_pred, 0, None)  # revenue can't be negative
 
    predicted_next_month_total = future_pred.sum()
    this_month_actual = cat_data[cat_data["order_date"].dt.month == cat_data["order_date"].dt.month.max()]["item_total"].sum()
 
    change_pct = round((predicted_next_month_total - this_month_actual) / this_month_actual * 100, 2)
    results.append({
        "category": category,
        "this_month_actual": round(this_month_actual, 2),
        "predicted_next_month": round(predicted_next_month_total, 2),
        "predicted_change_%": change_pct,
        "trend_slope": round(model.coef_[0], 2),  # positive = growing, negative = shrinking
    })
 
    plt.plot(cat_data["order_date"], y, alpha=0.4, label=f"{category} (actual)")
    plt.plot(future_dates, future_pred, "--", label=f"{category} (predicted)")
 
results_df = pd.DataFrame(results).sort_values("predicted_change_%", ascending=False)
print("=== Demand Prediction: Next Month vs This Month ===")
print(results_df.to_string(index=False), "\n")
 
results_df.to_csv("demand_prediction.csv", index=False)
print("Saved demand_prediction.csv\n")
 
plt.xlabel("Date")
plt.ylabel("Daily Revenue (Rs.)")
plt.title("Category Revenue Trend: Actual (solid) vs Predicted Next Month (dashed)")
plt.legend(fontsize=7, loc="upper left")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart_demand_prediction.png", dpi=150)
plt.close()
print("Saved chart_demand_prediction.png\n")
 
# ---------------------------------------------------------------
# STEP 3: Simple text insights
# ---------------------------------------------------------------
top_up = results_df.iloc[0]
top_down = results_df.iloc[-1]
print("=== AI Insight ===")
print(f"Next month, '{top_up['category']}' is predicted to grow by {top_up['predicted_change_%']}% "
      f"-> consider increasing stock.")
print(f"'{top_down['category']}' is predicted to change by {top_down['predicted_change_%']}% "
      f"-> monitor closely / plan promotions if declining.")