import streamlit as st
import pandas as pd
import numpy as np


####__________________________________________________________________________________________________________________________________________________________________________________________
# class and methods for Player recommdation app

class PlayerRecommendationSystem:

    def __init__(self,gender='Male') -> None:
        """
        init method to initalize the player gender
        i/p : gender
        """
        self.gender=gender


    def get_player_details(self,player_id):

        """
        Get player details like face,club,value,salary
        """

        if self.gender=='Male':
            player_df = pd.read_csv('data/male/players_22.csv', low_memory=False)
        else:
            player_df = pd.read_csv('data/female/female_players_22.csv', low_memory=False)
        
    
        player_df.set_index('sofifa_id',inplace=True)

        player = player_df.loc[player_id]

        player_dict={}  # dictionary to store player details
        
        player_dict['face'] = player['player_face_url'] 
        player_dict['positions'] = player['player_positions']
        player_dict['traits'] = player['player_traits']


        # add club,value and salary for male players since it is unavailble in the dataset 
        if self.gender=='Male':
            player_dict['club'] = player['club_logo_url']
            player_dict['value'] = player['value_eur']
            player_dict['salary'] = player['wage_eur']
        

        return player_dict


    def get_players(self):

        if self.gender=='Male':

            player_df = pd.read_csv('data/player_abilities.csv', low_memory=False)
        else:
            player_df = pd.read_csv('data/female_player_abilities.csv', low_memory=False)
            

        player_ids = list(player_df['sofifa_id'])
        player_names = list(player_df['short_name']+','+player_df['overall'].astype('str'))

        
        player_dict = dict(zip(player_names, player_ids))

        return player_dict

        
    def get_similiar_players(self,player,player_count=5):
        """
        find top 5 similiar players
        i/p: player_id
        """

        player_name = player.split(',')[0]
        overall = player.split(',')[1]

        # male players
        if(self.gender=='Male'):

            PCA_components = pd.read_csv('models/male_pca_result.csv', low_memory=False)
            pl_df          = pd.read_csv('models/male_pl_df.csv', low_memory=False)

        # female players
        else:
            PCA_components = pd.read_csv('models/female_pca_result.csv', low_memory=False)
            pl_df          = pd.read_csv('models/female_pl_df.csv', low_memory=False)
        
        # get player id
        playerA_id = PCA_components[(pl_df['name']==str(player_name)) & (pl_df['overall']==int(overall))]['sofifa_id'].item()

        # set sofifa_id as index fro both dataframes
        pl_df.set_index('sofifa_id',inplace=True)
        PCA_components.set_index('sofifa_id',inplace=True)

        n_clusters = list(PCA_components['pred_labels'].unique())

        cluster_dict = {i: pl_df.index[PCA_components['pred_labels']==i].tolist() for i in range(len(n_clusters))}

    
        # find the cluster the player belongs
        cluster = PCA_components.loc[playerA_id]['pred_labels']

        # get the features of playerA
        playerA_data = PCA_components.loc[playerA_id].head()

        
        # get the other players in the same cluster
        cluster_indices = cluster_dict[cluster]


        # get the other players in the same cluster
        cluster_indices = cluster_dict[cluster]

        # initialise a temp dictionary to store player ids and distances
        dist_dict={}

        # iterate through each player in the cluster
        for player_id in cluster_indices:

            if(player_id != playerA_id):

            
                playerB_data = PCA_components.loc[player_id].head()
                dist = np.linalg.norm(playerA_data-playerB_data)
                dist_dict[player_id]=dist.round(4)
            
        
        # create a new dataframe to show the id and distance
        dist_df = pd.DataFrame(columns=['id','distance'])

        # add data to the dataframe
        dist_df['id'] = dist_dict.keys()
        dist_df['distance'] = dist_dict.values()
        dist_df.sort_values('distance',inplace=True) # sorts the dataframe based on distance

        # shortlist players based on player count
        similiar_players = dist_df.head(player_count)
        
        name_list=[]

        for id in list(similiar_players['id']):
            name_list.append(pl_df.loc[id]['name'])

        similiar_players['name'] =name_list

        return similiar_players


        
       
####__________________________________________________________________________________________________________________________________________________________________________________________
# main function for app's UI/UX


def display_PlayerDetails(player_name,player_info,gender):
    """
    displays basic info of chosen player
    """

    st.image(player_info['face'])        # shows player face
    st.header(player_name.split(',')[0]) # shows player name


    # Male Players info
    if gender=="Male":

        col1, col2, col3 = st.columns(3) # creates 3 columns

        with col1:
            st.subheader('Current Club') 
            st.image(player_info['club']) # shows club logo

        with col2:
            st.subheader('Positions')          
            st.write(player_info['positions']) # shows player positions

        with col3:
            st.subheader('Special Traits')
            st.write(player_info['traits']) # shows special traits

    # Female Players info
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Positions')
            st.write(player_info['positions']) # shows player positions

        with col2:
            
            st.subheader('Special Traits')
            st.write(player_info['traits'])    # shows special traits


def main():
    st.title('Welcome To Player Reccomendation Application')
    st.image("https://cdn.mos.cms.futurecdn.net/y8Z3cKCQ6cZgTZNh5TeKgX.jpg")


    # instruction section
    st.subheader('Instructions', anchor=None)

    instructions = "Choose the player you want to replace and the model will give you a list of most similiar players"
    st.markdown(instructions)


    # gets gender as input
    gender = st.sidebar.radio("Select gender",('Male', 'Female'))

    player_count = st.sidebar.slider('How many similiar player do you want?', 0, 15, 5)

    # creates a new object of the PlayerRecommendationSystem class with the gender
    app = PlayerRecommendationSystem(gender=gender)

    # gets the player names and their id
    player_dict = app.get_players()

    # list of player names
    data_split_names = list(player_dict.keys())

    # select player from selectbox
    player_name = st.sidebar.selectbox(
            "Select Players", data_split_names
            )
    # retrieves player id using the player name
    player_id = player_dict[player_name]

    # button onclick action
    if st.sidebar.button('Find Players'):

        # gets a datframe containing similiar players and a similiarity score
        similiar_players = app.get_similiar_players(player=player_name,player_count=player_count)

        similiar_players.rename(columns={'name':'Player Name','distance':'Similarity Score'},inplace=True)

        # get player details
        player_info = app.get_player_details(player_id)


        st.header("Here is the player you've selected")
        
        # displays basic info of chosen player
        display_PlayerDetails(player_name,player_info,gender)

        st.info('The ideal replacement is '+similiar_players.iloc[0]['Player Name'])

        st.header("Here are the most similiar players")


      
        # dispays table of similiar players
        st.table(similiar_players[['Player Name','Similarity Score']])


        st.caption('*Lower the score, Greater the similarity')


if __name__ == '__main__':

    main()

   
        
