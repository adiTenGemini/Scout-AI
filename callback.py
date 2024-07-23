import streamlit as st

# Define a function to be called when the selectbox value changes
def on_selectbox_change(selected_option):
    st.write(f"Selected option: {selected_option}")

    # Define options for the second selectbox based on the selected option from the first selectbox
    options = [str(int(selected_option) * i) for i in range(1, 5)]

    # Create the second selectbox with updated options
    selected_option2 = st.selectbox("Select an option", options)

    # Print the selected option from the second selectbox
    st.write(f"Selected option 2: {selected_option2}")

# Create the first selectbox widget
selected_option1 = st.selectbox("Select an option", ["1", "2", "3"])

# Call the on_selectbox_change function when the first selectbox value changes
on_selectbox_change(selected_option1)
