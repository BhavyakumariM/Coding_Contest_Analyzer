import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Coding Contest Analyzer", layout="centered")

st.title("🏆 Coding Contest Analyzer")
st.markdown("Analyze your contest performance over time.")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your contest CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Convert 'Date' to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # 📋 Display raw data
    st.subheader("📋 Raw Contest Data")
    st.dataframe(df)

    # 📆 Date filter
    st.subheader("📆 Filter by Date Range")
    min_date = df['Date'].min()
    max_date = df['Date'].max()

    start_date, end_date = st.date_input(
        "Select date range:",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Filtered data
    mask = (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))
    filtered_df = df.loc[mask]

    if filtered_df.empty:
        st.warning("No contests found in the selected date range.")
    else:
        st.subheader("📊 Filtered Contest Data")
        st.dataframe(filtered_df)

        # Summary for filtered data
        avg_score = filtered_df['Score'].mean()
        avg_attempts = filtered_df['Attempts'].mean()
        st.metric("Filtered Avg Score", f"{avg_score:.2f}")
        st.metric("Filtered Avg Attempts", f"{avg_attempts:.2f}")

        # Chart type selector
        chart_type = st.selectbox("📊 Select chart type:", ["Line Chart", "Bar Chart"])

        st.subheader("📈 Score Trend (Filtered)")
        if chart_type == "Line Chart":
            st.line_chart(filtered_df.set_index("Date")["Score"])
        else:
            st.bar_chart(filtered_df.set_index("Date")["Score"])

        st.subheader("🌀 Attempts Trend (Filtered)")
        if chart_type == "Line Chart":
            st.line_chart(filtered_df.set_index("Date")["Attempts"])
        else:
            st.bar_chart(filtered_df.set_index("Date")["Attempts"])

    # 📈 Overall Summary Stats
    st.subheader("📈 Overall Performance Summary")
    avg_score_all = df['Score'].mean()
    avg_attempts_all = df['Attempts'].mean()
    st.metric("Overall Avg Score", f"{avg_score_all:.2f}")
    st.metric("Overall Avg Attempts", f"{avg_attempts_all:.2f}")

    # 🏅 Top 3 contests
    st.subheader("🏅 Top 3 Contests by Score")
    top3 = df.sort_values("Score", ascending=False).head(3)
    st.table(top3[['Contest', 'Date', 'Score', 'Attempts']])

else:
    st.info("👆 Please upload a .csv file containing your contest data.")
