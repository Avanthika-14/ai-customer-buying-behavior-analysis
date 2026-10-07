"""
Task 3: Month-over-Month AI Analysis
Generates automatic insight sentences from the last-month vs this-month comparison.
Uses: blinkit_orders.csv (created in Task 1)
Run: python monthly_ai_insights.py
"""
import pandas as pd
import numpy as np
 
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)
 
# ---------------------------------------------------------------
# STEP 1: Load data
# ---------------------------------------------------------------
df = pd.read_csv("blinkit_orders.csv", parse_dates=["order_date"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)
last_m, this_m = sorted(df["month"].unique())
print(f"Comparing LAST MONTH = {last_m}  vs  THIS MONTH = {this_m}\n")
 
# ---------------------------------------------------------------
# STEP 2: Category-wise change % (same as Task 1)
# ---------------------------------------------------------------
cat = df.pivot_table(index="category", columns="month", values="item_total",
                      aggfunc="sum", fill_value=0)
cat["change_%"] = ((cat[this_m] - cat[last_m]) / cat[last_m] * 100).round(2)
 
# ---------------------------------------------------------------
# STEP 3: Rule-based AI classification of each category
# (this is the "AI logic" - decision rules based on % change)
# ---------------------------------------------------------------
def classify(change):
    if change >= 50:
        return "Strong Growth"
    elif change >= 15:
        return "Moderate Growth"
    elif change >= -15:
        return "Stable"
    elif change >= -50:
        return "Moderate Decline"
    else:
        return "Strong Decline"
 
def reason(category, change, label):
    # simple rule-based "why" explanation - swap in your own domain reasoning
    festive_categories = ["Sweets & Festive", "Personal Care"]
    if label in ("Strong Growth", "Moderate Growth") and category in festive_categories:
        return "likely driven by festival season demand"
    elif label in ("Strong Growth", "Moderate Growth"):
        return "showing rising customer interest"
    elif label in ("Strong Decline", "Moderate Decline") and category == "Beverages":
        return "possibly due to seasonal/weather-related drop in demand"
    elif label in ("Strong Decline", "Moderate Decline"):
        return "showing reduced customer interest"
    else:
        return "demand remained largely consistent"
 
cat["ai_label"] = cat["change_%"].apply(classify)
cat["reason"] = [reason(c, v, l) for c, v, l in zip(cat.index, cat["change_%"], cat["ai_label"])]
cat = cat.sort_values("change_%", ascending=False)
 
print("=== AI-Classified Category Analysis ===")
print(cat[[last_m, this_m, "change_%", "ai_label", "reason"]], "\n")
 
# ---------------------------------------------------------------
# STEP 4: Flag significant anomalies (|change| >= 20%)
# ---------------------------------------------------------------
anomalies = cat[cat["change_%"].abs() >= 20]
print("=== Significant Anomalies (|change| >= 20%) ===")
print(anomalies[[last_m, this_m, "change_%", "ai_label"]], "\n")
 
# ---------------------------------------------------------------
# STEP 5: Auto-generate plain-English insight sentences
# ---------------------------------------------------------------
insights = []
insights.append(f"Month-over-Month AI Analysis: {last_m} (last month) vs {this_m} (this month)\n")
 
total_last = df[df.month == last_m]["item_total"].sum()
total_this = df[df.month == this_m]["item_total"].sum()
overall_change = round((total_this - total_last) / total_last * 100, 2)
insights.append(f"Overall revenue changed by {overall_change}% month-over-month "
                 f"(Rs.{total_last:.0f} -> Rs.{total_this:.0f}).\n")
 
for category, row in cat.iterrows():
    sentence = (f"- {category}: {row['change_%']}% change -> {row['ai_label']} "
                f"({row['reason']}).")
    insights.append(sentence)
 
insights.append("\nTop priority actions:")
top_growth = cat.iloc[0]
top_decline = cat.iloc[-1]
insights.append(f"- Increase stock for '{cat.index[0]}' (up {top_growth['change_%']}%) "
                 f"to avoid running out.")
insights.append(f"- Investigate '{cat.index[-1]}' (down {abs(top_decline['change_%'])}%) "
                 f"and consider promotions or discounts.")
 
report_text = "\n".join(insights)
print(report_text)
 
with open("monthly_ai_insights.txt", "w", encoding="utf-8") as f:
    f.write(report_text)
 
print("\n\nSaved monthly_ai_insights.txt (paste this into your report)")