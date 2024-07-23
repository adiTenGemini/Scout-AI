import streamlit as st
import pandas as pd
import numpy as np
import modelling
from sklearn.cluster import KMeans
import chart



# Define the PlayerRecommendationSystem class and methods

# Define a function to handle the file upload and automatically determine the file type
def upload_file():
    st.sidebar.subheader("Upload Dataset")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            # Try reading the file as CSV
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            st.sidebar.success("File successfully uploaded as CSV!")
            return df
        except UnicodeDecodeError:
            pass
        except pd.errors.ParserError:
            pass

        try:
            # Try reading the file as Excel
            df = pd.read_excel(uploaded_file)
            st.sidebar.success("File successfully uploaded as Excel!")
            return df
        except pd.errors.ParserError:
            pass

        # If unable to read as CSV or Excel, show error message
        st.sidebar.error("Unable to read the file. Please check the file format or try another file.")
        return None
    else:
        return None


def pre_process(df):
    # Define a dictionary comprehension to create the new column names
    col_names = {col_name: col_name.replace(',', '').replace(' ', '_') for col_name in df.columns}
    
    # Rename the columns using the generated dictionary
    df.rename(columns=col_names, inplace=True)

    

    # Split the position column into primary, secondary, and tertiary position columns
    df[['Primary_Position', 'Secondary_Position', 'Tertiary_Position']] = df['Position'].str.split(',', expand=True)

    df[['Aerial_duels_per_90.1', 'Free_kicks_per_90',
       'Direct_free_kicks_per_90', 'Direct_free_kicks_on_target_%',
       'Corners_per_90', 'Penalties_taken', 'Penalty_conversion_%']]=df[['Aerial_duels_per_90.1', 'Free_kicks_per_90',
                                                    'Direct_free_kicks_per_90', 'Direct_free_kicks_on_target_%',
                                                    'Corners_per_90', 'Penalties_taken', 'Penalty_conversion_%']].fillna(0)
     
    
    # Calculate the percentage of null values in each column
    null_percentage = df.isnull().mean()

    # Filter columns where null percentage is greater than the threshold
    cols_to_drop = null_percentage[null_percentage > 0.5].index.tolist()

    # Drop the selected columns from the DataFrame
    df = df.drop(columns=cols_to_drop)

    numeric_cols = df.select_dtypes(include=['int', 'float']).columns.tolist()
    # Fill missing values with median values for players in the same primary position
    for col in numeric_cols:
        df[col] = df.groupby('Primary_Position')[col].transform(lambda x: x.fillna(x.median()))

    df=df.fillna(0)
    print(list(df.columns))
    return df

# Define a function to display player select dropdown based on team selection
def select_player_by_team(df):
    selected_team = st.sidebar.selectbox("Select Team", df['Team'].unique())

    players_in_selected_team = df[df['Team'] == selected_team]['Player'].unique()

    selected_player = st.sidebar.selectbox("Select Player", players_in_selected_team)

    return selected_player


# Define a function to display player select dropdown based on team selection
def select_player_by_team(df):
    selected_team = st.sidebar.selectbox("Select Team", df['Team'].unique())

    players_in_selected_team = df[df['Team'] == selected_team]['Player'].unique()

    selected_player = st.sidebar.selectbox("Select Player", players_in_selected_team)

    return selected_player,selected_team

# Define a function to display player select dropdown based on team selection
def selectSimiliarPlayer(df):
    
    similiar_player = st.sidebar.selectbox("Select Player", df['Player'])

    return similiar_player


def comparePlayers(processed_df, selected_player, selected_similar_players, imp_cols):
    st.subheader("Radar Chart for Comparison")

    initial_player_data = processed_df[processed_df['Player'] == selected_player][imp_cols]

    for similar_player in selected_similar_players:
        st.write(f"Comparison with {similar_player}:")
        selected_similar_player_data = processed_df[processed_df['Player'] == similar_player][imp_cols]
        fig = chart.plot_radar_chart(selected_similar_player_data, initial_player_data)
        st.plotly_chart(fig)



@st.cache_data
def preprocess_and_cluster_data(data):
    processed_df = pre_process(data)
    model = modelling.model(processed_df)
    processed_df['Cluster'] = model.labels_
    return processed_df

# Define the main function for app's UI/UX
def main():
    # Initialize session state variable to store similar players
    if 'similar_players' not in st.session_state:
        st.session_state.similar_players = []

    st.title('Welcome To ScoutAI')


    # Add a section for CSV dataset upload
    uploaded_data = upload_file()

    if uploaded_data is not None:
        processed_df = pre_process(uploaded_data)

        if processed_df is not None:
            # st.write("Uploaded dataset:")
            # st.write(processed_df)

            st.sidebar.subheader("KMeans Clustering")

            # Add player select dropdown based on team selection
            selected_player, selected_team = select_player_by_team(processed_df)
            st.write("Selected Player:", selected_player)

            st.sidebar.subheader("KMeans Clustering")

            # Button to trigger KMeans clustering
            if st.sidebar.button("Run KMeans Clustering"):
                k = st.sidebar.slider("Number of clusters", min_value=2, max_value=10, value=5)

                model = modelling.model(processed_df)

                # Add cluster labels to the dataset
                processed_df['Cluster'] = model.labels_

                # Find the most similar players
                most_similar_players = modelling.find_similar_players(selected_player, selected_team, processed_df, top_n=10)

                # Show table of most similar players
                st.write("10 Most Similar Players:")
                st.write(most_similar_players)

                # Update similar players session state variable
                st.session_state.similar_players = most_similar_players['Player'].tolist()

            # Define important columns for radar chart comparison
            imp_cols = ['Successful_attacking_actions_per_90', 'Goals_per_90', 'Non-penalty_goals_per_90',
                        'xG_per_90', 'Assists_per_90', 'Crosses_per_90', 'Accurate_crosses_%', 'Dribbles_per_90']

            percentile_df = modelling.get_percentile(processed_df,imp_cols)

            imp_cols.append('Player')
            # Multi-select box to choose most similar players
            selected_similar_players = st.multiselect("Select Most Similar Players", st.session_state.similar_players)

            if selected_similar_players:
                for player in selected_similar_players:
                    st.subheader(f"Radar Chart Comparison between {selected_player} and {player}")
                    selected_similar_player_data = percentile_df[percentile_df['Player'] == player][imp_cols]
                    initial_player_data = percentile_df[percentile_df['Player'] == selected_player][imp_cols]

                    #fig = chart.plot_radar_chart(selected_similar_player_data, initial_player_data)
                    fig = chart.plot_radar_and_bar_chart(selected_similar_player_data, initial_player_data)
                    st.plotly_chart(fig)

    else:
        st.write("Uploaded data is None.")

if __name__ == '__main__':
    main()
    # processed_df, selected_player, imp_cols = main()
    # if selected_player is not None:
    #     handle_comparison(processed_df, selected_player, imp_cols)