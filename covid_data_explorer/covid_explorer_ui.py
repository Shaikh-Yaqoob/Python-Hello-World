# Import libraries
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import os

# Ensure necessary directories exist
base_dir = "D:/covid_data_explorer"
data_dir = os.path.join(base_dir, "data")
saved_reports_dir = os.path.join(base_dir, "saved_reports")

os.makedirs(data_dir, exist_ok=True)
os.makedirs(saved_reports_dir, exist_ok=True)

# Default file path for the dataset
default_file_path = os.path.join(data_dir, "covid-data.csv")

# Function to load and preprocess data
def load_data(filepath):
    data = pd.read_csv(filepath, parse_dates=['date'])
    # Selecting relevant columns
    columns_to_keep = [
        "iso_code", "continent", "location", "date", "total_cases", "new_cases", 
        "total_deaths", "new_deaths", "total_vaccinations", "population", 
        "median_age", "population_density", "hospital_beds_per_thousand"
    ]
    data = data[columns_to_keep]
    data.fillna(0, inplace=True)  # Handling missing values
    return data

# Function to calculate summary statistics
def get_summary_statistics(data):
    stats = {
        "🌎 Total Cases": int(data['total_cases'].sum()),
        "⚰️ Total Deaths": int(data['total_deaths'].sum()),
        "📈 Avg. New Cases": round(np.mean(data['new_cases']), 2),
        "💉 Total Vaccinations": int(data['total_vaccinations'].sum()),
    }
    return stats

# Function to plot data using Plotly
def plot_data(data, country='World', metric='total_cases'):
    country_data = data[data['location'] == country]
    fig = px.line(
        country_data,
        x='date',
        y=metric,
        title=f'{metric.replace("_", " ").title()} in {country}',
        labels={'date': 'Date', metric: metric.replace("_", " ").title()},
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig.update_layout(
        title=dict(font=dict(size=24), x=0.5),
        xaxis=dict(title="Date", titlefont=dict(size=20), tickfont=dict(size=16)),
        yaxis=dict(title=metric.replace("_", " ").title(), titlefont=dict(size=20), tickfont=dict(size=16)),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    fig.update_traces(line=dict(color='white', width=2))
    return fig

# Streamlit App
st.set_page_config(page_title="COVID-19 Data Explorer", page_icon="🦠", layout="wide")
st.markdown(
    """
    <style>
        .main {background-color: #2e2e2e; color: white; font-size: 18px;}
        .sidebar .sidebar-content {background-color: #3e3e3e; color: white; font-size: 18px;}
        h1 {color: #4e79a7; font-size: 32px;}
        h2 {color: #f28e2c; font-size: 28px;}
        footer {visibility: hidden;}
        .stButton>button {background-color: #4CAF50; color: white; border-radius: 12px; font-size: 18px;}
        .stButton>button:hover {background-color: #45a049;}
        .stSelectbox>div>div>div>div>div {color: #4e79a7; font-size: 18px;}
        .stMarkdown {color: white; font-size: 18px;}
        .stTextInput>div>div>input {background-color: #3e3e3e; color: white; border-radius: 5px; border: 1px solid #4e79a7;}
        .stTextInput>div>div>input:focus {border: 1px solid #f28e2c;}
        .stFileUploader>div>div>div>button {background-color: #4CAF50; color: white; border-radius: 12px; font-size: 18px;}
        .stFileUploader>div>div>div>button:hover {background-color: #45a049;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🦠 COVID-19 Data Explorer")
st.markdown(
    """
    <div style="background-color: #3e3e3e; padding: 10px; border-radius: 10px;">
        <h2>Welcome to the COVID-19 Data Explorer!</h2>
        <p>Analyze global trends, upload your own data, and visualize key insights.</p>
    </div>
    """, unsafe_allow_html=True
)
st.sidebar.title("⚙️ Options")

# File uploader for custom dataset
filepath = st.sidebar.file_uploader("📂 Upload CSV", type=["csv"])

# Load default or uploaded dataset
if filepath:
    data = load_data(filepath)
else:
    if not os.path.exists(default_file_path):
        st.error(f"❌ Default dataset not found at '{default_file_path}'. Please upload a CSV.")
    else:
        data = load_data(default_file_path)

# Sidebar options
if 'location' in data.columns:
    country = st.sidebar.selectbox("🌍 Select Country", data['location'].unique())
else:
    st.error("❌ The dataset does not have a 'location' column. Please upload a valid CSV.")
    country = "World"

metric = st.sidebar.selectbox("📊 Select Metric", ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_vaccinations'])

# Display Summary Statistics
st.header("📋 Summary Statistics")
stats = get_summary_statistics(data)
for key, value in stats.items():
    st.markdown(f"<div style='background-color: #4e4e4e; padding: 10px; border-radius: 10px; font-size: 18px;'><strong>{key}</strong>: {value:,}</div>", unsafe_allow_html=True)

# Data Visualization
st.header("📈 Data Visualization")
fig = plot_data(data, country, metric)
st.plotly_chart(fig)

# Save Graph
if st.button("💾 Save Graph"):
    save_path = os.path.join(saved_reports_dir, f"{country}_{metric}_trend.png")
    fig.write_image(save_path)
    st.success(f"✅ Graph saved at {save_path}")

# Save Statistics
if st.button("📝 Save Statistics"):
    stats_path = os.path.join(saved_reports_dir, f"{country}_statistics.txt")
    with open(stats_path, "w") as f:
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")
    st.success(f"✅ Statistics saved at {stats_path}")
