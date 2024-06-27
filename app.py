import streamlit as st
import pandas as pd
import plotly.express as px

# Read CSV data
df = pd.read_csv('mortality_rates.csv')

# Calculate cumulative survival probability
df['Survival Probability'] = 1 - df['Mortality Rate']
df['Cumulative Survival Probability'] = df.groupby(['Sex', 'Quality of Life Index'])['Survival Probability'].cumprod()

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

# Create cumulative survival probability plot
fig_cumulative = px.line(filtered_data, x='Age', y='Cumulative Survival Probability', color='Quality of Life Index', 
                         title='Cumulative Survival Probability by Age and Quality of Life Index')

# Display the cumulative survival probability plot
st.plotly_chart(fig_cumulative)

# Create scatter plot
fig_scatter = px.scatter(filtered_data, x='Age', y='Mortality Rate', color='Quality of Life Index', 
                         title='Mortality Rate by Age and Quality of Life Index', 
                         color_continuous_scale=px.colors.sequential.Viridis)

# Display the scatter plot
st.plotly_chart(fig_scatter)
