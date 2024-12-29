import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Load your dataset
@st.cache_data
def load_data():
    data = pd.read_csv("cleaned_graduate_employment_data_2.csv")  # Ensure the CSV file is in the same directory or provide full path
    return data

# Load data
data = load_data()

# Title and Description
st.title("Graduate Employment Survey from Singapore Universities")
st.write("Ever wondered how graduate employment trends differ between degrees? Which field secures the highest salaries or the highest employment rate? Explore and compare one or two degrees with this interactive tool to find out!")

# Step 1: Degree Selection


# Select Degree 1
universities = data["University"].unique()
selected_university1 = st.selectbox("Select the University for Degree 1:", universities, key="uni1")
filtered_schools1 = data[data["University"] == selected_university1]["School"].unique()
selected_school1 = st.selectbox("Select the School for Degree 1:", filtered_schools1, key="school1")
filtered_degrees1 = data[
    (data["University"] == selected_university1) & 
    (data["School"] == selected_school1)
]["Degree"].unique()
selected_degree1 = st.selectbox("Select Degree 1:", filtered_degrees1, key="degree1")

# Degree Comparison Options
st.subheader("Degree Comparison Options")
compare_second_degree = st.radio("Do you want to compare with a second degree?", ["No", "Yes"], index=1)

# Select Degree 2 if comparison is enabled
if compare_second_degree == "Yes":
    st.markdown("---")
    selected_university2 = st.selectbox("Select the University for Degree 2:", universities, key="uni2")
    filtered_schools2 = data[data["University"] == selected_university2]["School"].unique()
    selected_school2 = st.selectbox("Select the School for Degree 2:", filtered_schools2, key="school2")
    # Exclude Degree 1 from Degree 2 options
    filtered_degrees2 = data[
        (data["University"] == selected_university2) & 
        (data["School"] == selected_school2)
    ]["Degree"].unique()
    filtered_degrees2 = [degree for degree in filtered_degrees2 if degree != selected_degree1]
    selected_degree2 = st.selectbox("Select Degree 2:", filtered_degrees2, key="degree2")
else:
    selected_university2, selected_school2, selected_degree2 = None, None, None



# Step 2: Select Time Frame
years = data["Year"].unique()
start_year, end_year = st.select_slider(
    "Select a Time Frame (Year Range):",
    options=sorted(years),
    value=(min(years), max(years))
)

# Step 3: Select Metric to Compare
metrics = [
    "Employment Rate (Overall)",
    "Employment Rate (Full-Time Permanent)",
    "Basic Monthly Mean",
    "Basic Monthly Median",
    "Gross Monthly Mean",
    "Gross Monthly Median",
    "Gross Monthly 25th Percentile",
    "Gross Monthly 75th Percentile",
]
selected_metric = st.selectbox("Select a Metric to Compare:", metrics)

# Filter Data
filtered_data1 = data[
    (data["University"] == selected_university1) &
    (data["School"] == selected_school1) &
    (data["Degree"] == selected_degree1) &
    (data["Year"] >= start_year) &
    (data["Year"] <= end_year)
]

if compare_second_degree == "Yes":
    filtered_data2 = data[
        (data["University"] == selected_university2) &
        (data["School"] == selected_school2) &
        (data["Degree"] == selected_degree2) &
        (data["Year"] >= start_year) &
        (data["Year"] <= end_year)
    ]
    combined_data = pd.concat([filtered_data1, filtered_data2])
else:
    combined_data = filtered_data1

# Display Graph
if combined_data.empty:
    st.write("No data available for the selected filters.")
else:
    # Plot Line Graph with custom colors
    fig = px.line(
        combined_data,
        x="Year",
        y=selected_metric,
        color="Degree",
        markers=True,
        title=f"{selected_metric.replace('_', ' ')} Over Time",
        color_discrete_map={
            selected_degree1: "#1f77b4",  # Blue for Degree 1
            selected_degree2: "#ff7f0e" if compare_second_degree == "Yes" else None,  # Orange for Degree 2
        }
    )

    # Configure legend to appear at the bottom
    fig.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",
            y=-0.3,  # Position below the plot
            xanchor="center",
            x=0.5
        ),
        xaxis_title="Year",
        yaxis_title=selected_metric.replace("_", " ").capitalize(),
    )

    # Remove annotations (no longer needed)
    st.plotly_chart(fig)

# Show Data Preview (Optional)
with st.expander("View Filtered Data for Both Degrees"):
    st.dataframe(combined_data)
