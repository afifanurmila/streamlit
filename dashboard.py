import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Title of the dashboard
st.title("E-commerce Dashboard")

# Add a header
st.header("Welcome to my Streamlit App")

# Add some text
st.write("This is a simple dashboard created using Streamlit.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("df_data.csv", parse_dates=["shipping_limit_date"])
    return df

df = load_data()

# Preprocessing
df["year_month"] = df["shipping_limit_date"].dt.to_period("M")

# Streamlit UI
st.title("📈 Analisis Tren Waktu Pengiriman")

# Hitung jumlah order per bulan
order_trend = df["year_month"].value_counts().sort_index().reset_index()
order_trend.columns = ["year_month", "jumlah_order"]

# Konversi Period ke String untuk Plotly
order_trend["year_month"] = order_trend["year_month"].astype(str)

# Plot menggunakan Plotly
fig = px.line(order_trend, x="year_month", y="jumlah_order", 
              markers=True, title="Tren Pengiriman per Bulan",
              labels={"year_month": "Tahun-Bulan", "jumlah_order": "Jumlah Order"},
              line_shape="linear")

fig.update_traces(line=dict(color="purple"))
fig.update_layout(xaxis_tickangle=-45)

# Tampilkan plot di Streamlit
st.plotly_chart(fig)

# Sidebar Filter
st.sidebar.header("Filter")
selected_category = st.sidebar.selectbox("Pilih Kategori Produk:", df["product_category_name_english"].dropna().unique())

# Filter data berdasarkan kategori
df_filtered = df[df["product_category_name_english"] == selected_category]

# 2️⃣ **Distribusi Kategori Produk**
st.subheader("📊 Distribusi Kategori Produk")
df_category = df["product_category_name_english"].value_counts().reset_index()
df_category.columns = ["category", "count"]
fig_category = px.bar(df_category, x="count", y="category", orientation="h", title="Distribusi Kategori Produk")
st.plotly_chart(fig_category)

# 3️⃣ **Distribusi Harga Produk**
st.subheader("💰 Distribusi Harga Produk")
fig_price = px.histogram(df_filtered, x="price", nbins=50, title=f"Distribusi Harga - {selected_category}")
st.plotly_chart(fig_price)

st.caption('Copyright (C) Afifa Nur Mila 2025')