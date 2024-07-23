import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
import time
import pickle
import os
from sklearn import metrics
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


class PlayerSimilarityModel:
    def __init__(self, data):
        self.data = data
        self.clustered_data = None

    def run_kmeans_clustering(self, k=5):
        # Perform KMeans clustering
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(self.data.drop(['Team', 'Player'], axis=1))

        # Add cluster labels to the dataset
        self.clustered_data = self.data.copy()
        self.clustered_data['Cluster'] = kmeans.labels_

    # def find_similar_players(self, selected_team, selected_player, top_n=10):
    #     if self.clustered_data is None:
    #         raise ValueError("Clustering has not been performed. Please run KMeans clustering first.")

    #     # Find the most similar players to the selected player in the same cluster
    #     selected_player_data = self.clustered_data[(self.clustered_data['Player'] == selected_player) & (self.clustered_data['Team'] == selected_team)]

    #     cluster_indices = self.clustered_data.index[(self.clustered_data['Player'] == selected_player) & (self.clustered_data['Team'] == selected_team)]

    #     dist_dict = {}
    #     for player_id in cluster_indices:
    #         if player_id != selected_player:
    #             player_data = self.clustered_data.loc[player_id]
    #             dist = np.linalg.norm(selected_player_data - player_data)
    #             dist_dict[player_id] = dist

    #     most_similar_players_ids = sorted(dist_dict, key=dist_dict.get)[:top_n]
    #     most_similar_players = self.clustered_data.loc[most_similar_players_ids]

    #     return most_similar_players


def get_next_model_name(folder):
    
    # Get a list of existing models in the folder
    existing_models = [f for f in os.listdir(folder) if f.endswith('.pkl')]
    return f"model_{len(existing_models) + 1}.pkl"

# Define a function to find the most similar players to the selected player in the same cluster
def find_similar_players(selected_player, selected_team, processed_df, top_n=10):
    # Filter the DataFrame to get data for the selected player and team
    selected_player_data = processed_df[(processed_df['Player'] == selected_player) & 
                                        (processed_df['Team'] == selected_team)]

    # Get the indices of players in the same cluster as the selected player
    cluster_indices = processed_df.index[processed_df['Cluster'] == selected_player_data['Cluster'].iloc[0]]

    

    # Filter the DataFrame to include only players in the same cluster
    cluster_df = processed_df.loc[cluster_indices]

    print('\n',cluster_df)
    # Initialize a dictionary to store distances between players
    dist_dict = {}

    # Select numeric columns for distance calculation
    numeric_cols = cluster_df.select_dtypes(include=['int', 'float']).columns.tolist()

    numeric_cols=list(set(numeric_cols)-{'Age', 'Market_value', 'Matches_played', 'Minutes_played'} )

    # Iterate through each player in the cluster
    # Iterate through each player index in the cluster
    # Iterate through each player index in the cluster
    for player_ix in cluster_indices:
        if player_ix != selected_player_data.index:  # Exclude the selected player
            # Calculate the distance between the selected player and other players in the cluster
            playerA_data = selected_player_data[numeric_cols].values
            playerB_data = cluster_df.loc[player_ix, numeric_cols].values
            dist = np.linalg.norm(playerA_data - playerB_data)
            # Store both player name and team name in dist_dict
            dist_dict[(cluster_df.loc[player_ix, 'Player'], cluster_df.loc[player_ix, 'Team'])] = dist.round(4)


    print('\n',dist_dict)

    # Convert dist_dict to a DataFrame
    dist_df = pd.DataFrame(list(dist_dict.items()), columns=['Player_Team', 'Distance'])
    dist_df[['Player', 'Team']] = pd.DataFrame(dist_df['Player_Team'].tolist(), index=dist_df.index)
    dist_df.drop(columns=['Player_Team'], inplace=True)

    # Sort the DataFrame by distance
    dist_df.sort_values(by='Distance', inplace=True)

    return dist_df

def get_percentile(df, cols):

    new_cols = ['Player', 'Team']

    # Create a new DataFrame with Player and Team columns
    df_new = df[new_cols].copy()

    for col in cols:
        col_name = col
        new_cols.append(col_name)
        percentile_data = df[col].rank(pct=True)
        df_new[col_name] = percentile_data

    return df_new

def model(df):

    numeric_clmns = df.dtypes[df.dtypes != "object"].index 

    player_names = df['Player']
    teams = df['Team']

    cols= list(set(df.columns)-{'Age', 'Market_value', 'Matches_played', 'Minutes_played'}-{'Player','Team','Team_within_selected_timeframe', 'Passport_country', 'On_loan', 'Position', 'Birth_country', 'Foot', 'Contract_expires','Tertiary_Position', 'Primary_Position', 'Secondary_Position','Height', 'Weight'})

    print(df[cols].isnull().sum())
    pl_df = df[numeric_clmns]

    model = KMeans(n_clusters=20, random_state=124)
    model.fit(pl_df[cols])

    # pred_labels = km.labels_ 
    # pl_df["pred_labels"] = pred_labels

    # Get the next model name
    model_name = get_next_model_name("models")

    # Save the model using pickle
    with open(os.path.join("models", model_name), "wb") as f:
        pickle.dump(model, f)

    return model


