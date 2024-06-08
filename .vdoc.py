# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| classes: custompython
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
#
#
#
#
#
#
#| classes: custompython
# Read the data from a file into a dataframe, with proper character encoding
supermDF = pd.read_csv("Resources/Data/SupermarketCSV/transactions.csv",
                        encoding="iso-8859-1")
#
#
#
#
#
#
#
#
#
#| classes: custompython
supermDF.shape
#
#
#
#
#
#| classes: custompython
print(supermDF.dtypes)
#
#
#
#
#
#
#| classes: custompython
print(supermDF.info())
#
#
#
#| classes: custompython
# Convert the field Date to a string, which is used by pd.to_datetime with a specific
# format to be converted into an array of datetime object, which is stored in our
# dataframe using a new column name.
supermDF['DateTime'] = pd.to_datetime(supermDF['Date'].astype(str),format='%Y%m%d%H%M%S')
#
#
#
#
#
#
#
#
#
#
#
#| classes: custompython
# Get the column Description, create a series with the unique values on it, 
# return the length of this series. 
len(pd.unique(supermDF['Description']))
#
#
#
#
#
#
#
#| classes: custompython
# Show a summary of the counts for all values of the column Description.
supermDF['Description'].value_counts()
#
#
#
#
#
#| classes: custompython
# Show the top ten items of the counts for all values of the column Description.
supermDF['Description'].value_counts().head(10)
#
#
#
#
#
#| classes: custompython
# Store the counts in a series.
counts = supermDF['Description'].value_counts()
# Filter those between two values.
counts[counts.between(1000,1200)]
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| classes: custompython
# Create a new dataframe with only the first item in each transaction. 
onlyFirstItems = supermDF.loc[supermDF['itemOrder'] == 1].copy()
#
#
#
#
#
#| classes: custompython
# Prints the mean of all transactions' TotalDue.
onlyFirstItems['TotalDue'].mean()
#
#
#
#
#
#| classes: custompython
# Get the mean of all transactions' TotalDue.
ts1 = onlyFirstItems.loc[onlyFirstItems['StoreID'] == 1,'TotalDue'].mean()
ts2 = onlyFirstItems.loc[onlyFirstItems['StoreID'] == 2,'TotalDue'].mean()
ts3 = onlyFirstItems.loc[onlyFirstItems['StoreID'] == 3,'TotalDue'].mean()
ts4 = onlyFirstItems.loc[onlyFirstItems['StoreID'] == 4,'TotalDue'].mean()
# Format and print these values.
print(f"Mean Total Due by Store: 1:{ts1:.2f}, 2:{ts2:.2f}, 3:{ts3:.2f}, 4:{ts4:.2f}.")
#
#
#
#
#
#| classes: custompython
# Print a series with all unique values for StoreID.
pd.unique(supermDF['StoreID'])
#
#
#
#
#
#
#
#
#
#
#
#
#| classes: custompython
# Create the plot.
fig = px.histogram(onlyFirstItems, x='TotalDue', nbins=20, 
          title='Histogram of total amount due for each transaction')
# Update layout for labels and grid.
fig.update_layout(
    xaxis_title='Total Due',
    yaxis_title='Frequency',
    showlegend=False
)
fig.update_xaxes(showgrid=True)
fig.update_yaxes(showgrid=True)
# Display it.
fig.show()
#
#
#
#
#
#
#
#| classes: custompython
# Create a list of columns we want to show.
fields = ['TransactionID','TotalDue','TotalPaid','Change','Status']
# Print the top 10 largest TotalDue values with the fields we chose.
onlyFirstItems.nlargest(10,'TotalDue')[fields]
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| classes: custompython
epsilon = 0.0001
onlyFirstItems['LogTotalPaid'] = np.log10(onlyFirstItems['TotalPaid']+epsilon)
#
#
#
#
#
#| classes: custompython
# We will use custom tick values and labels.
tickvals = np.log10([0.05,0.10,0.25,0.5,1,2,5,10,20,50,100,200,500,1000])
ticktext = ['0.05','0.10','0.25','0.5','1','2','5','10','20','50','100','200','500','1000']
# Create the histogram.
fig = go.Figure()
fig.add_trace(go.Histogram(
    x=onlyFirstItems['LogTotalPaid'],
    nbinsx=50,
    hoverinfo='skip' # Very hard to make a working hover info!
))
# Update layout.
fig.update_layout(
    title='Histogram of total amount paid in each transaction',
    xaxis_title='Total Paid',
    yaxis_title='Frequency',
     xaxis=dict(
        tickmode='array',
        tickvals=tickvals,
        ticktext=ticktext,
        type='linear'  
    ),
    yaxis=dict(
        type='linear',
        tickformat=',d'
    ),
    showlegend=False
)
# Add grids.
fig.update_xaxes(showgrid=True)
fig.update_yaxes(showgrid=True)
# Display it.
fig.show()
#
#
#
#
#
#
#
#
#
#
#
#
#| classes: custompython
# Select only some fields for displaying.
fields = ['TransactionID','Description','UnitPrice','Quantity','Amount']
# Filter the dataframe locating only rows where TotalPaid is >= 800, then sort the
# filtered dataframe by Amount (from larger to smaller) then show the fields we chose.
supermDF.loc[supermDF['TotalPaid'] >= 800].sort_values('Amount',ascending=False)[fields]
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| classes: custompython
# Group records by TransactionID, select TransactionID to extract a metric (size).
itemsIT = supermDF.groupby('TransactionID')['TransactionID'].transform('size')
# Add it as a new column.
supermDF['itemsInTransaction'] = itemsIT
# We want only one record per transaction!
onlyFirstItems = supermDF.loc[supermDF['itemOrder'] == 1].copy()
#
#
#
#
#
#| classes: custompython
# Create histogram.
fig = go.Figure()
fig.add_trace(go.Histogram(
    x=onlyFirstItems['itemsInTransaction'],
    nbinsx=50
))
# Update layout.
fig.update_layout(
    title='Histogram of number of items in basket',
    xaxis_title='Number of Items',
    yaxis_title='Frequency',
    yaxis=dict(
        type='log',
        tickformat='g'
    ),
    showlegend=False
)
fig.update_xaxes(showgrid=True)
fig.update_yaxes(showgrid=True)
# Display it.
fig.show()

#
#
#
#
#
#
#
#
#
#
#
#
#| classes: custompython
# Create scatter plot using Plotly
fig = px.scatter(
    onlyFirstItems,
    x='itemsInTransaction',
    y='TotalPaid',
    title='Scatter Plot of Number of Items in Cart versus Total Paid',
    labels={
        'itemsInTransaction': 'Number of Items in Cart',
        'TotalPaid': 'Total Paid'
    }
)
# Show the plot
fig.show()
#
#
#
#
#
#| classes: custompython
# Fit linear regression model.
X = np.array(onlyFirstItems['itemsInTransaction']).reshape(-1, 1)
y = np.array(onlyFirstItems['TotalPaid'])
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
# Create the figure.
fig = go.Figure()
# Add scatter plot using Plotly Graph Objects.
fig.add_trace(go.Scatter(
    x=onlyFirstItems['itemsInTransaction'],
    y=onlyFirstItems['TotalPaid'],
    mode='markers',
    name='Data Points',
    showlegend=False,
    marker=dict(opacity=0.6)  # Adjust marker opacity
))
# Add linear regression line using Plotly Graph Objects.
fig.add_trace(go.Scatter(
    x=onlyFirstItems['itemsInTransaction'],
    y=y_pred,
    mode='lines',
    name='Linear Regression',
    line=dict(color='red'),
    showlegend=False,
))
# Update the figure.
fig.update_layout(
    title='Number of Items in Basket x Total Paid',
    xaxis_title='Number of Items',
    yaxis_title='Total Paid',
    showlegend=False
)
# Show the plot.
fig.show()
#
#
#
#
#
#
#
#
#
#
#
#
#
#| classes: custompython
# Create the scatter plot with Plotly Express.
fig = px.scatter(
    onlyFirstItems,
    x="itemsInTransaction",
    y="TotalPaid",
    color="PaymentMethod",
    title='Scatter Plot of Number of Items in Cart versus Total Paid',
    labels={
        'itemsInTransaction': 'Number of Items in Cart',
        'TotalPaid': 'Total Paid'
    }
)
# Show the plot.
fig.show()
#
#
#
#
#
#
#
#
#
#
#
#| classes: custompython
# A simple function that simply the categories of payment method.
def simplifyPayment(paymethod):
    if paymethod.startswith("Dinheiro"):
        return "Dinheiro"
    elif paymethod.startswith("Cartao"):
        return "Cartao"
    elif paymethod.startswith("Cheque"):
        return "Cheque"
    else:
        return "Outros"
# Now we can add a new column based on the value of PaymentMethod.
onlyFirstItems['SimplifiedPaymentMethod'] = \
    onlyFirstItems['PaymentMethod'].apply(simplifyPayment)      
#
#
#
#
#
#| classes: custompython
# Define a custom color palette.
custom_color_palette = {
    'Dinheiro': 'yellowgreen',
    'Cartao'  : 'slateblue',
    'Cheque'  : 'magenta',
    'Outros'  : 'lightgrey'  
}
# Create the scatter plot with Plotly Express.
fig = px.scatter(
    onlyFirstItems,
    x="itemsInTransaction",
    y="TotalPaid",
    color="SimplifiedPaymentMethod",
    title='Scatter Plot of Number of Items in Cart versus Total Paid',
    labels={
        'itemsInTransaction': 'Number of Items in Cart',
        'TotalPaid': 'Total Paid'
    },
    color_discrete_map=custom_color_palette
)
# Show the plot.
fig.show()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| classes: custompython
# Get only items that are equal to "PAO FRANCES           "
onlyBreadRolls = supermDF.loc[supermDF['Description'] == "PAO FRANCES           "]
# Select only some of the columns.
onlyBreadRolls = onlyBreadRolls[['StoreID','DateTime','Quantity']]
# Extract the day of month from the DateTime column, store in new column.
onlyBreadRolls['DayOfMonth'] = onlyBreadRolls['DateTime'].dt.day
# Extract the hour of day from the DateTime column, store in new column.
onlyBreadRolls['HourOfDay'] = onlyBreadRolls['DateTime'].dt.hour
#
#
#
#
#
#| classes: custompython
# Sum the amounts for each combination of DayOfMonth and HourOfDay.
histoFB = onlyBreadRolls.groupby(["DayOfMonth","HourOfDay"]).Quantity.sum().reset_index() 
#
#
#
#
#
#
#
#
#
#
#
#
#| classes: custompython
# Reorders the two-dimensional histogram as a matrix-like dataframe.
hmap = histoFB.pivot(index="HourOfDay", columns="DayOfMonth", values="Quantity").fillna(0)
# Use those indexes for the row and column indexes.
days = list(range(1, 32))
hours = list(range(24))
# Apply those indexes to the datafrme, filling nonexistent (na) values with zeros.
hmap = hmap.reindex(index=hours).reindex(columns=days).fillna(0)
#
#
#
#
#
#| classes: custompython
# Create the heatmap.
fig = go.Figure(data=go.Heatmap(
    z=hmap.values,
    x=hmap.columns,
    y=hmap.index,
    colorscale='Jet',
    text=hmap.values,
    texttemplate="%{text:.0f}",  # Format text to display as integers
    textfont={"size":10},
    hoverinfo='z',  # Display value on hover
    showscale=True
))
# Update layout to add thin lines around each cell.
# This was suggested by Code Copilot!
fig.update_traces(
    zmin=0, zmax=hmap.values.max(),  
    xgap=1,  
    ygap=1,  
    colorbar=dict(tickfont=dict(size=10))  
)
# Customize the layout.
fig.update_layout(
    title='Heatmap of Bread Rolls Sold',
    xaxis_title='Day of Month',
    yaxis_title='Hour of Day',
    xaxis=dict(
        tickmode='linear',
        dtick=1,  
        tickfont=dict(size=10),
        showgrid=False,
        zeroline=False # Remove grid lines
    ),
    yaxis=dict(
        tickmode='linear',
        dtick=1, 
        tickfont=dict(size=10),
        showgrid=False,
        zeroline=False # Remove grid lines
    ),
    plot_bgcolor='#808080', 
)
# Invert the Y-axis.
fig.update_yaxes(autorange='reversed')
# Show the plot.
fig.show()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
