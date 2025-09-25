import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("customer360_cleaned.csv")

st.set_page_config(page_title="Customer 360 Dashboard", layout="wide")
st.title("📊 Customer 360 Dashboard")
st.markdown("Visualizing Telco churn data with engagement and risk insights.")

# -------------------------------
# 📌 Key Metrics Summary
# -------------------------------
st.markdown("### 📌 Key Metrics Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", len(df))
col2.metric("Churn Rate", f"{(df['Churn_Risk'] == 'High').mean():.2%}")
col3.metric("Avg Engagement Score", f"{df['Engagement_Score'].mean():.2f}")

# -------------------------------
# 🔍 Sidebar Filters
# -------------------------------
st.sidebar.header("🔍 Filter Data")
contract_filter = st.sidebar.multiselect("Contract Type", df['Contract'].unique())
internet_filter = st.sidebar.multiselect("Internet Service", df['InternetService'].unique())

filtered_df = df.copy()
if contract_filter:
    filtered_df = filtered_df[filtered_df['Contract'].isin(contract_filter)]
if internet_filter:
    filtered_df = filtered_df[filtered_df['InternetService'].isin(internet_filter)]

# -------------------------------
# 💡 Feature Descriptions
# -------------------------------
st.markdown("💡 **Engagement Score**: Number of services a customer uses. Higher = more loyal.")
st.markdown("💡 **Churn Risk**: Flag based on whether the customer has churned.")
st.markdown("💡 **Tenure Bucket**: Groups customers by how long they've stayed.")

# -------------------------------
# 📊 Churn Risk Pie Chart
# -------------------------------
churn_counts = filtered_df['Churn_Risk'].value_counts()
fig_churn = px.pie(values=churn_counts.values, names=churn_counts.index, title="Churn Risk Distribution")
st.plotly_chart(fig_churn, use_container_width=True)

# -------------------------------
# 📈 Engagement Score Histogram
# -------------------------------
fig_engage = px.histogram(filtered_df, x='Engagement_Score', nbins=10, title="Engagement Score Distribution")
st.plotly_chart(fig_engage, use_container_width=True)

# -------------------------------
# 📍 Tenure Bucket Bar Chart
# -------------------------------
tenure_counts = filtered_df['Tenure_Bucket'].value_counts().reset_index()
tenure_counts.columns = ['Tenure_Bucket', 'Customer_Count']
fig_tenure = px.bar(
    tenure_counts,
    x='Tenure_Bucket',
    y='Customer_Count',
    title="Tenure Bucket Breakdown",
    labels={'Tenure_Bucket': 'Tenure Bucket', 'Customer_Count': 'Customer Count'}
)
st.plotly_chart(fig_tenure, use_container_width=True)

# -------------------------------
# 🔥 Correlation Heatmap
# -------------------------------
st.markdown("### 🔥 Feature Correlation Heatmap")
corr = filtered_df.select_dtypes(include='number').corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# -------------------------------
# 📥 Download Filtered Data
# -------------------------------
st.download_button("📥 Download Filtered Data", filtered_df.to_csv(index=False), "filtered_data.csv")

# -------------------------------
# 🔎 Filter by Contract Type (Legacy View)
# -------------------------------
st.markdown("### 🔎 Contract Type View")
contract_type = st.selectbox("Select Contract Type", df['Contract'].unique())
contract_df = df[df['Contract'] == contract_type]
st.write(f"Showing {len(contract_df)} customers with contract type: {contract_type}")
st.dataframe(contract_df[['customerID', 'Engagement_Score', 'Churn_Risk']])
