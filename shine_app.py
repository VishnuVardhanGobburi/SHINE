import streamlit as st
import pandas as pd
import sqlite3

# Page config
st.set_page_config(
    page_title="SHINE Research Explorer",
    layout="wide"
)

st.title("SHINE Research Explorer")
st.caption("Browse and search annotated scholarship in distance education")

# SQLite connection
def get_connection():
    return sqlite3.connect("shine1.db", check_same_thread=False)

conn = get_connection()

# --------------------------------------------------
# Load aggregated data from SQLite
# --------------------------------------------------
@st.cache_data
def load_data():
    query = "SELECT * FROM research_search"
    return pd.read_sql(query, conn)

df = load_data()

# --------------------------------------------------
# Create exploded dataframe for filters
# --------------------------------------------------
def explode_for_filters(df):
    exploded = df.copy()

    exploded["author_name"] = (
        exploded["authors"]
        .fillna("")
        .str.split(";")
        .explode()
        .str.strip()
    )

    exploded["keyword"] = (
        exploded["keywords"]
        .fillna("")
        .str.split(",")
        .explode()
        .str.strip()
    )

    return exploded

exploded_df = explode_for_filters(df)

# --------------------------------------------------
# Sidebar filters
# --------------------------------------------------
st.sidebar.header("🔍 Filters")

authors = ["All"] + sorted(
    exploded_df["author_name"]
    .replace("", pd.NA)
    .dropna()
    .unique()
    .tolist()
)

keywords = ["All"] + sorted(
    exploded_df["keyword"]
    .replace("", pd.NA)
    .dropna()
    .unique()
    .tolist()
)

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

# --------------------------------------------------
# Apply filters (on aggregated df)
# --------------------------------------------------
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

# --------------------------------------------------
# Featured vs Search logic
# --------------------------------------------------
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
    st.subheader("🌟 Featured Research")
else:
    display_df = filtered_df
    st.subheader(f"Results ({len(display_df)})")

# --------------------------------------------------
# Display results
# --------------------------------------------------
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

