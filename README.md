# Scout AI
 
## Overview

Scout-AI is an innovative player recommendation application built using Streamlit. This tool is designed to help scouts, analysts, coaches, and football enthusiasts find players who are similar in style and performance. By leveraging data from Wyscout, one of the leading football analytics platforms, Scout-AI provides insightful recommendations based on advanced clustering algorithms.
Features

    Player Search and Recommendations: Find players who match the style and performance metrics of your target player.
    Data-Driven Insights: Utilize comprehensive data from Wyscout to inform recommendations.
    Interactive User Interface: Streamlit provides a user-friendly and interactive interface to explore player similarities.
    Clustering Algorithm: Advanced clustering techniques are used to group players with similar characteristics and performance metrics.
    Upload Custom Datasets: Users can upload their own datasets for analysis and recommendations.

## Installation

    Clone the repository:

    bash

git clone https://github.com/yourusername/scout-ai.git
cd scout-ai

Install the required dependencies:

bash

pip install -r requirements.txt

Run the application:

bash

    streamlit run app.py

Usage

    Upload Dataset: Upload your custom player dataset in CSV format.
    Input Player Information: Enter the details of the player you want to find similar recommendations for.
    Explore Recommendations: View the list of recommended players along with their stats and similarity scores.
    Detailed Analysis: Click on a recommended player to see a detailed analysis of their performance metrics and how they compare to the target player.

## Data Source

Scout-AI uses data from Wyscout, a leading football analytics platform, and allows users to upload their own datasets. The data includes comprehensive statistics on player performance, which forms the basis for clustering and similarity analysis.
Clustering Methodology

Scout-AI employs advanced clustering algorithms to group players based on their performance metrics. This allows for the identification of players who exhibit similar playing styles and abilities. The clustering process involves:

    Data Preprocessing: Cleaning and normalizing the data to ensure consistency.
    Feature Selection: Identifying key performance metrics that are most indicative of a player's style.
    Clustering: Applying algorithms such as K-means to group players into clusters.
    Similarity Scoring: Calculating similarity scores based on the distance between players within the feature space.