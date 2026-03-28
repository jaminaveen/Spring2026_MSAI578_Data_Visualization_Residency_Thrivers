"""
PROJECT 2: E-Commerce Business Analytics
Group Project - Starter Code (Python)
Saturday: 9.5 hours work time

TEAM INFORMATION:
Team Name: Thrivers
Members:
1. Naveen Jami (Role: Data Engineer)
2. Vikranth Reddy Gurram (Role: Analyst 1)
3. Yiming Liu (Role: Analyst 2)
4. Shishir Khanal (Role: Visualization Specialist)
5. Chiranjeevi Pinapati (Role: Communications Lead)

DELIVERABLES CHECKLIST:
[ ] Dashboard (HTML/Notebook)
[ ] PowerPoint Presentation (10-15 slides)
[ ] Technical Report (4-6 pages)
[ ] Clean code with README
[ ] All 10 analyses complete
"""

# ==============================================================================
# SETUP & IMPORTS
# ==============================================================================

import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Output folder for all HTML figures
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set styles
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

# Professional color palette
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'info': '#17becf'
}

print("="*70)
print(" "*20 + "E-COMMERCE ANALYTICS PROJECT")
print("="*70)
print(f"Team: Thrivers")
print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)

# ==============================================================================
# DATA LOADING
# ==============================================================================

print("\n📊 LOADING DATA...")

# Load the main dataset
# NOTE: Update the file path to where you saved the data
folder_path = "data/"
file_path = os.path.join(folder_path, "Online Retail.xlsx")  # UPDATE THIS PATH

try:
    df = pd.read_excel(file_path)
    print(f"✓ Data loaded successfully: {df.shape[0]:,} rows × {df.shape[1]} columns")
except FileNotFoundError:
    print("❌ Error: Data file not found!")
    print("Please download from: https://archive.ics.uci.edu/ml/datasets/Online+Retail")
    print("Or check your file path")

# Display basic info
print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

# ==============================================================================
# DATA EXPLORATION
# ==============================================================================

print("\n"  + "="*70)
print(" "*25 + "DATA EXPLORATION")
print("="*70)

print("\n📈 BASIC STATISTICS:")
print(f"Total Transactions: {df['InvoiceNo'].nunique():,}")
print(f"Unique Products: {df['StockCode'].nunique():,}")
print(f"Unique Customers: {df['CustomerID'].nunique():,}")
print(f"Countries: {df['Country'].nunique():,}")
print(f"Date Range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")

print("\n❓ MISSING VALUES:")
print(df.isnull().sum())

print("\n💰 PRICE STATISTICS:")
print(df['UnitPrice'].describe())

print("\n📦 QUANTITY STATISTICS:")
print(df['Quantity'].describe())

# ==============================================================================
# DATA CLEANING
# ==============================================================================

print("\n" + "="*70)
print(" "*25 + "DATA CLEANING")
print("="*70)

# Create a copy for cleaning
df_clean = df.copy()

# 1. Convert InvoiceDate to datetime
df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
print("✓ Converted InvoiceDate to datetime")

# 2. Create calculated fields
df_clean['TotalPrice'] = df_clean['Quantity'] * df_clean['UnitPrice']
print("✓ Created TotalPrice column")

# 3. Extract time components
df_clean['Year'] = df_clean['InvoiceDate'].dt.year
df_clean['Month'] = df_clean['InvoiceDate'].dt.month
df_clean['MonthName'] = df_clean['InvoiceDate'].dt.month_name()
df_clean['Day'] = df_clean['InvoiceDate'].dt.day
df_clean['DayOfWeek'] = df_clean['InvoiceDate'].dt.day_name()
df_clean['Hour'] = df_clean['InvoiceDate'].dt.hour
df_clean['Date'] = df_clean['InvoiceDate'].dt.date
print("✓ Extracted time components")

# 4. TODO: Handle missing CustomerID [Completed]
# Decision: How do you want to handle transactions without CustomerID?
# Option A: Remove them
# Option B: Keep them but exclude from customer-specific analyses
# Option C: Create a "Guest" category

# YOUR DECISION HERE:
# DECISION: Option B + C hybrid
#   - These are legitimate transactions (guest checkouts) — revenue is real
#   - We keep them in df_clean for revenue/product/trend analyses
#   - We flag them as 'Guest' so customer-specific analyses like Customer Behavior, Cohort Analysis can exclude them
#   - Removing them (Option A) would undercount total revenue and sales volume
print("-" * 50)
print("TODO 4: Handling missing CustomerID")
print("-" * 50)
missing_customer = df_clean['CustomerID'].isnull().sum()
print(f"Rows with missing CustomerID: {missing_customer:,} ({missing_customer/len(df_clean)*100:.1f}% of data)")

# Fill missing CustomerID with 'Guest' label
df_clean['CustomerID'] = df_clean['CustomerID'].fillna('Guest')
print(f"✓ Missing CustomerID filled with 'Guest'")

# Add a flag column so analysts can filter these out easily and also analyze them separately if desired
df_clean['IsGuest'] = (df_clean['CustomerID'] == 'Guest').astype(int)
print(f"✓ Added IsGuest flag column (1 = guest, 0 = registered customer)")
customer_specific_analyses_data = df_clean[df_clean['IsGuest']==0].reset_index(drop=True)

# Verify
print(f"\nVerification:")
print(f"  Remaining NaN in CustomerID : {df_clean['CustomerID'].isnull().sum()}")
print(f"  Guest rows                  : {df_clean['IsGuest'].sum():,}")
print(f"  Registered customer rows    : {(df_clean['IsGuest'] == 0).sum():,}")
print(f"\n For customer-specific analyses (RFM, CLV, cohorts): filter with df_clean[df_clean['IsGuest']==0]")




# 5. TODO: Handle negative quantities (returns/cancellations) [Completed]
# Decision: How do you want to handle returns?
# Option A: Remove all negative quantities
# Option B: Create separate returns dataset
# Option C: Keep them for return analysis

# YOUR DECISION HERE:
# DECISION: Option B
#   - Negative quantities and C-prefix invoices are returns/cancellations
#   - They contain valuable signal for Analysis 8 (Returns & Cancellations)
#   - We create two clear sub-datasets: `sales` and `returns`
#   - df_clean itself keeps ALL rows — analysts choose the subset they need
#   - Option A would hide the return signal entirely
print("-" * 50)
print("TODO 5: Handling negative quantities (returns/cancellations)")
print("-" * 50)
df_clean['IsReturn']       = (df_clean['Quantity'] < 0).fillna(False)
df_clean['IsCancellation'] = df_clean['InvoiceNo'].str.startswith('C').fillna(False)

neg_qty_count  = df_clean['IsReturn'].sum()
cancel_count   = df_clean['IsCancellation'].sum()
print(f"Negative quantity rows  : {neg_qty_count:,}")
print(f"C-prefix invoice rows   : {cancel_count:,}")
print(f"Either flag (union)     : {(df_clean['IsReturn'] | df_clean['IsCancellation']).sum():,}")

# Create separate sub-datasets (Option B)
# `sales`   — forward sales only: positive qty, no C-prefix invoices
# `returns` — any row that is a return or cancellation
sales   = df_clean[~df_clean['IsReturn'] & ~df_clean['IsCancellation']].copy()
returns = df_clean[df_clean['IsReturn']  |  df_clean['IsCancellation']].copy()

print(f"\n✓ Created sub-datasets:")
print(f"  sales   : {len(sales):,}   rows  — forward transactions only")
print(f"  returns : {len(returns):,}   rows  — returns & cancellations")
print(f"\n💡 Usage guide:")
print(f"  Use `customer_specific_analyses_data` (CustomerID != 'Guest') for customer behavior, CLV, cohorts")
print(f"  Use `sales`   for revenue totals, product sales, customer CLV")
print(f"  Use `returns` for Analysis 8 (returns analysis)")
print(f"  Use `df_clean` (all rows) when you need both, e.g. total volume")



# 6. TODO: Handle outliers in price and quantity [completed]
# Check for unusual values and decide how to handle
# APPROACH:
#   - Zero / negative UnitPrice rows = non-product adjustments → REMOVE
#   - Extreme UnitPrice outliers (>99.9th percentile) → FLAG, keep in data
#   - Extreme Quantity outliers → FLAG, keep (bulk B2B orders are legitimate)
# YOUR CODE HERE:
print("-" * 50)
print("TODO 6: Handling outliers")
print("-" * 50)

before = len(df_clean)

# Step 7 (from starter code) — remove invalid (zero/negative) unit prices
df_clean = df_clean[df_clean['UnitPrice'] > 0].copy()
print(f"Removed {before - len(df_clean):,} rows with UnitPrice ≤ 0")

# Recalculate TotalPrice after removals (values may have changed)
df_clean['TotalPrice'] = df_clean['Quantity'] * df_clean['UnitPrice']

# Flag extreme UnitPrice outliers (>99.9th percentile) — not removing, just flagging for analysts to consider
price_99 = df_clean['UnitPrice'].quantile(0.999)
df_clean['IsPriceOutlier'] = df_clean['UnitPrice'] > price_99
print(f"Flagged {df_clean['IsPriceOutlier'].sum():,} extreme price outliers (UnitPrice > £{price_99:.2f}) — kept in data")

# Flag extreme Quantity outliers similarly 
qty_99 = df_clean['Quantity'].abs().quantile(0.999)
df_clean['IsQtyOutlier'] = df_clean['Quantity'].abs() > qty_99
print(f"Flagged {df_clean['IsQtyOutlier'].sum():,} extreme quantity outliers (|Qty| > {qty_99:.0f}) — kept in data")

print(f"\n✓ CLEANED DATA: {df_clean.shape[0]:,} rows × {df_clean.shape[1]} columns")

# Rebuild sales / returns from the now-fully-cleaned df_clean
sales   = df_clean[~df_clean['IsReturn'] & ~df_clean['IsCancellation']].copy()
returns = df_clean[df_clean['IsReturn']  |  df_clean['IsCancellation']].copy()
print(f"\nRebuilt sub-datasets after outlier removal:")
print(f"  sales   : {len(sales):,} rows")
print(f"  returns : {len(returns):,} rows")

print(f"\nFINAL COLUMN REFERENCE:")
print(f"  df_clean columns: {list(df_clean.columns)}")



# 7. Remove invalid prices (if any)
df_clean = df_clean[df_clean['UnitPrice'] > 0]
print(f"✓ Removed {len(df) - len(df_clean):,} rows with invalid prices")

print(f"\n✓ CLEANED DATA: {df_clean.shape[0]:,} rows × {df_clean.shape[1]} columns")

# ==============================================================================
# ANALYSIS 1: SALES OVERVIEW & TRENDS
# ==============================================================================

print("\n" + "="*70)
print(" "*20 + "ANALYSIS 1: SALES OVERVIEW & TRENDS")
print("="*70)

# Calculate key metrics
total_revenue = df_clean['TotalPrice'].sum()
total_transactions = df_clean['InvoiceNo'].nunique()
total_customers = df_clean['CustomerID'].nunique()
avg_order_value = df_clean.groupby('InvoiceNo')['TotalPrice'].sum().mean()

print(f"\n💰 TOTAL REVENUE: ${total_revenue:,.2f}")
print(f"🛒 TOTAL TRANSACTIONS: {total_transactions:,}")
print(f"👥 TOTAL CUSTOMERS: {total_customers:,}")
print(f"💵 AVERAGE ORDER VALUE: ${avg_order_value:,.2f}")

# Monthly revenue trend
monthly_revenue = df_clean.groupby(df_clean['InvoiceDate'].dt.to_period('M'))['TotalPrice'].sum()
monthly_revenue.index = monthly_revenue.index.to_timestamp()

fig1 = px.line(
    x=monthly_revenue.index,
    y=monthly_revenue.values,
    title='Monthly Revenue Trend',
    labels={'x': 'Month', 'y': 'Revenue ($)'},
    markers=True
)
fig1.update_layout(height=500)
fig1.show()
fig1.write_html(os.path.join(OUTPUT_DIR, "analysis1_monthly_revenue.html"))

# TODO: Add more trend visualizations
# - Weekly trends
# - Growth rate calculation
# - Seasonal patterns
print("-" * 50)
print("[Charts open in your browser]Weekly revenue trend")
print("-" * 50)
# ── TODO: Weekly revenue trend ───────────────────────────────────────────────
weekly_revenue = sales.groupby(sales['InvoiceDate'].dt.to_period('W'))['TotalPrice'].sum()
weekly_revenue.index = weekly_revenue.index.to_timestamp()
weekly_ma4 = weekly_revenue.rolling(4, min_periods=1).mean()

fig1b = go.Figure()
fig1b.add_trace(go.Scatter(x=weekly_revenue.index, y=weekly_revenue.values,
                           mode='lines', name='Weekly Revenue',
                           line=dict(color=COLORS['primary'], width=1), opacity=0.5))
fig1b.add_trace(go.Scatter(x=weekly_ma4.index, y=weekly_ma4.values,
                           mode='lines', name='4-Week Moving Avg',
                           line=dict(color=COLORS['danger'], width=2.5)))
fig1b.update_layout(title='Weekly Revenue Trend (with 4-Week Moving Average)',
                    xaxis_title='Week', yaxis_title='Revenue ($)', height=480)
fig1b.show()
fig1b.write_html(os.path.join(OUTPUT_DIR, "analysis1_weekly_revenue.html"))

# ── TODO: Growth rate calculation ────────────────────────────────────────────
print("-" * 50)
print("[Charts open in your browser]Growth rate calculation")
print("-" * 50)
monthly_revenue_s = sales.groupby(sales['InvoiceDate'].dt.to_period('M'))['TotalPrice'].sum()
monthly_df = monthly_revenue_s.reset_index()
monthly_df.columns = ['YearMonth', 'Revenue']
monthly_df['YearMonth_str']  = monthly_df['YearMonth'].astype(str)
monthly_df['MoM_Growth_Pct'] = monthly_df['Revenue'].pct_change() * 100
monthly_df['Rolling_3M_Avg'] = monthly_df['Revenue'].rolling(3, min_periods=1).mean()

avg_growth = monthly_df['MoM_Growth_Pct'].dropna().mean()
print(f"📈 Average Month-over-Month Growth Rate: {avg_growth:.1f}%")
print(f"\nMonthly Revenue + Growth Rate:")
print(monthly_df[['YearMonth_str', 'Revenue', 'MoM_Growth_Pct']].to_string(index=False))

fig1c = make_subplots(specs=[[{"secondary_y": True}]])
fig1c.add_trace(go.Bar(x=monthly_df['YearMonth_str'], y=monthly_df['Revenue'],
                       name='Revenue ($)', marker_color=COLORS['primary'], opacity=0.7),
                secondary_y=False)
fig1c.add_trace(go.Scatter(x=monthly_df['YearMonth_str'], y=monthly_df['MoM_Growth_Pct'],
                           name='MoM Growth (%)', mode='lines+markers',
                           line=dict(color=COLORS['success'], width=2)),
                secondary_y=True)
fig1c.update_layout(title='Monthly Revenue with Month-over-Month Growth Rate',
                    height=500, xaxis_title='Month')
fig1c.update_yaxes(title_text='Revenue ($)', secondary_y=False)
fig1c.update_yaxes(title_text='Growth Rate (%)', secondary_y=True)
fig1c.show()
fig1c.write_html(os.path.join(OUTPUT_DIR, "analysis1_growth_rate.html"))

# ── TODO: Seasonal patterns (quarterly) ──────────────────────────────────────
print("-" * 50)
print("[Charts open in your browser]Seasonal patterns (quarterly)")
print("-" * 50)
# .rename() gives each groupby key a distinct name so reset_index() doesn't conflict
seasonal = (
    sales.groupby([
        sales['InvoiceDate'].dt.year.rename('Year'),
        sales['InvoiceDate'].dt.quarter.rename('Quarter')
    ])['TotalPrice']
    .sum()
    .reset_index()
)
seasonal['Period'] = 'Q' + seasonal['Quarter'].astype(str) + ' ' + seasonal['Year'].astype(str)

fig1d = px.bar(seasonal, x='Period', y='TotalPrice',
               title='Seasonal Revenue by Quarter',
               labels={'TotalPrice': 'Revenue ($)', 'Period': 'Quarter'},
               text_auto='.2s')
fig1d.update_traces(textposition='outside')
fig1d.update_layout(height=450)
fig1d.show()
fig1d.write_html(os.path.join(OUTPUT_DIR, "analysis1_seasonal.html"))

# ── Peak period identification ────────────────────────────────────────────────
peak_month = monthly_df.loc[monthly_df['Revenue'].idxmax(), 'YearMonth_str']
peak_rev   = monthly_df['Revenue'].max()
dow_rev    = sales.groupby('DayOfWeek')['TotalPrice'].sum().reindex(
                ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
best_day   = dow_rev.idxmax()
best_hour  = sales.groupby('Hour')['TotalPrice'].sum().idxmax()

print(f"\n🏆 PEAK PERIODS:")
print(f"  Peak Month    : {peak_month}  (${peak_rev:,.2f})")
print(f"  Best Day      : {best_day}")
print(f"  Peak Hour     : {best_hour:02d}:00")
print(f"  Q4 vs Q1 lift : {seasonal[seasonal['Quarter']==4]['TotalPrice'].mean() / seasonal[seasonal['Quarter']==1]['TotalPrice'].mean():.1f}x")

print("✓ Analysis 1 complete")

# ==============================================================================
# ANALYSIS 2: PRODUCT PERFORMANCE
# ==============================================================================

print("\n" + "="*70)
print(" "*20 + "ANALYSIS 2: PRODUCT PERFORMANCE")
print("="*70)

# Top 10 products by quantity
top_products_qty = df_clean.groupby('Description')['Quantity'].sum().nlargest(10)

fig2a = px.bar(
    x=top_products_qty.values,
    y=top_products_qty.index,
    orientation='h',
    title='Top 10 Best-Selling Products (by Quantity)',
    labels={'x': 'Quantity Sold', 'y': 'Product'},
    color=top_products_qty.values,
    color_continuous_scale='Blues'
)
fig2a.update_layout(height=500, showlegend=False)
fig2a.show()
fig2a.write_html(os.path.join(OUTPUT_DIR, "analysis2_top_products_quantity.html"))

# Top 10 products by revenue
top_products_rev = df_clean.groupby('Description')['TotalPrice'].sum().nlargest(10)

fig2b = px.bar(
    x=top_products_rev.values,
    y=top_products_rev.index,
    orientation='h',
    title='Top 10 Products by Revenue',
    labels={'x': 'Revenue ($)', 'y': 'Product'},
    color=top_products_rev.values,
    color_continuous_scale='Greens'
)
fig2b.update_layout(height=500, showlegend=False)
fig2b.show()
fig2b.write_html(os.path.join(OUTPUT_DIR, "analysis2_top_products_revenue.html"))

# TODO: Additional product analyses
# - Price vs sales volume
# - Underperforming products
# - Product category analysis (if you create categories)



print("✓ Analysis 2 complete")


# ==============================================================================
# ANALYSIS 3: CUSTOMER BEHAVIOR
# ==============================================================================

print("\n" + "="*70)
print(" "*20 + "ANALYSIS 3: CUSTOMER BEHAVIOR")
print("="*70)

# Customer purchase frequency
customer_freq = df_clean.groupby('CustomerID')['InvoiceNo'].nunique()

print(f"\n📊 CUSTOMER PURCHASE FREQUENCY:")
print(f"One-time buyers: {(customer_freq == 1).sum():,} ({(customer_freq == 1).sum()/len(customer_freq)*100:.1f}%)")
print(f"Repeat customers: {(customer_freq > 1).sum():,} ({(customer_freq > 1).sum()/len(customer_freq)*100:.1f}%)")
print(f"Average purchases per customer: {customer_freq.mean():.2f}")

# Distribution of purchase frequency
fig3a = px.histogram(
    customer_freq,
    nbins=50,
    title='Distribution of Customer Purchase Frequency',
    labels={'value': 'Number of Purchases', 'count': 'Number of Customers'}
)
fig3a.update_layout(height=500)
fig3a.write_html(os.path.join(OUTPUT_DIR, "analysis3_purchase_frequency.html"))

# Customer Lifetime Value (CLV)
customer_clv = df_clean.groupby('CustomerID')['TotalPrice'].sum().sort_values(ascending=False)

print(f"\n💰 TOP 10 CUSTOMERS BY CLV:")
print(customer_clv.head(10))

# TODO: Additional customer analyses
# - Customer segmentation (RFM analysis)
# - New vs returning customer trends
# - Customer retention analysis


# Use only registered customers and positive transactions for customer-specific analyses
customer_df = df_clean[(df_clean['IsGuest'] == 0) & (df_clean['Quantity'] > 0)].copy()

# - Customer segmentation (RFM analysis)

snapshot_date = customer_df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = (
    customer_df.groupby('CustomerID')
    .agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum'
    })
    .reset_index()
)

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

rfm['R_Score'] = pd.qcut(rfm['Recency'].rank(method='first'), 4, labels=[4, 3, 2, 1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 4, labels=[1, 2, 3, 4]).astype(int)

def segment_customer(row):
    if row['R_Score'] >= 3 and row['F_Score'] >= 3 and row['M_Score'] >= 3:
        return 'Champions'
    elif row['R_Score'] >= 3 and row['F_Score'] >= 2:
        return 'Loyal Customers'
    elif row['R_Score'] == 4 and row['F_Score'] == 1:
        return 'New Customers'
    elif row['R_Score'] <= 2 and row['F_Score'] >= 3:
        return 'At Risk'
    elif row['R_Score'] <= 2 and row['F_Score'] <= 2:
        return 'Lost'
    else:
        return 'Potential Loyalists'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)
segment_counts = rfm['Segment'].value_counts()

print(f"\n🎯 CUSTOMER SEGMENTS:")
print(segment_counts)

fig3b = px.bar(
    x=segment_counts.index,
    y=segment_counts.values,
    title='Customer Segmentation (RFM)',
    labels={'x': 'Segment', 'y': 'Number of Customers'},
    color=segment_counts.values,
    color_continuous_scale='Viridis'
)
fig3b.update_layout(height=500, showlegend=False)
fig3b.write_html(os.path.join(OUTPUT_DIR, "analysis3_rfm_segments.html"))

# - New vs returning customer trends
customer_first_purchase = customer_df.groupby('CustomerID')['InvoiceDate'].min().dt.to_period('M')
new_customers_by_month = customer_first_purchase.value_counts().sort_index()
new_customers_by_month.name = 'NewCustomers'

monthly_customer_activity = (
    customer_df.assign(YearMonth=customer_df['InvoiceDate'].dt.to_period('M'))
    .groupby('YearMonth')['CustomerID']
    .nunique()
)
monthly_customer_activity.name = 'ActiveCustomers'

customer_trend = pd.concat(
    [new_customers_by_month, monthly_customer_activity],
    axis=1
).fillna(0)

customer_trend['ReturningCustomers'] = (
    customer_trend['ActiveCustomers'] - customer_trend['NewCustomers']
).clip(lower=0)

customer_trend = customer_trend.rename_axis('YearMonth').reset_index()
customer_trend['YearMonth'] = customer_trend['YearMonth'].astype(str)

fig3c = go.Figure()
fig3c.add_trace(go.Bar(
    x=customer_trend['YearMonth'],
    y=customer_trend['NewCustomers'],
    name='New Customers'
))
fig3c.add_trace(go.Bar(
    x=customer_trend['YearMonth'],
    y=customer_trend['ReturningCustomers'],
    name='Returning Customers'
))
fig3c.update_layout(
    barmode='stack',
    title='New vs Returning Customers by Month',
    xaxis_title='Month',
    yaxis_title='Number of Customers',
    height=500
)
fig3c.write_html(os.path.join(OUTPUT_DIR, "analysis3_new_vs_returning.html"))

# - Customer retention analysis

retention_summary = pd.DataFrame({
    'CustomerID': customer_df.groupby('CustomerID')['InvoiceNo'].nunique().index,
    'PurchaseCount': customer_df.groupby('CustomerID')['InvoiceNo'].nunique().values
})

retention_summary['Retained'] = np.where(
    retention_summary['PurchaseCount'] > 1,
    'Repeat',
    'One-Time'
)

retention_counts = retention_summary['Retained'].value_counts()

print(f"\n🔁 CUSTOMER RETENTION SUMMARY:")
print(retention_counts)

fig3d = px.pie(
    names=retention_counts.index,
    values=retention_counts.values,
    title='One-Time vs Repeat Customers'
)
fig3d.update_layout(height=500)
fig3d.write_html(os.path.join(OUTPUT_DIR, "analysis3_retention_summary.html"))

print("✓ Analysis 3 complete")


# ==============================================================================
# ANALYSIS 4: GEOGRAPHIC ANALYSIS
# ==============================================================================

print("\n" + "="*70)
print(" "*20 + "ANALYSIS 4: GEOGRAPHIC ANALYSIS")
print("="*70)

# Revenue by country
country_revenue = df_clean.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False)

print(f"\n🌍 TOP 10 COUNTRIES BY REVENUE:")
for i, (country, revenue) in enumerate(country_revenue.head(10).items(), 1):
    print(f"{i}. {country}: ${revenue:,.2f}")

# Visualize top countries
fig4a = px.bar(
    x=country_revenue.head(15).values,
    y=country_revenue.head(15).index,
    orientation='h',
    title='Top 15 Countries by Revenue',
    labels={'x': 'Revenue ($)', 'y': 'Country'},
    color=country_revenue.head(15).values,
    color_continuous_scale='Viridis'
)
fig4a.update_layout(height=600, showlegend=False)
fig4a.show()
fig4a.write_html(os.path.join(OUTPUT_DIR, "analysis4_country_revenue.html"))

# TODO: Create geographic map visualization
# Hint: Use plotly choropleth or scatter_geo



print("✓ Analysis 4 complete")

# ==============================================================================
# ANALYSIS 5: TIME-BASED PATTERNS
# ==============================================================================

print("\n" + "="*70)
print(" "*20 + "ANALYSIS 5: TIME-BASED PATTERNS")
print("="*70)

# Sales by day of week
dow_revenue = df_clean.groupby('DayOfWeek')['TotalPrice'].sum()
dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dow_revenue = dow_revenue.reindex(dow_order)

fig5a = px.bar(
    x=dow_order,
    y=dow_revenue.values,
    title='Revenue by Day of Week',
    labels={'x': 'Day of Week', 'y': 'Revenue ($)'},
    color=dow_revenue.values,
    color_continuous_scale='Blues'
)
fig5a.update_layout(height=500, showlegend=False)
fig5a.show()
fig5a.write_html(os.path.join(OUTPUT_DIR, "analysis5_day_of_week.html"))

# Sales by hour of day
hour_revenue = df_clean.groupby('Hour')['TotalPrice'].sum()

fig5b = px.line(
    x=hour_revenue.index,
    y=hour_revenue.values,
    title='Revenue by Hour of Day',
    labels={'x': 'Hour', 'y': 'Revenue ($)'},
    markers=True
)
fig5b.update_layout(height=500)
fig5b.show()
fig5b.write_html(os.path.join(OUTPUT_DIR, "analysis5_hour_of_day.html"))

# TODO: Additional time analyses
# - Monthly seasonality
# - Weekend vs weekday
# - Holiday effects (if you identify holidays)



print("✓ Analysis 5 complete")

# ==============================================================================
# ANALYSIS 6: BASKET ANALYSIS
# ==============================================================================

print("\n" + "="*70)
print(" "*20 + "ANALYSIS 6: BASKET ANALYSIS")
print("="*70)

# Calculate basket metrics
basket_size = df_clean.groupby('InvoiceNo')['Quantity'].sum()
basket_value = df_clean.groupby('InvoiceNo')['TotalPrice'].sum()
basket_items = df_clean.groupby('InvoiceNo')['StockCode'].count()

print(f"\n🛒 BASKET STATISTICS:")
print(f"Average items per basket: {basket_items.mean():.2f}")
print(f"Average basket value: ${basket_value.mean():.2f}")
print(f"Median basket value: ${basket_value.median():.2f}")

# Distribution of basket values
fig6 = px.histogram(
    basket_value[basket_value < basket_value.quantile(0.95)],  # Remove top 5% outliers for visibility
    nbins=50,
    title='Distribution of Basket Values (excluding top 5% outliers)',
    labels={'value': 'Basket Value ($)', 'count': 'Frequency'}
)
fig6.update_layout(height=500)
fig6.show()
fig6.write_html(os.path.join(OUTPUT_DIR, "analysis6_basket_distribution.html"))

# TODO: Additional basket analyses
# - Large vs small basket patterns
# - Basket size trends over time



print("✓ Analysis 6 complete")

# ==============================================================================
# ANALYSIS 7: PRICING ANALYSIS
# ==============================================================================

print("\n" + "="*70)
print(" "*20 + "ANALYSIS 7: PRICING ANALYSIS")
print("="*70)

# Price distribution
fig7a = px.histogram(
    df_clean[df_clean['UnitPrice'] < df_clean['UnitPrice'].quantile(0.95)],
    x='UnitPrice',
    nbins=50,
    title='Product Price Distribution (excluding top 5%)',
    labels={'UnitPrice': 'Unit Price ($)'}
)
fig7a.update_layout(height=500)
fig7a.show()
fig7a.write_html(os.path.join(OUTPUT_DIR, "analysis7_price_distribution.html"))

# Revenue by price range
df_clean['PriceRange'] = pd.cut(df_clean['UnitPrice'], 
                                bins=[0, 5, 10, 20, 50, 100, float('inf')],
                                labels=['$0-5', '$5-10', '$10-20', '$20-50', '$50-100', '$100+'])

price_range_revenue = df_clean.groupby('PriceRange')['TotalPrice'].sum()

fig7b = px.bar(
    x=price_range_revenue.index.astype(str),
    y=price_range_revenue.values,
    title='Revenue by Price Range',
    labels={'x': 'Price Range', 'y': 'Revenue ($)'},
    color=price_range_revenue.values,
    color_continuous_scale='Greens'
)
fig7b.update_layout(height=500, showlegend=False)
fig7b.show()
fig7b.write_html(os.path.join(OUTPUT_DIR, "analysis7_price_ranges.html"))

# TODO: Additional pricing analyses
# - Price elasticity insights
# - Optimal price points



print("✓ Analysis 7 complete")

# ==============================================================================
# ANALYSIS 8: RETURNS/CANCELLATIONS
# ==============================================================================

print("\n" + "="*70)
print(" "*20 + "ANALYSIS 8: RETURNS & CANCELLATIONS")
print("="*70)

# Identify returns (negative quantities)
returns = df_clean[df_clean['Quantity'] < 0]
sales = df_clean[df_clean['Quantity'] > 0]

print(f"\n↩️ RETURN STATISTICS:")
print(f"Total return transactions: {returns['InvoiceNo'].nunique():,}")
print(f"Total items returned: {abs(returns['Quantity'].sum()):,.0f}")
print(f"Return rate: {len(returns)/len(df_clean)*100:.2f}%")
print(f"Financial impact: ${abs(returns['TotalPrice'].sum()):,.2f}")

# Top returned products
if len(returns) > 0:
    top_returned = returns.groupby('Description')['Quantity'].sum().nsmallest(10)
    
    fig8 = px.bar(
        x=abs(top_returned.values),
        y=top_returned.index,
        orientation='h',
        title='Top 10 Most Returned Products',
        labels={'x': 'Quantity Returned', 'y': 'Product'},
        color=abs(top_returned.values),
        color_continuous_scale='Reds'
    )
    fig8.update_layout(height=500, showlegend=False)
    fig8.show()
    fig8.write_html(os.path.join(OUTPUT_DIR, "analysis8_top_returns.html"))

# TODO: Additional return analyses
# - Return patterns over time
# - Countries with highest return rates
# ── TODO: Return rate by product ─────────────────────────────────────────────
print("-" * 50)
print("[Charts open in your browser]Return rate by product")
print("-" * 50)
sold_by_product = (sales.groupby(['StockCode','Description'])
                   .agg(qty_sold=('Quantity','sum')).reset_index())
ret_by_product  = (returns.groupby('StockCode')
                   .agg(qty_returned=('Quantity','sum')).reset_index())
ret_by_product['qty_returned_abs'] = ret_by_product['qty_returned'].abs()

product_returns = sold_by_product.merge(
    ret_by_product[['StockCode','qty_returned_abs']], on='StockCode', how='left'
).fillna(0)
product_returns['ReturnRate_Pct'] = (
    product_returns['qty_returned_abs'] / product_returns['qty_sold'] * 100
).clip(upper=100).round(2)
product_returns = product_returns.sort_values('ReturnRate_Pct', ascending=False)

fig8b = px.bar(
    product_returns.head(15),
    x='ReturnRate_Pct', y='Description', orientation='h',
    color='ReturnRate_Pct', color_continuous_scale='Reds',
    title='Top 15 Products by Return Rate (%)',
    labels={'ReturnRate_Pct': 'Return Rate (%)', 'Description': 'Product'},
    text='ReturnRate_Pct'
)
fig8b.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig8b.update_layout(yaxis={'categoryorder':'total ascending'}, height=520,
                    coloraxis_showscale=False)
fig8b.show()
fig8b.write_html(os.path.join(OUTPUT_DIR, "analysis8_return_rate_by_product.html"))

# ── TODO: Return patterns over time ──────────────────────────────────────────
print("-" * 50)
print("[Charts open in your browser]Return patterns over time")
print("-" * 50)
ret_monthly = (returns.groupby(returns['InvoiceDate'].dt.to_period('M'))
               .agg(n_returns=('InvoiceNo','count'), return_value=('TotalPrice','sum'))
               .reset_index())
ret_monthly.columns = ['YearMonth', 'n_returns', 'return_value']
ret_monthly['YearMonth_str']    = ret_monthly['YearMonth'].astype(str)
ret_monthly['return_value_abs'] = ret_monthly['return_value'].abs()

monthly_sales_val = (sales.groupby(sales['InvoiceDate'].dt.to_period('M'))['TotalPrice']
                     .sum().reset_index())
monthly_sales_val.columns = ['YearMonth', 'sales_revenue']
monthly_sales_val['YearMonth_str'] = monthly_sales_val['YearMonth'].astype(str)

ret_vs_sales = ret_monthly.merge(
    monthly_sales_val[['YearMonth_str','sales_revenue']], on='YearMonth_str', how='left'
)
ret_vs_sales['pct_of_sales'] = (
    ret_vs_sales['return_value_abs'] / ret_vs_sales['sales_revenue'] * 100
).round(2)

fig8c = make_subplots(specs=[[{"secondary_y": True}]])
fig8c.add_trace(go.Bar(x=ret_vs_sales['YearMonth_str'], y=ret_vs_sales['return_value_abs'],
                       name='Return Value ($)', marker_color=COLORS['danger'], opacity=0.8),
                secondary_y=False)
fig8c.add_trace(go.Scatter(x=ret_vs_sales['YearMonth_str'], y=ret_vs_sales['pct_of_sales'],
                           name='Returns as % of Sales', mode='lines+markers',
                           line=dict(color=COLORS['secondary'], width=2)),
                secondary_y=True)
fig8c.update_layout(title='Monthly Return Value & Returns as % of Sales',
                    xaxis_title='Month', height=470)
fig8c.update_yaxes(title_text='Return Value ($)', secondary_y=False)
fig8c.update_yaxes(title_text='% of Sales Revenue', secondary_y=True)
fig8c.show()
fig8c.write_html(os.path.join(OUTPUT_DIR, "analysis8_returns_over_time.html"))

# ── TODO: Countries with highest return rates ────────────────────────────────
print("-" * 50)
print("[Charts open in your browser]Countries with highest return rates")
print("-" * 50)
country_sales   = sales.groupby('Country')['Quantity'].sum().rename('qty_sold')
country_returns = returns.groupby('Country')['Quantity'].sum().abs().rename('qty_returned')
country_ret_rate = pd.concat([country_sales, country_returns], axis=1).fillna(0)
country_ret_rate['ReturnRate_Pct'] = (
    country_ret_rate['qty_returned'] / country_ret_rate['qty_sold'] * 100
).clip(upper=100).round(2)
country_ret_rate = (country_ret_rate.reset_index()
                    .sort_values('ReturnRate_Pct', ascending=False).head(15))

fig8d = px.bar(
    country_ret_rate, x='ReturnRate_Pct', y='Country', orientation='h',
    color='ReturnRate_Pct', color_continuous_scale='Oranges',
    title='Countries with Highest Return Rates (%)',
    labels={'ReturnRate_Pct': 'Return Rate (%)', 'Country': ''},
    text='ReturnRate_Pct'
)
fig8d.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig8d.update_layout(yaxis={'categoryorder':'total ascending'}, height=480,
                    coloraxis_showscale=False)
fig8d.show()
fig8d.write_html(os.path.join(OUTPUT_DIR, "analysis8_returns_by_country.html"))

# ── Financial impact summary ──────────────────────────────────────────────────
gross_sales = sales['TotalPrice'].sum()
gross_ret   = returns['TotalPrice'].sum()
net_rev     = gross_sales + gross_ret

print(f"\n Summary ofFINANCIAL IMPACT OF RETURNS:")
print(f"  Gross Sales Revenue : ${gross_sales:>12,.2f}")
print(f"  Gross Return Value  : ${gross_ret:>12,.2f}")
print(f"  Net Revenue         : ${net_rev:>12,.2f}")
print(f"  Return Rate (value) : {abs(gross_ret)/gross_sales*100:.2f}% of gross sales")


print("✓ Analysis 8 complete")


# ==============================================================================
# ANALYSIS 9: COHORT ANALYSIS
# ==============================================================================

print("\n" + "="*70)
print(" "*20 + "ANALYSIS 9: COHORT ANALYSIS")
print("="*70)

# TODO: Complete cohort analysis
# Steps:
# 1. Identify first purchase date for each customer
# 2. Group customers by cohort (month of first purchase)
# 3. Calculate retention rates
# 4. Visualize cohort behavior over time


# Use only registered customers and completed sales
cohort_df = df_clean[(df_clean['IsGuest'] == 0) & (df_clean['Quantity'] > 0)].copy()

# Convert transaction date to month
cohort_df['InvoiceMonth'] = cohort_df['InvoiceDate'].dt.to_period('M').dt.to_timestamp()

# Find first purchase month for each customer
first_purchase = (
    cohort_df.groupby('CustomerID', as_index=False)['InvoiceMonth']
    .min()
    .rename(columns={'InvoiceMonth': 'CohortMonth'})
)

# Attach cohort month to each transaction
cohort_df = cohort_df.merge(first_purchase, on='CustomerID', how='left')

# Calculate months since first purchase
cohort_df['CohortIndex'] = (
    (cohort_df['InvoiceMonth'].dt.year - cohort_df['CohortMonth'].dt.year) * 12
    + (cohort_df['InvoiceMonth'].dt.month - cohort_df['CohortMonth'].dt.month)
)

# Build cohort count matrix
cohort_counts = (
    cohort_df.groupby(['CohortMonth', 'CohortIndex'])['CustomerID']
    .nunique()
    .unstack(fill_value=0)
)

# Build retention matrix
retention = cohort_counts.divide(cohort_counts[0], axis=0) * 100
retention = retention.round(1)

# Format cohort labels
cohort_counts.index = cohort_counts.index.strftime('%Y-%m')
retention.index = retention.index.strftime('%Y-%m')

# Hide future months with no available data
retention_display = retention.where(cohort_counts > 0)

print("\n👥 COHORT CUSTOMER COUNTS:")
print(cohort_counts)

print("\n📈 COHORT RETENTION RATES (%):")
print(retention_display)

# Save retention table
retention_display.to_csv("cohort_retention.csv")

# Static heatmap for report / presentation
plt.figure(figsize=(14, 8))
sns.heatmap(retention_display, annot=True, fmt=".1f", cmap="Blues")
plt.title("Customer Cohort Retention Rate (%)")
plt.xlabel("Months Since First Purchase")
plt.ylabel("Cohort Month")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "analysis9_cohort_retention.png"),
    dpi=300,
    bbox_inches='tight'
)
plt.close()

# Interactive heatmap for dashboard
fig9 = px.imshow(
    retention_display,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues",
    labels={
        "x": "Months Since First Purchase",
        "y": "Cohort Month",
        "color": "Retention %"
    },
    title="Customer Cohort Retention Rate (%)"
)

fig9.update_layout(
    height=600,
    font=dict(family="Arial", size=12)
)
fig9.update_xaxes(title="Months Since First Purchase", tickmode="linear")
fig9.update_yaxes(title="Cohort Month")

fig9.write_html(os.path.join(OUTPUT_DIR, "analysis9_cohort_retention.html"))

print("✓ Saved cohort_retention.csv")
print("✓ Saved outputs/analysis9_cohort_retention.png")
print("✓ Saved outputs/analysis9_cohort_retention.html")
print("✓ Analysis 9 complete")

# ==============================================================================
# ANALYSIS 10: FORECASTING & PREDICTIONS
# ==============================================================================

print("\n" + "="*70)
print(" "*20 + "ANALYSIS 10: FORECASTING & PREDICTIONS")
print("="*70)

# Simple trend analysis and projection
# TODO: Create revenue forecast for next quarter
# Can use simple trend line or more advanced methods

# Example: Calculate growth rate
revenue_by_month = df_clean.groupby(df_clean['InvoiceDate'].dt.to_period('M'))['TotalPrice'].sum()
growth_rates = revenue_by_month.pct_change()

print(f"\n📈 AVERAGE MONTHLY GROWTH RATE: {growth_rates.mean()*100:.2f}%")

# TODO: Create forecast visualization
# Project next 3 months based on trend



print("✓ Analysis 10 complete")

# ==============================================================================
# SUMMARY STATISTICS
# ==============================================================================

print("\n" + "="*70)
print(" "*25 + "PROJECT SUMMARY")
print("="*70)

summary_stats = {
    'Total Revenue': f"${total_revenue:,.2f}",
    'Total Transactions': f"{total_transactions:,}",
    'Total Customers': f"{total_customers:,}",
    'Average Order Value': f"${avg_order_value:,.2f}",
    'Top Country': country_revenue.index[0],
    'Date Range': f"{df_clean['InvoiceDate'].min()} to {df_clean['InvoiceDate'].max()}",
    'Total Products': f"{df_clean['StockCode'].nunique():,}",
    'Countries Served': f"{df_clean['Country'].nunique():,}"
}

summary_df = pd.DataFrame(list(summary_stats.items()), columns=['Metric', 'Value'])
summary_df.to_csv("project_summary.csv", index=False)

print("\n✓ Summary statistics saved to project_summary.csv")

# ==============================================================================
# NEXT STEPS
# ==============================================================================

print("\n" + "="*70)
print(" "*28 + "NEXT STEPS")
print("="*70)

print("""
📋 REMAINING TASKS:

1. COMPLETE ALL ANALYSES
   [ ] Analysis 1-8 are started - refine and enhance
   [ ] Complete Analysis 9 (Cohort Analysis)
   [ ] Complete Analysis 10 (Forecasting)

2. CREATE COMPREHENSIVE DASHBOARD
   [ ] Decide on dashboard format (Plotly Dash, Streamlit, HTML, etc.)
   [ ] Integrate all visualizations
   [ ] Add executive summary
   [ ] Polish design and layout

3. CREATE POWERPOINT PRESENTATION
   [ ] Title slide with team info
   [ ] Business problem (1-2 slides)
   [ ] Methodology (1 slide)
   [ ] Key visualizations (6-8 slides)
   [ ] Insights & recommendations (2-3 slides)
   [ ] Limitations & future work (1 slide)

4. WRITE TECHNICAL DOCUMENTATION
   [ ] Executive summary
   [ ] Data preparation details
   [ ] Analytical approach
   [ ] Key findings
   [ ] Business recommendations
   [ ] Limitations

5. FINALIZE CODE
   [ ] Add comments throughout
   [ ] Create README.md
   [ ] Create requirements.txt
   [ ] Test that everything runs
   [ ] Organize files logically

6. QUALITY CHECK
   [ ] All visualizations display correctly
   [ ] All files are properly named
   [ ] ZIP file is ready for submission
   [ ] Team review complete

Good luck! 🚀
""")

print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)
