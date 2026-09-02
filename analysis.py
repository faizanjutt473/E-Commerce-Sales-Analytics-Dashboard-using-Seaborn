"""
Advanced Seaborn Visualization Project
Dataset: clean_final_data.csv (E-commerce orders)

4 different graph types:
1. Heatmap        -> Category vs City average Sales
2. Violin Plot    -> Sales distribution by Customer Segment
3. Bar Plot       -> Total Sales by Category (with Payment Method breakdown)
4. Line Plot      -> Monthly Sales trend over time
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# 1. Load & prepare data

df = pd.read_csv("clean_final_data.csv")

df["OrderDate"] = pd.to_datetime(df["OrderDate"])
df["Month"] = df["OrderDate"].dt.to_period("M").dt.to_timestamp()

# Only keep completed orders for "clean" revenue analysis
completed = df[df["Status"] == "Completed"].copy()


# 2. Style setup

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.dpi"] = 110

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("E-Commerce Sales Analysis Dashboard", fontsize=18, fontweight="bold", y=1.02)


# Graph 1: Heatmap -> Category vs City average Sales

pivot = completed.pivot_table(
    index="Category", columns="City", values="Sales", aggfunc="mean"
)
sns.heatmap(
    pivot, annot=True, fmt=".0f", cmap="YlGnBu",
    linewidths=0.5, ax=axes[0, 0], cbar_kws={"label": "Avg Sales"}
)
axes[0, 0].set_title("Average Sales: Category vs City", fontsize=13, fontweight="bold")
axes[0, 0].set_xlabel("City")
axes[0, 0].set_ylabel("Category")


# Graph 2: Violin Plot -> Sales distribution by Customer Segment

sns.violinplot(
    data=completed, x="CustomerSegment", y="Sales",
    hue="CustomerSegment", palette="magma", ax=axes[0, 1], legend=False
)
axes[0, 1].set_title("Sales Distribution by Customer Segment", fontsize=13, fontweight="bold")
axes[0, 1].set_xlabel("Customer Segment")
axes[0, 1].set_ylabel("Sales")
axes[0, 1].set_ylim(0, completed["Sales"].quantile(0.98))  # trim extreme outliers for clarity


# Graph 3: Bar Plot -> Total Sales by Category, split by Payment Method

cat_pay = (
    completed.groupby(["Category", "PaymentMethod"])["Sales"]
    .sum()
    .reset_index()
)
sns.barplot(
    data=cat_pay, x="Category", y="Sales", hue="PaymentMethod",
    palette="Set2", ax=axes[1, 0]
)
axes[1, 0].set_title("Total Sales by Category & Payment Method", fontsize=13, fontweight="bold")
axes[1, 0].set_xlabel("Category")
axes[1, 0].set_ylabel("Total Sales")
axes[1, 0].tick_params(axis="x", rotation=30)
axes[1, 0].legend(title="Payment Method", fontsize=8)


# Graph 4: Line Plot -> Monthly Sales trend

monthly = completed.groupby("Month")["Sales"].sum().reset_index()
sns.lineplot(
    data=monthly, x="Month", y="Sales",
    marker="o", linewidth=2.5, color="darkorange", ax=axes[1, 1]
)
axes[1, 1].set_title("Monthly Sales Trend", fontsize=13, fontweight="bold")
axes[1, 1].set_xlabel("Month")
axes[1, 1].set_ylabel("Total Sales")
axes[1, 1].tick_params(axis="x", rotation=45)


# Save

plt.tight_layout()
plt.savefig("sales_dashboard.png", bbox_inches="tight")
print("Saved: sales_dashboard.png")
