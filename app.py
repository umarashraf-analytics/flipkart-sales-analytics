import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Flipkart Analytics Engine", layout="wide")
st.title("🛍️ Flipkart Sales & Customer Analytics Platform")
st.markdown("Enterprise data pipeline visualizing customer lifetime value, segmentations, and purchase affinities.")

# --- COMPREHENSIVE E-COMMERCE DATA PIPELINE (Cached for speed) ---
@st.cache_data
def run_ecommerce_pipeline():
    np.random.seed(101)
    random.seed(101)
    
    # 1. Base Parameters
    categories = ['Electronics', 'Fashion', 'Home & Kitchen', 'Beauty & Personal Care', 'Books & Media']
    products = {
        'Electronics': ['Realme Smartphone', 'BoAt Wireless Earbuds', 'HP Laptop', 'Samsung Smartwatch'],
        'Fashion': ['Men Slim Fit Jeans', 'Women Ethnic Kurti', 'Puma Running Shoes', 'Leather Wallet'],
        'Home & Kitchen': ['Prestige Induction Cooktop', 'Milton Water Bottle', 'Bedsheet Set', 'LED Desk Lamp'],
        'Beauty & Personal Care': ['Mamaearth Face Wash', 'Nivea Body Lotion', 'Matte Lipstick', 'Trimmer'],
        'Books & Media': ['UPSC Prep Guide', 'Fiction Bestseller', 'Self-Help Book', 'Financial Freedom Guide']
    }
    payment_methods = ['UPI (PhonePe/GPay)', 'Flipkart Axis Credit Card', 'Cash on Delivery', 'Net Banking']
    cities = ['Bengaluru', 'Mumbai', 'Delhi', 'Hyderabad', 'Chennai', 'Pune']
    
    # 2. Generate Core Sales Datasets
    sales_data = []
    start_date = datetime(2025, 6, 1)
    
    for i in range(2500):
        order_id = f"OD{random.randint(100000000, 999999999)}"
        customer_id = f"FK-CUST-{random.randint(1000, 1400)}"  # 400 unique customers for repeating patterns
        category = random.choice(categories)
        product = random.choice(products[category])
        
        # Weighted pricing logic
        if category == 'Electronics': base_price = random.randint(1500, 45000)
        elif category == 'Fashion': base_price = random.randint(499, 2999)
        else: base_price = random.randint(199, 1499)
        
        qty = np.random.choice([1, 2, 3], p=[0.85, 0.12, 0.03])
        sales_amt = base_price * qty
        discount = round(sales_amt * random.choice([0.05, 0.10, 0.15, 0.20]), 2)
        final_payout = sales_amt - discount
        
        order_date = start_date + timedelta(days=random.randint(0, 365))
        city = random.choice(cities)
        pay_mode = random.choice(payment_methods)
        
        sales_data.append([order_id, customer_id, order_date, category, product, final_payout, city, pay_mode])
        
    df_sales = pd.DataFrame(sales_data, columns=[
        'Order_ID', 'Customer_ID', 'Order_Date', 'Category', 'Product', 'Net_Revenue_INR', 'City', 'Payment_Method'
    ])
    
    # 3. ADVANCED ALGORITHMIC LAYER: RFM Customer Segmentation
    # Recency (Days since last purchase), Frequency (Total orders), Monetary (Total spend)
    snapshot_date = df_sales['Order_Date'].max() + timedelta(days=1)
    
    rfm = df_sales.groupby('Customer_ID').agg(
        Recency=('Order_Date', lambda x: (snapshot_date - x.max()).days),
        Frequency=('Order_ID', 'count'),
        Monetary=('Net_Revenue_INR', 'sum')
    ).reset_index()
    
    # Mathematical binning using quantiles
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 3, labels=[3, 2, 1]).astype(int) # Lower recency days = Higher score
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 3, labels=[1, 2, 3]).astype(int)
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 3, labels=[1, 2, 3]).astype(int)
    
    # Segmentation logic mapping
    def segment_customer(row):
        total_score = row['R_Score'] + row['F_Score'] + row['M_Score']
        if total_score >= 8: return '🏆 High-Value Loyal'
        elif total_score >= 5: return '📈 Mid-Tier Regular'
        else: return '⚠️ At-Risk / Hibernating'
        
    rfm['Customer_Segment'] = rfm.apply(segment_customer, axis=1)
    
    return df_sales, rfm

# Run pipeline
df_sales, rfm_df = run_ecommerce_pipeline()

# --- PRESENTATION LAYER: KPI DASHBOARD ---
tot_rev = df_sales['Net_Revenue_INR'].sum()
tot_orders = len(df_sales)
avg_ticket = tot_rev / tot_orders

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1: st.metric("Gross Revenue (INR)", f"₹{tot_rev:,.2f}")
with kpi2: st.metric("Total Order Volume", f"{tot_orders:,} Orders")
with kpi3: st.metric("Average Order Value (AOV)", f"₹{avg_ticket:,.2f}")

st.write("---")

tab1, tab2, tab3 = st.tabs(["📊 Sales Performance Trends", "👥 Customer Segmentation (RFM)", "🎯 Product Affinity Matrix"])

with tab1:
    st.subheader("Category-Wise Financial Breakdown")
    cat_analysis = df_sales.groupby('Category').agg(
        Revenue_Contribution=('Net_Revenue_INR', 'sum'),
        Units_Sold=('Order_ID', 'count')
    ).sort_values(by='Revenue_Contribution', ascending=False)
    st.dataframe(cat_analysis, use_container_width=True)
    
    st.subheader("Geographic Revenue Distribution")
    city_analysis = df_sales.groupby('City').Net_Revenue_INR.sum().reset_index().sort_values(by='Net_Revenue_INR', ascending=False)
    st.dataframe(city_analysis, use_container_width=True, index=False)

with tab2:
    st.subheader("Algorithmic Marketing Segmentation")
    st.markdown("Customers partitioned using historical Recency, Frequency, and Monetary parameters.")
    
    seg_counts = rfm_df['Customer_Segment'].value_counts().reset_index()
    seg_counts.columns = ['Customer Segment', 'Headcount']
    st.table(seg_counts)
    
    st.subheader("Drill-Down Customer Registry")
    st.dataframe(rfm_df[['Customer_ID', 'Recency', 'Frequency', 'Monetary', 'Customer_Segment']], use_container_width=True, index=False)

with tab3:
    st.subheader("Top Performing Product Affinity Catalog")
    st.markdown("Identifies moving SKU item sets accelerating catalog turnover.")
    prod_analysis = df_sales.groupby(['Category', 'Product']).agg(
        Total_Sales_INR=('Net_Revenue_INR', 'sum'),
        Volume=('Order_ID', 'count')
    ).sort_values(by='Total_Sales_INR', ascending=False).reset_index()
    st.dataframe(prod_analysis, use_container_width=True, index=False)
