import streamlit as st
import pandas as pd
import pyodbc

# Page config
st.set_page_config(
    page_title="SHINE Research Explorer",
    layout="wide"
)

st.title("SHINE Research Explorer")

# Database connection
def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=SHINE_DB;"
        "UID=shine_user;"
        "PWD=Qweasdzxc@2811"
    )

conn = get_connection()

# Load data
def load_search_data():
    query = """
        SELECT *
        FROM shine_transformed.vw_research_search
    """
    return pd.read_sql(query, conn)


def load_filter_data():
    query = """
        SELECT DISTINCT
            author_name,
            keyword
        FROM shine_transformed.vw_research_exploded
    """
    return pd.read_sql(query, conn)

df = load_search_data()
filters_df = load_filter_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

authors = ["All"] + sorted(filters_df["author_name"].dropna().unique().tolist())
keywords = ["All"] + sorted(filters_df["keyword"].dropna().unique().tolist())

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

# Apply filters
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

# Results
st.subheader(f"Results ({len(filtered_df)})")

if filtered_df.empty:
    st.info("No results match the selected filters.")
else:
    for _, row in filtered_df.iterrows():
        with st.expander(row["title"]):
            st.markdown(f"**Authors:** {row['authors']}")
            st.markdown(f"**Publication Year:** {row['publication_year']}")
            st.markdown(f"**Source:** {row['source']}")
            st.markdown(f"**Keywords:** {row['keywords']}")
            st.markdown(f"**Methodology:** {row['methodology']}")
            st.markdown("---")
            st.markdown("**Annotation:**")
            st.write(row["annotation"])
