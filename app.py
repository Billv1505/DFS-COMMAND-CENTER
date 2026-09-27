import streamlit as st
import subprocess
import os
import pandas as pd

st.set_page_config(page_title="DFS Command Center", page_icon="🏈", layout="wide")

st.title("🏈 DFS Command Center")
st.write("Step 2: Build dataset + run projections")

DATASET_PATH = "data/nfl_dataset.csv"
PREDICTIONS_DIR = "predictions"


@st.cache_resource(show_spinner=False)
def build_dataset():
    """Run build-data once and cache the result."""
    with st.spinner("Building historical dataset (2018-present)... This takes 5-10 minutes on first run."):
        result = subprocess.run(
            ["python", "-m", "nfl_projections", "build-data"],
            capture_output=True, text=True, timeout=900,
        )
    return {
        "stdout": result.stdout[-1000:] if result.stdout else "",
        "stderr": result.stderr[-1000:] if result.stderr else "",
        "exists": os.path.exists(DATASET_PATH),
    }


@st.cache_resource(show_spinner=False)
def run_projections(week: int):
    """Run predict with quantiles once and cache."""
    with st.spinner(f"Training model and projecting Week {week}... This takes 5-10 minutes."):
        result = subprocess.run(
            ["python", "-m", "nfl_projections", "predict",
             "--season", "2025", "--week", str(week), "--quantiles"],
            capture_output=True, text=True, timeout=900,
        )
    return {
        "stdout": result.stdout[-1000:] if result.stdout else "",
        "stderr": result.stderr[-1000:] if result.stderr else "",
    }


st.markdown("### 1. Build Dataset")
st.write("This downloads nflverse data and creates `data/nfl_dataset.csv`. Required once.")

if st.button("🚀 Build Dataset"):
    build_result = build_dataset()
    if build_result["exists"]:
        st.success("✅ Dataset built successfully.")
    else:
        st.error("Dataset build failed. See logs below.")
        with st.expander("Build logs"):
            st.code(build_result["stdout"])
            st.code(build_result["stderr"])
        st.stop()

st.markdown("---")
st.markdown("### 2. Run Projections")

week = st.number_input("Week", min_value=1, max_value=18, value=3)

if st.button("📊 Run Projections"):
    if not os.path.exists(DATASET_PATH):
        st.warning("Build the dataset first.")
        st.stop()

    proj_result = run_projections(week)

    # Find prediction CSV
    if os.path.exists(PREDICTIONS_DIR):
        files = sorted(os.listdir(PREDICTIONS_DIR))
        csv_files = [f for f in files if f.endswith(".csv") and f"week{week}" in f.lower()]
        if not csv_files:
            csv_files = [f for f in files if f.endswith(".csv")]

        if csv_files:
            latest = csv_files[-1]
            df = pd.read_csv(os.path.join(PREDICTIONS_DIR, latest))
            st.success(f"✅ Loaded: {latest} ({len(df)} players)")
            st.dataframe(df, use_container_width=True, height=600)
        else:
            st.warning("No CSV files found in predictions/. Check logs:")
            with st.expander("Logs"):
                st.code(proj_result["stdout"])
                st.code(proj_result["stderr"])
    else:
        st.error("predictions/ folder not created. See logs:")
        with st.expander("Logs"):
            st.code(proj_result["stdout"])
            st.code(proj_result["stderr"])
            
