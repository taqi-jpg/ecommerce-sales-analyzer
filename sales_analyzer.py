import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# Load the generated data
df = pd.read_csv("data/sales_data.csv")
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# 1. Monthly Sales Trend (Bar Chart)
plt.figure(figsize=(10, 5))
df['Month'] = df['Order_Date'].dt.strftime('%Y-%m')  # Format: "2023-01"
monthly_sales = df.groupby('Month')['Sales'].sum()
monthly_sales.plot(kind='bar', color='skyblue')
plt.title("Monthly Sales (2023)")
plt.xlabel("Month")
plt.ylabel("Total Sales ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('assets/monthly_sales.png')  # Save the chart

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