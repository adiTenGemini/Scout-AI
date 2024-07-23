from flask import Flask, render_template, request
import pandas as pd
import modelling
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import chart


app = Flask(__name__)

# Function to preprocess data
def pre_process(df):
    # Define a dictionary comprehension to create the new column names
    col_names = {col_name: col_name.replace(',', '').replace(' ', '_') for col_name in df.columns}
    
    # Rename the columns using the generated dictionary
    df.rename(columns=col_names, inplace=True)

    

    # Split the position column into primary, secondary, and tertiary position columns
    df[['Primary_Position', 'Secondary_Position', 'Tertiary_Position']] = df['Position'].str.split(',', expand=True)

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

    return df

def load_dataset():
    if 'file' not in request.files:
        return None, "No file part"

    file = request.files['file']

    if file.filename == '':
        return None, "No selected file"

    if file:
        try:
            # Try reading the file as CSV
            df = pd.read_csv(file, encoding='utf-8')
            return df, "File successfully uploaded as CSV!"
        except UnicodeDecodeError:
            pass
        except pd.errors.ParserError:
            pass

        try:
            # Try reading the file as Excel
            df = pd.read_excel(file)
            return df, "File successfully uploaded as Excel!"
        except pd.errors.ParserError:
            pass

        # If unable to read as CSV or Excel, show error message
        return None, "Unable to read the file. Please check the file format or try another file."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = load_dataset(file)
            if df is not None:
                processed_df = pre_process(df)
                return render_template('dashboard.html', df=processed_df.to_html())

    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        selected_player = request.form['selected_player']
        selected_team = request.form['selected_team']
        similar_players = request.form.getlist('similar_players')
        processed_df = pd.read_html(request.form['df'])[0]

        # Run KMeans clustering and find most similar players
        # (Similar code as before)
        # Find the most similar players
        similar_players = modelling.find_similar_players(selected_player, selected_team, processed_df, top_n=10)

        # Plot radar chart for selected players
        chart.plot_radar_chart(similar_players, processed_df)

    return render_template('dashboard.html')



if __name__ == '__main__':
    app.run(debug=True)
