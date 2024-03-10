import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

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
    
    return df



# main function for app's UI/UX
def main():
    st.title('Welcome To Player Recommendation Application')
    st.image("https://cdn.mos.cms.futurecdn.net/y8Z3cKCQ6cZgTZNh5TeKgX.jpg")

    # Add a section for CSV dataset upload
    uploaded_data = upload_file()
    print(uploaded_data.shape)
    processed_df = pre_process(uploaded_data)

    if uploaded_data is not None:
        st.write("Uploaded dataset:")
        st.write(processed_df)

        st.sidebar.subheader("KMeans Clustering")

        # Button to trigger KMeans clustering
        if st.sidebar.button("Run KMeans Clustering"):
            k = st.sidebar.slider("Number of clusters", min_value=2, max_value=10, value=5)

            # Perform KMeans clustering
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(processed_df)

            # Add cluster labels to the dataset
            uploaded_data['Cluster'] = kmeans.labels_

            # Show clustered dataset
            st.write("Clustered dataset:")
            st.write(uploaded_data)

if __name__ == '__main__':
    main()