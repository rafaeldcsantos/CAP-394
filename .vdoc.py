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
import pandas as pd # to represent and process dataframes
import matplotlib.pyplot as plt # to create some plots and charts
import seaborn as sns # a different graphics library.
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
#| classes: custompython
supermDF.shape
#
#
#
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
# Plot the histogram of TotalDue with 20 bins.
plt.hist(onlyFirstItems['TotalDue'], bins=20);
# Set some plot parameters.
plt.xlabel('Total Due')
plt.ylabel('Frequency')
plt.title('Histogram of total amount due for each transaction')
plt.grid(True)
# Display it.
plt.show()
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
import matplotlib.ticker as ticker # Required to format the Y axis.
# Plot the histogram of TotalDue with 50 bins.
plt.hist(onlyFirstItems['TotalPaid'], bins=50);
# Set some plot parameters.
plt.xlabel('Total Paid')
plt.ylabel('Frequency')
plt.yscale('log') 
plt.title('Histogram of total amount paid in each transaction')
plt.grid(True)
# Correct the Y axis so values won't be displayed in scientific notation.
# This solution was suggested by ChatGPT!
ax = plt.gca()
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:g}'.format(x)))
# Display it.
plt.show()
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
# Plot the histogram of TotalDue with 50 bins.
plt.hist(onlyFirstItems['itemsInTransaction'], bins=50);
# Set some plot parameters.
plt.xlabel('Number of Items')
plt.ylabel('Frequency')
plt.yscale('log') 
plt.title('Histogram of number of items in basket')
plt.grid(True)
# Correct the Y axis so values won't be displayed in scientific notation.
# This solution was suggested by ChatGPT!
ax = plt.gca()
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:g}'.format(x)))
# Display it.
plt.show()
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
# Create the scatter plot with X=itemsInTransaction abnd Y=TotalPaid
plt.scatter(onlyFirstItems['itemsInTransaction'],onlyFirstItems['TotalPaid'])
# Set title and axes labels.
plt.title('Scatter Plot of Number of Items in Cart versus Total Paid')
plt.xlabel('Number of Items in Cart')
plt.ylabel('Total Paid')
# Show the plot.
plt.show()
#
#
#
#
#
#| classes: custompython
# Create the X and Y series (to make next commands shorter).
X = onlyFirstItems["itemsInTransaction"]
Y = onlyFirstItems["TotalPaid"]
# Plot a regression plot with transparency in the data points.
sns.regplot(x=X,y=Y,scatter_kws={"color":"skyblue","alpha":0.5},line_kws={"color":"red"})
# Set title and axes labels.
plt.title('Scatter Plot of Number of Items in Cart versus Total Paid')
plt.xlabel('Number of Items in Cart')
plt.ylabel('Total Paid')
# Show the plot.
plt.show()
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
#| # Set the size of figure in inches.
plt.figure(figsize=(12,7.5)) 
# Create the X, Y and points' color series (to make next commands shorter).
X = onlyFirstItems["itemsInTransaction"]
Y = onlyFirstItems["TotalPaid"]
PM = onlyFirstItems["PaymentMethod"]
# Plot a regression plot with transparency in the data points.
sns.scatterplot(x=X,y=Y,hue=PM)
# Set title and axes labels
plt.title('Scatter Plot of Number of Items in Cart versus Total Paid')
plt.xlabel('Number of Items in Cart')
plt.ylabel('Total Paid')
# Show the plot.
plt.show()
```
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
# We need a palette - a mapping from names to colors.
color_mapping = {
    'Dinheiro': 'yellowgreen',
    'Cartao'  : 'slateblue',
    'Cheque'  : 'magenta',
    'Outros'  : 'lightgrey'
}
# Set the size of figure in inches.
plt.figure(figsize=(11, 8)) 
# Create the X, Y and points' color series (to make next commands shorter).
X = onlyFirstItems["itemsInTransaction"]
Y = onlyFirstItems["TotalPaid"]
col = onlyFirstItems["SimplifiedPaymentMethod"]
# Plot a scatter plot with the data points and the new palette.
sns.scatterplot(x='itemsInTransaction', y='TotalPaid', \
    hue='SimplifiedPaymentMethod',\
    s=40,data=onlyFirstItems,palette=color_mapping)
# Set title and axes labels
plt.title('Scatter Plot of Number of Items in Cart versus Total Paid')
plt.xlabel('Number of Items in Cart')
plt.ylabel('Total Paid')
# Change the title of the legend and the marker scale.
ax = plt.gca()
ax.legend(title='Payment Method',markerscale=2)
# Show the plot.
plt.show()
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
hmap = histoFB.pivot(index="HourOfDay", columns="DayOfMonth", values="Quantity")
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
#
#
#| classes: custompython
# Set the size, title and labels of the plot.
plt.figure(figsize=(18, 9)) 
plt.title('Units of Bread Rolls sold by hour and day of month')
plt.xlabel('Day of Month')
plt.ylabel('Hour of Day')
# Create and show the heatmap. Note the parameters used to make it look good.
sns.heatmap(hmap,cmap='gist_ncar',linewidths=0.30,annot=True,fmt='g',vmin=0,vmax=1650)
plt.show()
```
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
