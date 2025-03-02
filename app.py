import plotly.express as px
import streamlit as st
import pandas as pd
vehicles = pd.read_csv('/datasets/vehicles_us.csv')
st.title("Vehicle Analysis Dashboard")

# Overview
st.header("Overview of Vehicle Price and Odometer Data")
st.write("""
This dashboard provides an analysis of vehicle sales using the given dataset.
Explore how vehicle condition and odometer readings affect the average sale price.
Use the controls below to customize your view.
""")

# Checkbox to toggle the display of "Average Price by Condition"
show_condition_chart = st.checkbox("Show Average Price by Vehicle Condition", value=True)

if show_condition_chart:
    # Group by 'condition' and calculate the average price
    average_price_by_condition = vehicles.groupby('condition')['price'].mean().reset_index()
    average_price_by_condition.columns = ['Condition', 'Average Price']

    # Create a bar chart
    fig_condition = px.bar(
        average_price_by_condition,
        x='Condition',
        y='Average Price',
        title='Average Price by Vehicle Condition',
        text='Average Price',
        labels={'Condition': 'Vehicle Condition', 'Average Price': 'Average Price ($)'},
        color='Condition'
    )

    # Display the chart
    st.plotly_chart(fig_condition)

# Group by odometer ranges in 10,000 mile increments
vehicles['odometer_bin'] = pd.cut(vehicles['odometer'], bins=range(0, int(vehicles['odometer'].max()) + 10000, 10000))
average_price_by_odometer = vehicles.groupby('odometer_bin')['price'].mean().reset_index()
average_price_by_odometer['odometer_bin'] = average_price_by_odometer['odometer_bin'].astype(str)

# Bar chart for average price by odometer
fig_odometer = px.bar(
    average_price_by_odometer,
    x='odometer_bin',
    y='price',
    title='Average Sale Price by Odometer Range',
    labels={'odometer_bin': 'Odometer Range (miles)', 'price': 'Average Price ($)'},
    text='price'
)

# Display the chart
st.plotly_chart(fig_odometer)



# Scatter plot for Price vs. Model Year with Color by Condition
fig = px.scatter(
    vehicles,
    x='model_year',
    y='price',
    color='condition',  # Color by condition
     color_discrete_sequence=px.colors.qualitative.Set1,  # Explicit color palette
    title='Price vs. Model Year',
    labels={'model_year': 'Model Year', 'price': 'Price'}
)

# Show the plot
fig.show()

# Histogram for Price Distribution
fig = px.histogram(
vehicles,
x='price',
nbins=100,
title='Price Distribution',
labels={'price': 'Vehicle Price'},
color_discrete_sequence=['blue']
)


fig.show()

# Scatter plot for Price vs. Odometer
fig = px.scatter(
    vehicles,
    x='odometer',
    y='price',
    color='fuel',
     color_discrete_sequence=px.colors.qualitative.Set1,  # Explicit color palette
    title='Price vs. Odometer',
    labels={'odometer': 'Odometer (miles)', 'price': 'Price'}
)
fig.show()

# Histogram for Condition Distribution
fig = px.histogram(
    vehicles,
    x='condition',
    title='Condition Distribution',
    labels={'condition': 'Car Condition'},
    color_discrete_sequence=['green']
)
fig.show()

# Group by 'condition' and calculate the average price
average_price_by_condition = vehicles.groupby('condition')['price'].mean().reset_index()

# Rename columns for better readability
average_price_by_condition.columns = ['Condition', 'Average Price']

# Create a bar chart to show the average price
fig = px.bar(
    average_price_by_condition,
    x='Condition',
    y='Average Price',
    title='Average Price by Vehicle Condition',
    text='Average Price',  # Display the average price as text on the bars
    labels={'Condition': 'Vehicle Condition', 'Average Price': 'Average Price ($)'},
    color='Condition',
    color_discrete_sequence=px.colors.qualitative.Set1,  # Explicit color palette
)

# Format the text on bars and show the chart
fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
fig.update_layout(yaxis_title='Average Sale Price ($)')
fig.show()

# Histogram for Days Listed Distribution
fig = px.histogram(
    vehicles,
    x='days_listed',
    nbins=30,
    title='Days Listed Distribution',
    labels={'days_listed': 'Days Listed'},
    color_discrete_sequence=['orange']
)
fig.show()

# Box plot for Price by Car Type
fig = px.box(
    vehicles,
    x='type',
    y='price',
    title='Price by Vehicle Type',
    labels={'type': 'Vehicle Type', 'price': 'Price'},
    color='type', color_discrete_sequence=px.colors.qualitative.Set1,  # Explicit color palette

    
)
fig.show()


