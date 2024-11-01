import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

most_product_sales_df = pd.read_csv("data_pembelian.csv")
most_customers_df = pd.read_csv("data_pelanggan.csv")
data_orders_df = pd.read_csv("data_pengiriman.csv")
data_sales_df = pd.read_csv("data_penjualan.csv")

def create_most_product_sales_df(df):
    most_sales_df = df.groupby("product_category_name").order_id.nunique().sort_values(ascending=False).reset_index()
    most_sales_df.rename(columns={"order_id":"order_count"}, inplace=True)
    return most_sales_df

def create_most_city_customers_df(df):
    most_city_customers_df = df.groupby("customer_city").customer_id.nunique().sort_values(ascending=False).reset_index()
    most_city_customers_df.rename(columns={"customer_id":"customer_count"}, inplace=True)
    return most_city_customers_df

def create_most_state_customers_df(df):
    most_state_customers_df = df.groupby("customer_state").customer_id.nunique().sort_values(ascending=False).reset_index()
    most_state_customers_df.rename(columns={"customer_id":"customer_count"}, inplace=True)
    return most_state_customers_df

def create_order_year_df(df):
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    year_orders_df = df.resample(rule='Y', on='order_purchase_timestamp').agg({
        "order_id": "nunique"
    })
    
    year_orders_df = year_orders_df.reset_index()
    year_orders_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    return year_orders_df

def create_most_price_df(df):
    most_expensive_product_df = df.groupby("product_category_name").agg({
        "product_id" : "nunique",
        "price" : "max"
    }).sort_values("price", ascending=False).reset_index()
    return most_expensive_product_df

most_sales_df = create_most_product_sales_df(most_product_sales_df)
most_city_customers_df = create_most_city_customers_df(most_customers_df)
most_state_customers_df = create_most_state_customers_df(most_customers_df)
year_orders_df = create_order_year_df(data_orders_df)
most_expensive_product_df = create_most_price_df(data_sales_df)

st.header('E-Commerce Dashboard :sparkles:')

st.subheader("Best & Worst Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="order_count", y="product_category_name", data = most_sales_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=35)
ax[0].tick_params(axis ='x', labelsize=30)

sns.barplot(x="order_count", y="product_category_name", data = most_sales_df.sort_values(by="order_count", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=50)

st.pyplot(fig)

st.subheader("Customer Demographics")

fig, ax = plt.subplots(figsize=(35, 15))

sns.barplot(
    x = "customer_city",
    y = "customer_count",
    data = most_city_customers_df.head(5).sort_values(by="customer_count", ascending=False),
    palette = colors, ax = ax
)

ax.set_title("Number of Customer by City", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=50)
ax.tick_params(axis='y', labelsize=50)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(35, 15))

sns.barplot(
    x = "customer_state",
    y = "customer_count",
    data = most_state_customers_df.head(5).sort_values(by="customer_count", ascending=False),
    palette = colors, ax = ax
)

ax.set_title("Number of Customer by State", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=50)
ax.tick_params(axis='y', labelsize=50)

st.pyplot(fig)

st.subheader("Customer Growth")

fig, ax = plt.subplots(figsize=(35, 15))

ax.plot(
    year_orders_df["order_purchase_timestamp"], 
    year_orders_df["order_count"], 
    marker='o', 
    linewidth=2, 
    color="#72BCD4"
)
ax.set_title("Number of Orders Years", loc="center", fontsize=50)
ax.tick_params(axis='x', labelsize=50)
ax.tick_params(axis='y', labelsize=50)

st.pyplot(fig)

st.subheader("Ranking of the Cheapest and Most Expensive Items")

fig, ax = plt.subplots(figsize=(10, 50))

ax.hlines(y=most_expensive_product_df['product_category_name'], xmin=0, xmax=most_expensive_product_df['price'], color='skyblue')

ax.plot(most_expensive_product_df['price'], most_expensive_product_df['product_category_name'], "o", markersize=8, color='blue')

ax.set_title('Product Price Ranking')
ax.set_xlabel('Price')
ax.set_ylabel('Product')

st.pyplot(fig)