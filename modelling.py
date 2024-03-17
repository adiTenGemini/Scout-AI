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

def get_next_model_name(folder):
    # Get a list of existing models in the folder
    existing_models = [f for f in os.listdir(folder) if f.endswith('.pkl')]
    return f"model_{len(existing_models) + 1}.pkl"

def model(df):

    numeric_clmns = df.dtypes[df.dtypes != "object"].index 

    player_names = df['Player']
    teams = df['Team']

    cols= list(set(df.columns)-{'Player','Team'})

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


