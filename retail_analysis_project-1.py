"""
Real-World Data Project: Retail Sales Analysis
Dataset: UCI Online Retail
Source: https://archive.ics.uci.edu/dataset/352/online+retail

Run after downloading "Online Retail.xlsx" from UCI.
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("Online Retail.xlsx")
df["InvoiceNo"] = df["InvoiceNo"].astype(str)

# 1) Basic cleaning
df = df.drop_duplicates()
cancelled = df[df["InvoiceNo"].str.startswith("C")].copy()
sales = df[~df["InvoiceNo"].str.startswith("C")].copy()

sales = sales[sales["Quantity"] > 0]
sales = sales[sales["UnitPrice"] > 0]

# 2) Feature engineering
sales["Revenue"] = sales["Quantity"] * sales["UnitPrice"]
sales["YearMonth"] = sales["InvoiceDate"].dt.to_period("M").astype(str)
sales["Weekday"] = sales["InvoiceDate"].dt.day_name()
sales["Hour"] = sales["InvoiceDate"].dt.hour

# 3) KPIs
print("Revenue:", round(sales["Revenue"].sum(), 2))
print("Invoices:", sales["InvoiceNo"].nunique())
print("SKUs:", sales["StockCode"].nunique())
print("Customers:", sales["CustomerID"].nunique())
print("AOV:", round(sales.groupby("InvoiceNo")["Revenue"].sum().mean(), 2))

# 4) Monthly revenue
monthly = sales.groupby("YearMonth")["Revenue"].sum()
monthly.plot(kind="line", marker="o", title="Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5) Top countries
country = sales.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(10)
country.plot(kind="bar", title="Top 10 Countries by Revenue")
plt.ylabel("Revenue (£)")
plt.tight_layout()
plt.show()

# 6) Top products
product = sales.groupby("Description")["Revenue"].sum().sort_values(ascending=False).head(10)
product.sort_values().plot(kind="barh", title="Top 10 Products by Revenue")
plt.xlabel("Revenue (£)")
plt.tight_layout()
plt.show()

# 7) Customer concentration
customer = sales.dropna(subset=["CustomerID"]).groupby("CustomerID")["Revenue"].sum().sort_values(ascending=False)
customer_share = customer.cumsum() / customer.sum() * 100
print("Customers needed for 80% of identified revenue:",
      int((customer_share < 80).sum()) + 1)

# 8) Cancellation summary
cancelled["CancelledValue"] = cancelled["Quantity"].abs() * cancelled["UnitPrice"]
print("Cancelled invoices:", cancelled["InvoiceNo"].nunique())
print("Cancelled value:", round(cancelled["CancelledValue"].sum(), 2))

print("\nProject complete.")
