import streamlit as st
from nfl_projections import project_week

st.title("🏈 DFS Command Center - Step 2 Test")

if st.button("Run Week 3 Projections"):
    with st.spinner("Training model and projecting Week 3... This may take a few minutes on the first run."):
        # This single function builds a service, projects the week, and returns a DataFrame
        df = project_week(2025, 3, quantiles=True) # Use 2025 for the current season, 3 for Week 3[reference:3]
    
    st.success("Projections complete!")
    st.dataframe(df)
