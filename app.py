import streamlit as st
import pandas as pd
from indeed_scraper import scrape_indeed

st.set_page_config(page_title="Live Job Tracker", layout="wide")

st.title("💼 Live Job Tracker Dashboard")

with st.sidebar:
    st.header("🔍 Search Filters")
    role = st.text_input("Job Title", value="data analyst")
    location = st.text_input("Location", value="remote")
    pages = st.slider("Number of pages to scrape", 1, 10, 3)
    search_button = st.button("🚀 Search Jobs")

if search_button:
    st.info(f"Scraping Indeed for '{role}' jobs in '{location}'...")
    df = scrape_indeed(role=role, location=location, pages=pages)

    if df.empty:
        st.warning("No jobs found. Try different keywords.")
    else:
        st.success(f"✅ Found {len(df)} job listings!")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", data=csv, file_name="jobs.csv", mime="text/csv")
