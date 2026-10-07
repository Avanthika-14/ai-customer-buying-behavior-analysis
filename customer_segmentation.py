"""
Task 2: Customer Segmentation using K-Means Clustering
Uses the dataset created earlier: blinkit_orders.csv
Run: python customer_segmentation.py
Needs: pandas, numpy, matplotlib, scikit-learn
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)
# STEP 1: Load the dataset (created in Task 1)
df = pd.read_csv("blinkit_orders.csv", parse_dates=["order_date"])
print(f"Loaded {len(df)} rows, {df.customer_id.nunique()} unique customers\n")
# STEP 2: Build customer-level features
order_level = df.groupby(["customer_id", "order_id"])["item_total"].sum().reset_index()
customer_features = order_level.groupby("customer_id").agg(
    total_orders=("order_id", "nunique"),
    total_spend=("item_total", "sum"),
    avg_order_value=("item_total", "mean"),
).reset_index()
customer_features["avg_order_value"] = customer_features["avg_order_value"].round(2)
print("=== Sample customer features ===")
print(customer_features.head(), "\n")
# STEP 3: Scale features
features = ["total_orders", "total_spend", "avg_order_value"]
X = customer_features[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# STEP 4: Elbow Method to find best k
inertia = []
k_range = range(1, 9)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertia.append(km.inertia_)
plt.figure(figsize=(7, 4))
plt.plot(list(k_range), inertia, marker="o")
plt.xlabel("Number of clusters (k)")
plt.ylabel("Inertia")
plt.title("Elbow Method for Optimal k")
plt.tight_layout()
plt.savefig("chart_elbow_method.png", dpi=150)
plt.close()
print("Saved chart_elbow_method.png\n")
# STEP 5: Run K-Means with k=4
k = 4
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
customer_features["cluster"] = kmeans.fit_predict(X_scaled)
# STEP 6: Label clusters
cluster_summary = customer_features.groupby("cluster")[features].mean().round(2)
cluster_summary["customer_count"] = customer_features["cluster"].value_counts().sort_index()
print("=== Cluster summary (raw) ===")
print(cluster_summary, "\n")
ranked = cluster_summary.sort_values("total_spend", ascending=False).index.tolist()
label_names = ["High Spenders", "Frequent Buyers", "Occasional Buyers", "Rare Buyers"]
label_map = {cluster_id: label_names[i] for i, cluster_id in enumerate(ranked)}
customer_features["segment"] = customer_features["cluster"].map(label_map)
cluster_summary["segment"] = cluster_summary.index.map(label_map)
print("=== Cluster summary (labeled) ===")
print(cluster_summary, "\n")
print("=== Customers per segment ===")
print(customer_features["segment"].value_counts(), "\n")
# STEP 7: Save results
customer_features.to_csv("customer_segments.csv", index=False)
print("Saved customer_segments.csv\n")
# STEP 8: Visualize
colors = {"High Spenders": "green", "Frequent Buyers": "blue",
          "Occasional Buyers": "orange", "Rare Buyers": "red"}
plt.figure(figsize=(8, 6))
for seg, group in customer_features.groupby("segment"):
    plt.scatter(group["total_orders"], group["total_spend"],
                label=seg, alpha=0.6, s=25, color=colors.get(seg))
plt.xlabel("Total Orders")
plt.ylabel("Total Spend (Rs.)")
plt.title("Customer Segments (K-Means Clustering)")
plt.legend()
plt.tight_layout()
plt.savefig("chart_customer_segments.png", dpi=150)
plt.close()
plt.figure(figsize=(6, 6))
customer_features["segment"].value_counts().plot.pie(autopct="%1.1f%%", colors=[colors[s] for s in customer_features["segment"].value_counts().index])
plt.ylabel("")
plt.title("Customer Segment Distribution")
plt.tight_layout()
plt.savefig("chart_segment_pie.png", dpi=150)
plt.close()
print("Saved chart_customer_segments.png and chart_segment_pie.png")
print("\nDONE.")