import plotly.express as px
import streamlit as st
import pandas as pd

# Load the dataset
vehicles = pd.read_csv('vehicles_us.csv')
# Filter out outliers and erronious data
vehicles['is_4wd'] = vehicles['is_4wd'].fillna(0.0)
vehicles['paint_color'] = vehicles['paint_color'].fillna('Unknown')
vehicles['odometer'] = vehicles['odometer'].fillna(0.0)
vehicles['model_year'] = vehicles['model_year'].fillna(1955) #this value was placed to preserve data
vehicles = vehicles[vehicles['price'] <= 100000]
vehicles = vehicles[vehicles['price'] >= 100]
vehicles = vehicles[vehicles['odometer'] <= 500000]
vehicles = vehicles[vehicles['model_year'] >= 1955]
vehicles['is_4wd'] = vehicles['is_4wd'].fillna(0).astype(int)
vehicles['paint_color'] = vehicles['paint_color'].fillna('Unknown')

)
#grouping vehicle data
vehicles['model_year'] = vehicles['model_year'].fillna( 
    vehicles.groupby('model')['model_year'].transform('median')
)
vehicles['odometer'] = vehicles['odometer'].fillna(
    vehicles.groupby('model')['odometer'].transform('median')
)
vehicles['cylinders'] = vehicles['cylinders'].fillna(
    vehicles.groupby('model')['cylinders'].transform(lambda x: x.mode()[0] if not x.mode().empty else None)
)

# Title
st.title("Vehicle Analysis Dashboard")

# Introduction
st.header("Overview of Vehicle Sales Data")
st.write("""
This dashboard provides an analysis of vehicle sales using the given dataset.
Explore how vehicle condition, odometer readings and fuel types affect the average sale price.
Use the checkboxes below to customize your view.
""")

# Checkbox for Average Price by Vehicle Condition Chart
if st.checkbox("Show Average Price by Vehicle Condition", value=True):
    # Calculate average price by condition and round it to 2 decimal places
    average_price_by_condition = vehicles.groupby('condition')['price'].mean().reset_index()
    average_price_by_condition.columns = ['Condition', 'Average Price']
    average_price_by_condition['Average Price'] = average_price_by_condition['Average Price'].round(
        2)  # Round to 2 decimals

    # Create the bar chart
    fig_condition = px.bar(
        average_price_by_condition,
        x='Condition',
        y='Average Price',
        title='Average Price by Vehicle Condition',
        text='Average Price',  # Display values on the chart
        labels={'Condition': 'Vehicle Condition', 'Average Price': 'Average Price ($)'},
        color='Condition'
    )

    # Update the text template to show bold values and rounded numbers
    fig_condition.update_traces(
        texttemplate='<b>$%{text:.2f}</b>',  # Make values bold and formatted to 2 decimals
        textposition='outside'  # Position text outside the bars
    )

    # Update layout for better readability
    fig_condition.update_layout(yaxis_title='Average Sale Price ($)')

    # Display the chart in Streamlit
    st.plotly_chart(fig_condition)


# Checkbox for Average Sale Price by Odometer Range
if st.checkbox("Show Average Sale Price by Odometer Range", value=True):
    # Create bins for odometer in 10,000-mile increments
    vehicles['odometer_bin'] = pd.cut(vehicles['odometer'],
                                      bins=range(0, int(vehicles['odometer'].max()) + 10000, 10000))

    # Group by odometer bin and calculate average price
    average_price_by_odometer = vehicles.groupby('odometer_bin')['price'].mean().reset_index()

    # Format the odometer bin labels with "K" and remove the last three zeros
    average_price_by_odometer['odometer_bin'] = average_price_by_odometer['odometer_bin'].apply(
        lambda x: f"{int(x.left // 1000)}K-{int(x.right // 1000)}K"
    )

    # Create the bar chart
    fig_odometer = px.bar(
        average_price_by_odometer,
        x='odometer_bin',
        y='price',
        title='Average Sale Price by Odometer Range',
        labels={
            'odometer_bin': 'Odometer Range (thousands of miles)',
            'price': 'Average Price ($)'
        },
        text='price'  # Show average prices on the chart
    )

    # Update traces to format the text on the bars (e.g., add $, 2 decimal points, bolded)
    fig_odometer.update_traces(
        texttemplate='<b>$%{text:.2f}</b>',  # Bold and format price values
        textposition='outside'  # Place text outside bars for clarity
    )

    # Update layout for better visualization
    fig_odometer.update_layout(
        xaxis_title='Odometer Range (K miles)',
        yaxis_title='Average Sale Price ($)'
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig_odometer)

# Checkbox for Price vs. Model Year Scatter Plot
if st.checkbox("Show Price vs. Model Year Scatter Plot", value=True):
    

    # Scatter plot for Price vs. Model Year
    fig = px.scatter(
        vehicles,
        x='model_year',
        y='price',
        color='condition',
        color_discrete_sequence=px.colors.qualitative.Set1,
        title='Price vs. Model Year',
        labels={'model_year': 'Model Year', 'price': 'Price'},
        hover_data=['model', 'model_year', 'condition', 'price', 'odometer', 'cylinders']  # Adding hover data
    )

    # Display in Streamlit
    st.plotly_chart(fig)



# Checkbox for Price Distribution Histogram
if st.checkbox("Show Price Distribution Histogram", value=True):
    fig = px.histogram(
        vehicles,
        x='price',
        nbins=100,
        title='Price Distribution',
        labels={'price': 'Vehicle Price'},
        color_discrete_sequence=['blue']
    )
    st.plotly_chart(fig)

# Checkbox for Price vs. Odometer Scatter Plot
if st.checkbox("Show Price vs. Odometer Scatter Plot", value=True):
    fig = px.scatter(
        vehicles,
        x='odometer',
        y='price',
        color='fuel',
        color_discrete_sequence=px.colors.qualitative.Set1,
        title='Price vs. Odometer',
        labels={'odometer': 'Odometer (miles)', 'price': 'Price'},
        hover_data=['model', 'model_year']  # Adding 'model' to hover data

    )
    st.plotly_chart(fig)

# Checkbox for Condition Distribution Histogram
if st.checkbox("Show Condition Distribution Histogram", value=True):
    fig = px.histogram(
        vehicles,
        x='condition',
        title='Condition Distribution',
        labels={'condition': 'Car Condition'},
        color_discrete_sequence=['green']
    )
    st.plotly_chart(fig)

# Checkbox for Days Listed Distribution Histogram
if st.checkbox("Show Days Listed Distribution Histogram", value=True):
    fig = px.histogram(
        vehicles,
        x='days_listed',
        nbins=30,
        title='Days Listed Distribution',
        labels={'days_listed': 'Days Listed'},
        color_discrete_sequence=['orange']
    )
    st.plotly_chart(fig)

# Checkbox for Price by Vehicle Type Box Plot
if st.checkbox("Show Price by Vehicle Type Box Plot", value=True):
  
    fig = px.box(
        vehicles,
        x='type',
        y='price',
        title='Price by Vehicle Type',
        labels={'type': 'Vehicle Type', 'price': 'Price'},
        color='type',
        color_discrete_sequence=px.colors.qualitative.Set1,
        hover_data=['model', 'model_year'], 
    )
    st.plotly_chart(fig)

