import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="South Korea Top 50 Dashboard",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 South Korea Top 50 Playlist Dashboard")
st.write("Analyze Comeback Momentum, Re-entry Behaviour and Fandom Intensity.")

# -----------------------------
# Upload Dataset
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Final_SouthKorea_Analysis.csv",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("Dataset Loaded Successfully!")

    # -----------------------------
    # Sidebar Filters
    # -----------------------------
    st.sidebar.header("Filters")

    artist = st.sidebar.selectbox(
        "Select Artist",
        ["All"] + sorted(df["artist"].unique().tolist())
    )

    album = st.sidebar.selectbox(
        "Album Type",
        ["All"] + sorted(df["album_type"].unique().tolist())
    )

    momentum = st.sidebar.selectbox(
        "Momentum Level",
        ["All"] + sorted(df["Momentum_Level"].unique().tolist())
    )

    explicit = st.sidebar.selectbox(
        "Explicit Songs",
        ["All", True, False]
    )

    filtered = df.copy()

    if artist != "All":
        filtered = filtered[filtered["artist"] == artist]

    if album != "All":
        filtered = filtered[filtered["album_type"] == album]

    if momentum != "All":
        filtered = filtered[filtered["Momentum_Level"] == momentum]

    if explicit != "All":
        filtered = filtered[filtered["is_explicit"] == explicit]

    # -----------------------------
    # KPI Cards
    # -----------------------------
    st.header("📊 Key Performance Indicators")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Songs",
        filtered["song"].nunique()
    )

    c2.metric(
        "Total Artists",
        filtered["artist"].nunique()
    )

    c3.metric(
        "Average Popularity",
        round(filtered["avg_popularity"].mean(),2)
    )

    c4.metric(
        "Average Momentum",
        round(filtered["momentum_score_final"].mean(),2)
    )

    st.markdown("---")

    # -----------------------------
    # Dataset Preview
    # -----------------------------
    st.subheader("Dataset Preview")

    st.dataframe(filtered)

    st.markdown("---")

    # -----------------------------
    # Top Artists
    # -----------------------------
    st.subheader("🎤 Top Artists by Momentum Score")

    artist_score = (
        filtered.groupby("artist")["momentum_score_final"]
        .mean()
        .reset_index()
        .sort_values(
            "momentum_score_final",
            ascending=False
        )
        .head(15)
    )

    fig1 = px.bar(
        artist_score,
        x="momentum_score_final",
        y="artist",
        orientation="h",
        color="momentum_score_final"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Momentum Level Distribution
    # -----------------------------
    st.subheader("🚀 Momentum Level Distribution")

    fig2 = px.histogram(
        filtered,
        x="Momentum_Level",
        color="Momentum_Level"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Album Type
    # -----------------------------
    st.subheader("💿 Album Type Distribution")

    fig3 = px.pie(
        filtered,
        names="album_type"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Explicit Songs
    # -----------------------------
    st.subheader("🎧 Explicit vs Non Explicit")

    fig4 = px.pie(
        filtered,
        names="is_explicit"
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Top Songs
    # -----------------------------
    st.subheader("🏆 Top 10 Songs")

    top_song = (
        filtered.sort_values(
            "momentum_score_final",
            ascending=False
        )
        [["song",
          "artist",
          "momentum_score_final"]]
        .head(10)
    )

    fig5 = px.bar(
        top_song,
        x="momentum_score_final",
        y="song",
        color="artist",
        orientation="h"
    )

    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Search Song
    # -----------------------------
    st.subheader("🔍 Search Song")

    search = st.text_input(
        "Enter Song Name"
    )

    if search:

        result = filtered[
            filtered["song"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

        st.dataframe(result)

    st.markdown("---")

    # -----------------------------
    # Download Dataset
    # -----------------------------
    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Filtered Dataset",
        csv,
        "Filtered_Dataset.csv",
        "text/csv"
    )

else:

    st.info("Please upload Final_SouthKorea_Analysis.csv")


