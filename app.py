import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px

# Load data
df = pd.read_csv("data/sales_data.csv")

st.title("📊 E-Commerce Sales Analyzer")

# Show raw data
if st.checkbox("Show raw data"):
    st.write(df)

# Product-wise sales count
st.subheader("🛒 Product Sales Distribution")
fig, ax = plt.subplots()
df['Product'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)
ax.axis('equal')
st.pyplot(fig)

# Save chart (optional)
os.makedirs("assets", exist_ok=True)
fig.savefig("assets/product_sales.png")

st.subheader("📅 Monthly Sales (2023)")

# Convert Order Date to datetime if not already
df['Order_Date'] = pd.to_datetime(df['Order_Date'])


# Group by month
monthly_sales = df.groupby(df['Order_Date'].dt.month)['Sales'].sum()

# Plot
fig2, ax2 = plt.subplots()
monthly_sales.plot(kind='bar', ax=ax2)
ax2.set_xlabel("Month")
ax2.set_ylabel("Sales")
ax2.set_title("Monthly Sales")
st.pyplot(fig2)

# Sidebar filters
st.sidebar.header("🔎 Filter Data")
product_list = df['Product'].unique()
selected_product = st.sidebar.selectbox("Choose a product", options=product_list)

# 📝 Log product filter selection
if not os.path.exists("user_logs.csv"):
    with open("user_logs.csv", "w") as f:
        f.write("Timestamp,Action,Value\n")

with open("user_logs.csv", "a") as f:
    now = pd.Timestamp.now()
    f.write(f"{now},Product Filter,{selected_product}\n")

# Filtered Data
filtered_df = df[df['Product'] == selected_product]
# 📥 Download Filtered Data
st.subheader("⬇️ Download Filtered Data as CSV")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='filtered_sales_data.csv',
    mime='text/csv',
)


st.write(f"Showing results for **{selected_product}**")
st.dataframe(filtered_df)

# 📊 Top 5 Products by Total Sales
st.subheader("🏆 Top 5 Products by Total Sales")
top_products = df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(5).reset_index()

fig_top = px.bar(
    top_products,
    x="Product",
    y="Sales",
    color="Product",
    text="Sales",
    title="Top 5 Products by Total Sales",
)
fig_top.update_layout(xaxis_title="Product", yaxis_title="Sales", showlegend=False)
st.plotly_chart(fig_top)

# 📈 Monthly Average Sales per Product
st.subheader("📉 Monthly Average Sales per Product")

df['Month'] = df['Order_Date'].dt.strftime('%B')  # Month names
df['Month'] = pd.Categorical(df['Month'], categories=[
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
], ordered=True)

monthly_avg = df.groupby(['Month', 'Product'])['Sales'].mean().reset_index()

fig_avg = px.line(
    monthly_avg,
    x="Month",
    y="Sales",
    color="Product",
    markers=True,
    title="Monthly Average Sales per Product"
)
fig_avg.update_layout(xaxis_title="Month", yaxis_title="Avg Sales")
st.plotly_chart(fig_avg)
