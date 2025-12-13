import streamlit as st
import pandas as pd
import sqlite3

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="SHINE Research Explorer",
    layout="wide"
)

st.title("📚 SHINE Research Explorer")
st.caption("Browse and search annotated scholarship in distance education")

# --------------------------------------------------
# SQLite connection
# --------------------------------------------------
@st.cache_resource
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
# Safely explode authors & keywords (for filters only)
# --------------------------------------------------
def explode_for_filters(df):
    # Explode authors
    authors_df = (
        df[["authors"]]
        .dropna()
        .assign(author_name=lambda x: x["authors"].str.split(";"))
        .explode("author_name")
    )
    authors_df["author_name"] = authors_df["author_name"].str.strip()

    # Explode keywords
    keywords_df = (
        df[["keywords"]]
        .dropna()
        .assign(keyword=lambda x: x["keywords"].str.split(","))
        .explode("keyword")
    )
    keywords_df["keyword"] = keywords_df["keyword"].str.strip()

    return authors_df[["author_name"]], keywords_df[["keyword"]]


authors_df, keywords_df = explode_for_filters(df)

# --------------------------------------------------
# Sidebar filters
# --------------------------------------------------
st.sidebar.header("🔍 Filters")

authors = ["All"] + sorted(
    authors_df["author_name"]
    .dropna()
    .unique()
    .tolist()
)

keywords = ["All"] + sorted(
    keywords_df["keyword"]
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
# Apply filters (on aggregated dataframe)
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
