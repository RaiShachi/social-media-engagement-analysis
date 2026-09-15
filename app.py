import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Social Media Engagement Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    social = pd.read_csv("cleaned_social_media_engagement_dataset.csv")
    virality = pd.read_csv("social_media_virality_analysis.csv")
    comments = pd.read_csv("cleaned_youtube_comments_nlp.csv")
    recommendations = pd.read_csv("platform_recommendations.csv")

    return social, virality, comments, recommendations


social, virality, comments, recommendations = load_data()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("📊 Dashboard Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Executive Overview",
        "Virality & Engagement Analysis",
        "Audience Sentiment & NLP Analysis",
        "Strategy Recommendations"
    ]
)

# ==================================================
# PAGE 1 - EXECUTIVE OVERVIEW
# ==================================================

if page == "Executive Overview":

    st.title("Social Media Engagement Dashboard")
    st.subheader("Executive Overview")

    platforms = sorted(social["Platform"].dropna().unique())

    selected_platforms = st.multiselect(
        "Filter by Platform",
        platforms,
        default=platforms
    )

    filtered = social[
        social["Platform"].isin(selected_platforms)
    ].copy()

    # KPI CARDS
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Posts",
        f"{len(filtered):,}"
    )

    c2.metric(
        "Total Interactions",
        f"{filtered['Total_Interactions'].sum():,.0f}"
    )

    c3.metric(
        "Median Engagement Rate",
        f"{filtered['Engagement_Rate'].median():.2f}"
    )

    c4.metric(
        "Total Views",
        f"{filtered['Views'].sum():,.0f}"
    )

    st.divider()

    # PLATFORM CHART
    platform_engagement = (
        filtered.groupby("Platform")["Engagement_Rate"]
        .median()
        .reset_index()
        .sort_values("Engagement_Rate", ascending=False)
    )

    fig1 = px.bar(
        platform_engagement,
        x="Platform",
        y="Engagement_Rate",
        title="Median Engagement by Platform"
    )

    # CONTENT TYPE CHART
    content_engagement = (
        filtered.groupby("Content_Type")["Engagement_Rate"]
        .median()
        .reset_index()
        .sort_values("Engagement_Rate", ascending=False)
    )

    fig2 = px.bar(
        content_engagement,
        x="Content_Type",
        y="Engagement_Rate",
        title="Median Engagement by Content Type"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    # CATEGORY CHART
    category_engagement = (
        filtered.groupby("Category")["Engagement_Rate"]
        .median()
        .reset_index()
        .sort_values("Engagement_Rate", ascending=False)
    )

    fig3 = px.bar(
        category_engagement,
        x="Category",
        y="Engagement_Rate",
        title="Median Engagement by Category"
    )

    # MONTH CHART
    month_engagement = (
        filtered.groupby("Month")["Engagement_Rate"]
        .median()
        .reset_index()
        .sort_values("Month")
    )

    fig4 = px.line(
        month_engagement,
        x="Month",
        y="Engagement_Rate",
        markers=True,
        title="Median Engagement by Month"
    )

    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.plotly_chart(fig4, use_container_width=True)


# ==================================================
# PAGE 2 - VIRALITY ANALYSIS
# ==================================================

elif page == "Virality & Engagement Analysis":

    st.title("Virality & Engagement Analysis")

    platforms = sorted(virality["Platform"].dropna().unique())

    selected_platforms = st.multiselect(
        "Filter by Platform",
        platforms,
        default=platforms,
        key="viral_platform"
    )

    vdf = virality[
        virality["Platform"].isin(selected_platforms)
    ].copy()

    high_viral = vdf[
        vdf["Viral_Level"].isin(["High", "Very High"])
    ]

    c1, c2 = st.columns(2)

    c1.metric(
        "Median Viral Score",
        f"{vdf['Viral_Score'].median():.2f}"
    )

    c2.metric(
        "High Viral Posts",
        f"{len(high_viral):,}"
    )

    st.divider()

    # CATEGORY HIGH VIRAL RATE
    category_rate = (
        vdf.assign(
            High_Viral=vdf["Viral_Level"].isin(
                ["High", "Very High"]
            ).astype(int)
        )
        .groupby("Category")["High_Viral"]
        .mean()
        .mul(100)
        .reset_index(name="High_Viral_Rate")
        .sort_values("High_Viral_Rate", ascending=False)
    )

    fig1 = px.bar(
        category_rate,
        x="Category",
        y="High_Viral_Rate",
        title="High-Viral Rate by Category"
    )

    # CONTENT TYPE HIGH VIRAL RATE
    content_rate = (
        vdf.assign(
            High_Viral=vdf["Viral_Level"].isin(
                ["High", "Very High"]
            ).astype(int)
        )
        .groupby("Content_Type")["High_Viral"]
        .mean()
        .mul(100)
        .reset_index(name="High_Viral_Rate")
        .sort_values("High_Viral_Rate", ascending=False)
    )

    fig2 = px.bar(
        content_rate,
        x="Content_Type",
        y="High_Viral_Rate",
        title="High-Viral Rate by Content Type"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    # VIRAL LEVEL DISTRIBUTION
    viral_order = ["Low", "Moderate", "High", "Very High"]

    viral_counts = (
        vdf["Viral_Level"]
        .value_counts()
        .reindex(viral_order, fill_value=0)
        .reset_index()
    )

    viral_counts.columns = ["Viral_Level", "Number_of_Posts"]

    fig3 = px.bar(
        viral_counts,
        x="Viral_Level",
        y="Number_of_Posts",
        title="Number of Posts by Viral Level"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Top 10 Viral Posts")

    top10 = (
        vdf.nlargest(10, "Viral_Score")[
            [
                "Post_ID",
                "Platform",
                "Content_Type",
                "Category",
                "Viral_Score",
                "Viral_Level"
            ]
        ]
    )

    st.dataframe(
        top10,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# PAGE 3 - NLP
# ==================================================

elif page == "Audience Sentiment & NLP Analysis":

    st.title("Audience Sentiment & NLP Analysis")

    total_comments = len(comments)

    positive_comments = (
        comments["Sentiment"]
        .astype(str)
        .str.lower()
        .eq("positive")
        .sum()
    )

    relatable_comments = (
        comments["Relatability"]
        .astype(str)
        .str.lower()
        .eq("relatable")
        .sum()
    )

    positive_rate = (
        positive_comments / total_comments * 100
        if total_comments else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Comments",
        f"{total_comments:,}"
    )

    c2.metric(
        "Positive Comments",
        f"{positive_comments:,}"
    )

    c3.metric(
        "Relatable Comments",
        f"{relatable_comments:,}"
    )

    c4.metric(
        "Positive Sentiment %",
        f"{positive_rate:.2f}%"
    )

    st.divider()

    # SENTIMENT DISTRIBUTION
    sentiment_counts = (
        comments["Sentiment"]
        .value_counts()
        .reset_index()
    )

    sentiment_counts.columns = [
        "Sentiment",
        "Number_of_Comments"
    ]

    fig1 = px.bar(
        sentiment_counts,
        x="Sentiment",
        y="Number_of_Comments",
        title="Comments by Sentiment"
    )

    # RELATABILITY DISTRIBUTION
    relatability_counts = (
        comments["Relatability"]
        .value_counts()
        .reset_index()
    )

    relatability_counts.columns = [
        "Relatability",
        "Number_of_Comments"
    ]

    fig2 = px.bar(
        relatability_counts,
        x="Relatability",
        y="Number_of_Comments",
        title="Comments by Relatability"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    # COMMENT LENGTH
    length_by_sentiment = (
        comments.groupby("Sentiment")["Comment_Length"]
        .mean()
        .reset_index()
    )

    fig3 = px.bar(
        length_by_sentiment,
        x="Sentiment",
        y="Comment_Length",
        title="Average Comment Length by Sentiment"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # RELATABLE COMMENTS TABLE
    relatable = comments[
        comments["Relatability"]
        .astype(str)
        .str.lower()
        .eq("relatable")
    ].copy()

    relatable["Index"] = relatable.index + 1

    relatable["Comment Preview"] = (
        relatable["Comment"]
        .astype(str)
        .apply(
            lambda x:
            x[:120] + "..."
            if len(x) > 120
            else x
        )
    )

    st.subheader("Sample Relatable Comments")

    st.dataframe(
        relatable[
            [
                "Index",
                "Comment Preview",
                "Sentiment",
                "Comment_Length"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# PAGE 4 - RECOMMENDATIONS
# ==================================================

elif page == "Strategy Recommendations":

    st.title("Platform Strategy Recommendations")

    platforms = sorted(
        recommendations["Platform"]
        .dropna()
        .unique()
    )

    platform = st.selectbox(
        "Select Platform",
        platforms
    )

    rec = recommendations[
        recommendations["Platform"] == platform
    ].iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Recommended Category",
        rec["Recommended_Category"]
    )

    c2.metric(
        "Recommended Content Type",
        rec["Recommended_Content_Type"]
    )

    c3.metric(
        "Recommended Length",
        rec["Recommended_Length"]
    )

    c4.metric(
        "Suggested Posting Time",
        rec["Suggested_Posting_Time"]
    )

    st.divider()

    c5, c6 = st.columns(2)

    c5.metric(
        "Category Strategy Score",
        f"{rec['Category_Strategy_Score']:.2f}"
    )

    c6.metric(
        "Content Type Strategy Score",
        f"{rec['Content_Type_Strategy_Score']:.2f}"
    )

    st.subheader("Platform Recommendation Summary")

    st.dataframe(
        recommendations[
            recommendations["Platform"] == platform
        ][
            [
                "Platform",
                "Recommended_Category",
                "Recommended_Content_Type",
                "Recommended_Length",
                "Suggested_Posting_Time",
                "Category_Strategy_Score",
                "Content_Type_Strategy_Score"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
