import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import streamlit as st
import plotly.express as px


# Load the generated data
df = pd.read_csv("data/sales_data.csv")
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# 1. # 📅 Monthly Sales (Improved)
st.subheader("📅 Monthly Sales (2023)")

# Convert Order_Date if not already done
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# Extract month names
df['Month'] = df['Order_Date'].dt.strftime('%B')  # January, February, etc.

# Order the months properly
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
monthly_sales = df.groupby('Month')['Sales'].sum().reindex(month_order)

# Plot

# Optional: Convert numeric month to month names
month_map = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
    5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}
monthly_sales.index = monthly_sales.index.map(month_map)

# Bonus Plotly Chart
fig = px.bar(
    monthly_sales.reset_index(),
    x='Month', y='Sales',
    title="📅 Monthly Sales (2023)",
    labels={'Sales': 'Total Sales'},
    color='Sales',
    color_continuous_scale='Blues'
)
st.plotly_chart(fig)


# 2. Top Selling Products (Pie Chart)
plt.figure(figsize=(8, 8))
top_products = df['Product'].value_counts().head(5)
top_products.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title("Top 5 Products by Sales Volume")
plt.savefig('assets/top_products.png')

# 3. Generate PDF Report
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=16)
pdf.cell(200, 10, txt="E-Commerce Sales Report", ln=1, align='C')

# Add charts to PDF
pdf.image('assets/monthly_sales.png', x=10, y=30, w=180)
pdf.image('assets/top_products.png', x=10, y=120, w=180)

# Add summary stats
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt=f"Total Revenue: ${df['Sales'].sum():,.2f}", ln=2)
pdf.cell(200, 10, txt=f"Total Orders: {len(df)}", ln=3)
pdf.cell(200, 10, txt=f"Time Period: {df['Order_Date'].min().date()} to {df['Order_Date'].max().date()}", ln=4)

# Save PDF
pdf.output("sales_report.pdf")
print("✅ Generated: monthly_sales.png, top_products.png, sales_report.pdf")