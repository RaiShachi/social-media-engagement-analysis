# Social Media Engagement Analysis & Recommendation System

## Project Overview
This project analyzes social media engagement data to identify patterns in audience interaction, virality, sentiment, and content performance.

The project includes data cleaning, exploratory data analysis, virality scoring, statistical testing, sentiment analysis using NLP, relatability detection, and a platform-specific recommendation engine.

A Power BI dashboard is included to present the major insights interactively.

## Project Modules

1. Data Cleaning & EDA
   - Cleaned and prepared the social media engagement dataset
   - Examined engagement, views, interactions, categories, platforms, and content types

2. Virality Analysis
   - Created Viral Score and Viral Level
   - Identified High and Very High viral posts
   - Compared virality across categories and content types

3. Statistical Testing
   - Compared engagement for short vs long content
   - Tested media vs no-media engagement
   - Evaluated posting-time differences using statistical tests

4. NLP Sentiment Analysis
   - Cleaned YouTube comment data
   - Built a TF-IDF based sentiment classification model
   - Classified comments as Positive, Neutral, or Negative
   - Added relatability detection for audience comments

5. Recommendation Engine
   - Generates platform-specific recommendations for:
     - Content category
     - Content type
     - Content length
     - Suggested posting time
   - Uses historical engagement, virality, shares, saves, and statistical findings

## Power BI Dashboard

The Power BI dashboard contains four pages:

- Executive Overview
- Virality & Engagement Analysis
- Audience Sentiment & NLP Analysis
- Strategy Recommendations

## Main Files

- `01_Data_Cleaning_EDA.ipynb`
- `02_Virality_Analysis.ipynb`
- `03_AB_Testing.ipynb`
- `04_NLP_Sentiment_Analysis.ipynb`
- `05_Recommendation_Engine.ipynb`
- `Social_Media_Engagement_Dashboard.pbix`
- `cleaned_social_media_engagement_dataset.csv`
- `social_media_virality_analysis.csv`
- `cleaned_youtube_comments_nlp.csv`
- `platform_recommendations.csv`
- `sentiment_model.pkl`
- `tfidf_vectorizer.pkl`

## Tools & Technologies

Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, SciPy, NLP, TF-IDF, Power BI

## Final Outcome

The project provides an end-to-end analytical workflow for understanding social media performance and generating data-driven content strategy recommendations.