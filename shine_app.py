import streamlit as st
import pandas as pd
import sqlite3

import os
st.write("Current working directory:", os.getcwd())
st.write("Files in directory:", os.listdir("."))

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="SHINE Research Explorer",
    layout="wide"
)

st.title("SHINE Research Explorer")

# -----------------------------
# SQLite connection
# -----------------------------
@st.cache_resource
def get_connection():
    return sqlite3.connect("shine.db", check_same_thread=False)

conn = get_connection()
st.write("Inspecting SQLite tables:")

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
)

st.write(tables)

# -----------------------------
# Load data from SQLite
# -----------------------------
@st.cache_data
def load_data():
    query = "SELECT * FROM research_search"
    return pd.read_sql(query, conn)

df = load_data()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("🔍 Filters")

authors = ["All"] + sorted(df["authors"].dropna().unique().tolist())
keywords = ["All"] + sorted(df["keywords"].dropna().unique().tolist())

selected_author = st.sidebar.selectbox("Author", authors)
selected_keyword = st.sidebar.selectbox("Keyword", keywords)

min_year = int(df["publication_year"].min())
max_year = int(df["publication_year"].max())

year_range = st.sidebar.slider(
    "Publication Year",
    min_year,
    max_year,
    (min_year, max_year)
)

search_text = st.sidebar.text_input("Search title or annotation")

# -----------------------------
# Apply filters
# -----------------------------
filtered_df = df.copy()

if selected_author != "All":
    filtered_df = filtered_df[
        filtered_df["authors"].str.contains(selected_author, na=False)
    ]

if selected_keyword != "All":
    filtered_df = filtered_df[
        filtered_df["keywords"].str.contains(selected_keyword, na=False)
    ]

filtered_df = filtered_df[
    (filtered_df["publication_year"] >= year_range[0]) &
    (filtered_df["publication_year"] <= year_range[1])
]

if search_text:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search_text, case=False, na=False) |
        filtered_df["annotation"].str.contains(search_text, case=False, na=False)
    ]

# -----------------------------
# Featured vs search logic (Top 2)
# -----------------------------
show_featured_only = (
    not search_text
    and selected_author == "All"
    and selected_keyword == "All"
)

if show_featured_only:
    display_df = (
        filtered_df
        .sort_values(
            by=["publication_year", "source_timestamp"],
            ascending=False
        )
        .head(2)
    )
    st.subheader("Featured Research")
else:
    display_df = filtered_df
    st.subheader(f"Results ({len(display_df)})")

# -----------------------------
# Display results
# -----------------------------
if display_df.empty:
    st.info("No results match the selected filters.")
else:
    for _, row in display_df.iterrows():
        with st.expander(row["title"]):
            st.markdown(f"**Authors:** {row['authors']}")
            st.markdown(f"**Publication Year:** {row['publication_year']}")
            st.markdown(f"**Source:** {row['source']}")
            st.markdown(f"**Keywords:** {row['keywords']}")
            st.markdown(f"**Methodology:** {row['methodology']}")
            st.markdown("---")
            st.markdown("**Annotation:**")
            st.write(row["annotation"])


