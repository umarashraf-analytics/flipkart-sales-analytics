# 🛍️ Flipkart Sales & Customer Analytics Platform

### 🔗 [Launch Live Interactive Analytics Dashboard]

An end-to-end data processing pipeline and business intelligence platform built to simulate, aggregate, and analyze hyper-scale e-commerce transactional data. The system features advanced programmatic algorithmic features like **RFM (Recency, Frequency, Monetary) Customer Segmentation** to maximize retention strategy and marketing optimization.

---

## 🛠️ Technical Stack Archetype
- **Core Engineering Ecosystem:** Python, Pandas, NumPy
- **Serving Architecture:** Streamlit Community Cloud Engine
- **Algorithmic Focus:** Quantile-based RFM Aggregation and Product Performance Affinity Tracking

---

## 🧠 Data Pipeline & Architectural Deep Dive

### 1. In-Memory Data Generation & Optimization
- Engineered a scalable transaction generator that establishes robust purchasing behavior logs across hundreds of unique consumer tokens over a 365-day tracking continuum.
- Integrated performance-optimizing memory caching wrappers (`@st.cache_data`) to protect server load bounds and provide snappy web component switches.

### 2. Algorithmic RFM Customer Segmentation
The background data layer automatically groups transactions per consumer to derive three core features:
- **Recency ($R$):** Operationalized as time deltas between a simulated snapshot checkpoint and the maximum order date recorded.
- **Frequency ($F$):** Total aggregated raw transaction volume counts.
- **Monetary ($M$):** Aggregated mathematical column sum of a user's net spend.

The pipeline computes statistical quantiles across these parameters, partitioning users dynamically into three distinct high-level behavioral buckets:
- `🏆 High-Value Loyal`
- `📈 Mid-Tier Regular`
- `⚠️ At-Risk / Hibernating`

---

## 🚀 Native Local Deployment Setup

1. Copy the source directory environment:
   ```bash
   git clone [https://github.com/umarashraf-analytics/flipkart-sales-analytics.git](https://github.com/umarashraf-analytics/flipkart-sales-analytics.git)
   cd flipkart-sales-analytics
