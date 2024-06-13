import streamlit as st
import pandas as pd
import plotly.express as px

# Read CSV data
df = pd.read_csv('mortality_rates.csv')

# Function to calculate cumulative survival probability
def calculate_cumulative_survival_probability(row):
    cumulative_survival_probability = 1.0
    for age in range(1, row['Age'] + 1):
        mortality_rate = row[f'Mortality Rate at {age}']  # Adjust column name accordingly
        cumulative_survival_probability *= (1 - mortality_rate)
    return cumulative_survival_probability

# Apply the function to each row and store the results in a new column
df['Cumulative Survival Probability'] = df.apply(calculate_cumulative_survival_probability, axis=1)

# Title of the Streamlit app
st.title('Mortality Rates Analysis')

# Sidebar for user input
st.sidebar.header('Filter Data')
selected_sex = st.sidebar.selectbox('Sex', df['Sex'].unique())
selected_quality_of_life = st.sidebar.slider('Quality of Life Index', 1, 10, (1, 10))
selected_age = st.sidebar.slider('Age', int(df['Age'].min()), int(df['Age'].max()), (int(df['Age'].min()), int(df['Age'].max())))

# Filter data based on user selection
filtered_data = df[(df['Sex'] == selected_sex) & 
                   (df['Quality of Life Index'] >= selected_quality_of_life[0]) & 
                   (df['Quality of Life Index'] <= selected_quality_of_life[1]) &
                   (df['Age'] >= selected_age[0]) & 
                   (df['Age'] <= selected_age[1])]

# Display filtered data
if st.checkbox('Show Filtered Data'):
    st.subheader('Filtered Data:')
    st.write(filtered_data)

# Create interactive charts
st.sidebar.header('Select Chart Type')
chart_type = st.sidebar.radio('Chart Type', ['Bar', 'Line', 'Scatter'])

if chart_type == 'Bar':
    fig = px.bar(filtered_data, x='Age', y='Cumulative Survival Probability', color='Sex', title='Cumulative Survival Probability by Age')
elif chart_type == 'Line':
    fig = px.line(filtered_data, x='Age', y='Cumulative Survival Probability', color='Sex', title='Cumulative Survival Probability by Age')
else:
    fig = px.scatter(filtered_data, x='Age', y='Cumulative Survival Probability', color='Quality of Life Index', 
                     title='Cumulative Survival Probability by Age and Quality of Life Index', 
                     color_continuous_scale=px.colors.sequential.Viridis)

# Display the chart
st.plotly_chart(fig)


