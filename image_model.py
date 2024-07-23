import pandas as pd
from pandasql import sqldf

# Sample DataFrames (replace with your actual datasets)
fifa_players_df = pd.DataFrame({
    'Player': ['L. Messi', 'Cristiano Ronaldo', 'Neymar Jr'],
    'Team': ['Barcelona', 'Juventus', 'Paris SG'],
    'Overall': [93, 92, 91]
})

image_links_df = pd.DataFrame({
    'Player Name': ['Lionel Messi', 'Cristiano Ronaldo', 'Neymar'],
    'Image Link': ['http://example.com/messi.jpg', 'http://example.com/ronaldo.jpg', 'http://example.com/neymar.jpg']
})

# Function to execute SQL-like queries
pysqldf = lambda q: sqldf(q, globals())

# SQL-like join operation using player name similarity
query = """
    SELECT fifa_players_df.Player, fifa_players_df.Team, fifa_players_df.Overall,
           image_links_df.[Player Name] AS Player_Name, image_links_df.[Image Link]
    FROM fifa_players_df
    JOIN image_links_df ON fifa_players_df.Player LIKE '%' || image_links_df.[Player Name] || '%'
"""

# Execute the query
joined_df = pysqldf(query)

# Display the result
print(joined_df)
