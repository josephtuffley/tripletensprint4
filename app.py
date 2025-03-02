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
