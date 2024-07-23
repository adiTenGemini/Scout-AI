
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

@ st.cache_data
def plot_radar_chart(player_data1, player_data2):
    # Define the attributes for the radar chart
    attributes = list(player_data1.index)

    numeric_cols = player_data1.select_dtypes(include=['int', 'float']).columns.tolist()

    print(player_data1,player_data2)

    playerA,playerB = str(player_data1['Player'].values[0]),str(player_data2['Player'].values[0])
    print('\n','names:',playerA,playerB,'\n')

    values1 = player_data1[numeric_cols].values.tolist()[0]
    values2 = player_data2[numeric_cols].values.tolist()[0]

    # Create the radar chart
    fig = go.Figure()

    # Add traces for both players
    fig.add_trace(go.Scatterpolar(
        r=values1,
        theta=numeric_cols,
        fill='toself',
        name=playerA,  # Name for the first player
        marker=dict(color='rgba(0,0,255,0.5)')
    ))

    fig.add_trace(go.Scatterpolar(
        r=values2,
        theta=numeric_cols,
        fill='toself',
        name=playerB,  # Name for the second player
        marker=dict(color='rgba(255,0,0,0.5)')
    ))

    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True,range=[0,1]),
            
        ),
        showlegend=True  # Show legend to distinguish between players
    )
    
    values1.clear()
    values2.clear()
    return fig

@st.cache_data
def plot_radar_and_bar_chart(player_data1, player_data2):
    # Define the attributes for the radar chart
    attributes = list(player_data1.index)

    numeric_cols = player_data1.select_dtypes(include=['int', 'float']).columns.tolist()

    playerA,playerB = str(player_data1['Player'].values[0]),str(player_data2['Player'].values[0])

    values1 = player_data1[numeric_cols].values.tolist()[0]
    values2 = player_data2[numeric_cols].values.tolist()[0]

    # Create the radar chart
    fig_radar = go.Figure()

    # Add traces for both players
    fig_radar.add_trace(go.Scatterpolar(
        r=values1,
        theta=numeric_cols,
        fill='toself',
        name=playerA,  # Name for the first player
        marker=dict(color='#45474B')
    ))

    fig_radar.add_trace(go.Scatterpolar(
        r=values2,
        theta=numeric_cols,
        fill='toself',
        name=playerB,  # Name for the second player
        marker=dict(color='#ED7D31')
    ))

    # Update layout for radar chart
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True,range=[0,1]),   
        ),
        showlegend=False  # Show legend to distinguish between players
    )

    # Create the bar chart
    fig_bar = go.Figure()

    # Add bar traces for both players
    fig_bar.add_trace(go.Bar(
        x=numeric_cols,
        y=values1,
        name=playerA,
        marker=dict(color='#45474B')
    ))

    fig_bar.add_trace(go.Bar(
        x=numeric_cols,
        y=values2,
        name=playerB, 
        marker=dict(color='#ED7D31')
    ))

    # Update layout for bar chart
    fig_bar.update_layout(
        barmode='group', 
        xaxis=dict(title='Attributes'),
        yaxis=dict(title='Values')
    )

    # Create subplots
    fig = make_subplots(rows=1, cols=2, subplot_titles=[f'Radar Chart - {playerA} vs {playerB}', f'Bar Chart - {playerA} vs {playerB}'],
                        specs=[[{'type': 'polar'}, {'type': 'xy'}]])

    # Add radar chart to subplot
    fig.add_trace(fig_radar.data[0], row=1, col=1)
    fig.add_trace(fig_radar.data[1], row=1, col=1)

    # Add bar chart to subplot
    fig.add_trace(fig_bar.data[0], row=1, col=2)
    fig.add_trace(fig_bar.data[1], row=1, col=2)

    # Update layout for subplots
     # Update layout for subplots
  # Update layout for subplots
    # Update layout for subplots
    fig.update_layout(height=600, width=1000, showlegend=False)

    
    return fig