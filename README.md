# E-Commerce Business Analytics Project

## Course Information
- **Class:** Spring 2026 - MSAI 578 - M70 - Data Visualization  
- **Instructor:** Dr. Deya Banisakher  
- **Group Name:** Thrivers  

---

## Project Title
**E-Commerce Business Analytics**

---

## Dataset Overview

### Primary Dataset: E-Commerce Transactions

- **Source:** UCI Machine Learning Repository / Kaggle  
- **Dataset Name:** Online Retail Dataset  

### Description
This dataset contains transactional data from a UK-based online retail company. It captures detailed information about customer purchases, including products, quantities, pricing, and geographic location. The dataset is widely used for analyzing customer behavior, sales trends, and business performance in e-commerce environments.

---

## Dataset Details

- **Size:** ~540,000 transactions  
- **Time Period:** December 2010 – December 2011  
- **Geographical Scope:** Primarily United Kingdom, with some international transactions  
- **Data Type:** Transactional (Retail/E-Commerce)

---

## Dataset Attributes

The dataset contains the following key fields:

- **Invoice Number:** Unique identifier for each transaction  
- **Stock Code (Product ID):** Unique code assigned to each product  
- **Description (Product Name):** Name of the product purchased  
- **Quantity Sold:** Number of units purchased per transaction  
- **Invoice Date/Time:** Timestamp of when the transaction occurred  
- **Unit Price:** Price per unit of the product  
- **Customer ID:** Unique identifier for each customer  
- **Country:** Country where the customer is located  

---

## Data Characteristics

- The dataset is **transaction-level**, where each row represents a single product within an invoice.  
- A single invoice may include multiple rows (i.e., multiple products in one purchase).  
- The data supports multiple analytical perspectives, including:
  - Time-series analysis (sales trends, seasonality)  
  - Customer behavior analysis  
  - Product performance evaluation  
  - Geographic sales distribution  

---

## Dataset Link
- https://archive.ics.uci.edu/ml/datasets/Online+Retail

---

## Project Objectives

The primary goal of this project is to apply data visualization techniques to extract meaningful business insights from e-commerce data.

### Key Objectives:
- Analyze customer purchasing behavior  
- Identify trends and seasonal patterns in sales  
- Evaluate product-level performance and revenue contribution  
- Explore geographic distribution of customers and sales  
- Generate actionable insights to support business decision-making  

---

## Tools & Technologies

- **Programming:** Python  
- **Libraries:** Pandas, NumPy  
- **Visualization:** Matplotlib, Seaborn, Plotly  
- **Environment:** Jupyter Notebook  

---

# Data Engineer Handoff — Team Reference

---

## 📁 Datasets Available to All Analysts

- **`df_clean`**  
  Full cleaned dataset *(all transactions, including returns)*  

- **`sales`**  
  Positive transactions only  
  → Use for **revenue, product, and customer analyses**  

- **`returns`**  
  Returns and cancellations  
  → Use for **return behavior analysis (Analysis 8)**  

---

## Column Reference (PascalCase)

### Original Columns
- `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`  
- `UnitPrice`, `CustomerID`, `Country`  

### Engineered Columns
- `TotalPrice`, `Year`, `Month`, `MonthName`, `Day`, `DayOfWeek`  
- `Hour`, `Date`, `YearMonth`, `Quarter`  

### Flags
- `IsGuest`, `IsReturn`, `IsCancellation`, `IsPriceOutlier`, `IsQtyOutlier`  

---

## Data Cleaning Decisions

- **TODO 4 — CustomerID Handling**  
  → Option B + C  
  → Missing values filled with `"Guest"`  
  → Flag added: `IsGuest = 1`  

- **TODO 5 — Negative Quantity Handling**  
  → Option B  
  → Created separate datasets:  
    - `sales` (valid purchases)  
    - `returns` (returns/cancellations)  

- **TODO 6 — Outlier Handling**  
Removed: Zero-price transactions
Flagged extreme values: Price (`IsPriceOutlier`), Quantity (`IsQtyOutlier`)  

---

## Final Dataset Sizes

- **df_clean:** 534,129 rows × 23 columns  
- **sales:** 524,878 rows  
- **returns:** 9,251 rows  

---

## Other Notes
- Naming convention: **PascalCase** for consistency with starter code  
- Datasets are ready for downstream analysis and visualization  
- Supports:
  - Time-series analysis  
  - Customer segmentation  
  - Product analytics  
  - Return behavior analysis  

---