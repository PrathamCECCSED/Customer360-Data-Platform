import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned data
df = pd.read_csv("customer360_cleaned.csv")

st.title("📊 Customer 360 Dashboard")
st.markdown("Visualizing Telco churn data with engagement and risk insights.")

# Churn Risk Pie Chart
churn_counts = df['Churn_Risk'].value_counts()
fig_churn = px.pie(values=churn_counts.values, names=churn_counts.index, title="Churn Risk Distribution")
st.plotly_chart(fig_churn)

# Engagement Score Histogram
fig_engage = px.histogram(df, x='Engagement_Score', nbins=10, title="Engagement Score Distribution")
st.plotly_chart(fig_engage)

# Tenure Bucket Bar Chart
fig_tenure = px.bar(df['Tenure_Bucket'].value_counts().reset_index(),
                    x='index', y='Tenure_Bucket',
                    title="Tenure Bucket Breakdown",
                    labels={'index': 'Tenure Bucket', 'Tenure_Bucket': 'Customer Count'})
st.plotly_chart(fig_tenure)

# Filter by Contract Type
contract_type = st.selectbox("Filter by Contract Type", df['Contract'].unique())
filtered_df = df[df['Contract'] == contract_type]
st.write(f"Showing {len(filtered_df)} customers with contract type: {contract_type}")
st.dataframe(filtered_df[['customerID', 'Engagement_Score', 'Churn_Risk']])
