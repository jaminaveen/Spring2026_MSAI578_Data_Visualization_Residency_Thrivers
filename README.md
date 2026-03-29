# E-Commerce Business Analytics
**MSAI 578 — Data Visualization | Spring 2026 | Dr. Deya Banisakher**
**Team: Thrivers**

---

## Team Members & Roles

| Name | Role |
|------|------|
| Naveen Jami | Data Engineer |
| Vikranth Reddy Gurram | Analyst 1 |
| Yiming Liu | Analyst 2 |
| Shishir Khanal | Visualization Specialist |
| Chiranjeevi Pinapati | Communications Lead |

---

## Reproducing This Project

### Requirements
- **Python:** 3.13.9
- **OS:** macOS / Linux / Windows

### Setup

```bash
# 1. Create a virtual environment using Python 3.13.9
python3.13 -m venv .venv

# 2. Activate it
source .venv/bin/activate          # macOS / Linux
.venv\Scripts\activate             # Windows

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Run the full analysis script
python project2_ecommerce_python.py
```

> **Dataset required:** Place `Online Retail.xlsx` inside the `data/` folder before running.
> Download from: https://archive.ics.uci.edu/ml/datasets/Online+Retail

All HTML figures are written automatically to the `outputs/` folder on first run.

---

## Project Files

```
.
├── data/
│   ├── Online Retail.xlsx               # source dataset (required)
│   └── E-COMMERCE DATA DICTIONARY.pdf
├── outputs/                             # all HTML/PNG figures (auto-created)
├── project2_ecommerce_python.py         # main analysis script (all 10 analyses)
├── thrivers_ecommerce_analytics.ipynb   # Data Engineer notebook (Analysis 1 & 8)
├── requirements.txt
├── project_summary.csv                  # auto-generated KPI summary
├── cohort_retention.csv                 # cohort retention matrix
└── README.md
```

---

## Dataset Overview

| Attribute | Value |
|-----------|-------|
| Source | UCI Machine Learning Repository |
| File | `data/Online Retail.xlsx` |
| Raw rows | 541,909 |
| Columns | 8 |
| Period | December 2010 – December 2011 |
| Geography | UK-primary; 38 countries total |

**Columns:** `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`

Each row is one product line within an invoice. A single invoice may span multiple rows.

---

## Data Engineering Decisions

### TODO 4 — Missing CustomerID (135,080 rows = 24.9%)
**Decision: Option B + C** — Keep rows, fill with `"Guest"`, add `IsGuest` flag.
- Guest transactions are real revenue; removing them understates total sales.
- `IsGuest=1` flag lets analysts filter them out for identity-dependent analyses (Analysis 3, 9).

### TODO 5 — Negative Quantities / Cancellations (10,624 rows)
**Decision: Option B** — Create separate `sales` and `returns` sub-datasets.
- `sales` (530,104 rows): positive transactions only — use for revenue/product/customer work.
- `returns` (9,288 rows): C-prefix invoices and negative-quantity rows — use for Analysis 8.
- Removing them entirely (Option A) would eliminate the signal needed for return analysis.

### TODO 6 — Outliers
| Action | Detail |
|--------|--------|
| Removed | 2,517 rows with `UnitPrice ≤ 0` (non-product adjustments) |
| Removed | Administrative `StockCode` rows (`POST`, `DOT`, `BANK CHARGES`, etc.) |
| Flagged, kept | 540 extreme price outliers (`UnitPrice > £206.39`) → `IsPriceOutlier` |
| Flagged, kept | 474 extreme quantity outliers (`|Qty| > 480`) → `IsQtyOutlier` |

**Final cleaned dataset:** 539,392 rows × 21 columns

### Engineered Columns

| Column | Description |
|--------|-------------|
| `TotalPrice` | `Quantity × UnitPrice` |
| `Year`, `Month`, `MonthName`, `Day` | Date components |
| `DayOfWeek`, `Hour`, `Date` | Time components |
| `YearMonth`, `Quarter` | Aggregation periods |
| `IsGuest` | 1 = no CustomerID on record |
| `IsReturn` | 1 = negative Quantity |
| `IsCancellation` | 1 = InvoiceNo starts with 'C' |
| `IsPriceOutlier` | 1 = UnitPrice > 99.9th percentile |
| `IsQtyOutlier` | 1 = \|Quantity\| > 99.9th percentile |

### Dataset Reference for Analysts

| DataFrame | Use for |
|-----------|---------|
| `df_clean` | All transactions including returns |
| `sales` | Revenue, product performance, basket, time-pattern analyses |
| `returns` | Analysis 8 — returns & cancellations |
| `df_clean[df_clean['IsGuest']==0]` | Customer behavior, CLV, cohort analyses (Analysis 3, 9) |

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Revenue (net) | £9,769,872 |
| Gross Sales Revenue | £10,666,685 |
| Return Financial Impact | £896,812 (8.41% of gross) |
| Total Invoices | 23,796 |
| Unique Registered Customers | 4,372 |
| Unique Products | 4,070 |
| Countries Served | 38 |
| Average Order Value | £410.57 |
| Avg Month-over-Month Growth | 2.9% |
| Peak Revenue Month | November 2011 — £1,509,496 |
| Peak Sales Day | Thursday |
| Peak Sales Hour | 10:00 |
| Repeat Customer Rate | 70% |
| UK Market Share | 84.0% of revenue |
| ARIMA Forecast (Q1 2012) | ~£2.84M |

---

## Analyses Produced

| # | Analysis | Lead | Outputs |
|---|----------|------|---------|
| 1 | Sales Overview & Trends | Data Engineer | `analysis1_monthly_revenue.html`, `analysis1_weekly_revenue.html`, `analysis1_growth_rate.html`, `analysis1_seasonal.html` |
| 2 | Product Performance | Analyst 1 | `analysis2_top_products_quantity.html`, `analysis2_top_products_revenue.html` |
| 3 | Customer Behavior (RFM) | Analyst 1 | `analysis3_purchase_frequency.html` |
| 4 | Geographic Analysis | Analyst 2 | `analysis4_country_revenue.html` |
| 5 | Time-Based Patterns | Analyst 2 | `analysis5_day_of_week.html`, `analysis5_hour_of_day.html` |
| 6 | Basket Analysis | Visualization Specialist | `analysis6_basket_distribution.html` |
| 7 | Pricing Analysis | Visualization Specialist | `analysis7_price_distribution.html`, `analysis7_price_ranges.html` |
| 8 | Returns & Cancellations | Data Engineer | `analysis8_top_returns.html`, `analysis8_return_rate_by_product.html`, `analysis8_returns_over_time.html`, `analysis8_returns_by_country.html` |
| 9 | Cohort Analysis | Analyst 1 | `analysis9_cohort_retention.html`, `analysis9_cohort_retention.png` |
| 10 | Forecasting & Predictions | All | `analysis10_forecast.html` |
| — | Executive Dashboard | Visualization Specialist | `executive_dashboard.html` |

---

## Key Findings

- **Revenue peak:** November 2011 drove £1.5M — Q4 overall is the strongest quarter. Q1/Q2 are softer by ~25–30%.
- **Returns:** £897K (8.41% of gross) lost to returns. Return rate by transaction row is 1.72%.
- **Geography:** UK accounts for 84% of revenue. Netherlands, EIRE, and Germany are the top international markets.
- **Customer health:** 70% repeat rate, but the largest RFM segment is "Lost" (1,514 customers) — a retention opportunity.
- **Trading pattern:** Peak hours are 10:00–12:00 Thursday–Tuesday. Saturday has near-zero sales, consistent with B2B wholesale.
- **Forecast:** ARIMA projects ~£2.84M for Q1 2012, consistent with prior-year Q1 seasonality.

---

## Tools & Technologies

- **Python:** 3.13.9
- **Libraries:** pandas 3.0.1, numpy 2.4.3, plotly 6.6.0, matplotlib 3.10.8, seaborn 0.13.2, scipy 1.17.1, statsmodels 0.14.6, openpyxl 3.1.5
