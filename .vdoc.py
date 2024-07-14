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
#| classes: custompython
import pandas as pd
import plotly.express as px
import json
#
#
#
#
#
#| classes: custompython
file = 'Resources/Data/Emendas/Emendas.csv'
# Read the CSV file using the specified separator and encoding.
df = pd.read_csv(file, sep=';', encoding='ISO-8859-1')
#
#
#
#
#
#| classes: custompython
df['Valor'] = df['Valor Empenhado'].str.replace('.', '', regex=False).\
                                    str.replace(',', '.').astype(float)
#
#
#
#
#
#| classes: custompython
# We don't really need some of the fields (redundant ones):
df = df.drop(['Nome do Autor da Emenda', 'Número da emenda',
              'Código Função','Código Subfunção'], axis=1)
#
#
#
#
#
#| classes: custompython
# We don't really need some of the payment fields (only 'Valor'):
df = df.drop(['Valor Empenhado', 'Valor Liquidado', 'Valor Pago', 
              'Valor Restos A Pagar Inscritos','Valor Restos A Pagar Cancelados',
              'Valor Restos A Pagar Pagos'], axis=1)                                    
#
#
#
#
#
#| classes: custompython
# Display part of the data.
df
#
#
#
#
#
#| classes: custompython
dfCountry = df[df["Localidade do gasto"] == "Nacional"]
dfAbroad = df[df["Localidade do gasto"] == "Exterior"]
dfMultiple = df[df["Localidade do gasto"] == "MÚLTIPLO"]
regions = ["Norte","Centro-Oeste","Nordeste","Sudeste","Sul"]
dfRegions = df[df["Localidade do gasto"].isin(regions)]
dfStates = df[df["Localidade do gasto"].str.contains(r"\(\w{2}\)", regex=True)]
dfCounties = df[df["Localidade do gasto"].str.contains(" - ")]
#
#
#
#
#
#| classes: custompython
dfCount = len(df)
dfCountryCount = len(dfCountry)
dfAbroadCount = len(dfAbroad)
dfMultipleCount = len(dfMultiple)
dfRegionsCount = len(dfRegions)
dfStatesCount = len(dfStates)
dfCountiesCount = len(dfCounties)
total = dfCountryCount+dfAbroadCount+dfMultipleCount+\
        dfRegionsCount+dfStatesCount+dfCountiesCount
print("Number of records in the original DataFrame:", dfCount)
print("Number of records in the 'Nacional' subset:", dfCountryCount)
print("Number of records in the 'Exterior' subset:", dfAbroadCount)
print("Number of records in the 'Multiple' subset:", dfMultipleCount)
print("Number of records in the 'Regions' subset:", dfRegionsCount)
print("Number of records in the 'State (UF)' subset:", dfStatesCount)
print("Number of records in the 'County - State' subset:", dfCountiesCount)
print("Total number of records in the subsets:",total)
#
#
#
#
#
#
#
#
#
#
#
#
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
cfunctions = df.groupby(["Nome Função","Nome Subfunção"]).size().reset_index(name='Count')
cfunctions
#
#
#
#
#
#| classes: custompython
functionsU = cfunctions["Nome Função"].unique()
colors = px.colors.qualitative.Plotly
# Create a dictionary to map each "Nome Função" to a specific color
colormap = {function: colors[i % len(colors)] for i, function in enumerate(functionsU)}
#
#
#
#
#
#| classes: custompython
# Create a Sunburst chart
sunburstC = px.sunburst(cfunctions, 
                        path=['Nome Função', 'Nome Subfunção'], 
                        values='Count', 
                        title='Number of Amendments by Function and Subfunction',
                        labels={'Nome Função': 'Function', 'Nome Subfunção': \
                            'Subfunction', 'Count': 'Number of Amendments'},
                        color='Nome Função',
                        color_discrete_map=colormap)
# Display the chart
sunburstC.show()
#
#
#
#
#
#| classes: custompython
vfunctions = df.groupby(["Nome Função", "Nome Subfunção"])["Valor"].sum().reset_index(name='Amount')
vfunctions
#
#
#
#
#
#| classes: custompython
# Create a Sunburst chart
sunburstV = px.sunburst(vfunctions, 
                        path=['Nome Função', 'Nome Subfunção'], 
                        values='Amount', 
                        title='Total Amount of Amendments by Function and Subfunction',
                        labels={'Nome Função': 'Function', 'Nome Subfunção': \
                            'Subfunction', 'Count': 'Number of Amendments'},
                        color='Nome Função',
                        color_discrete_map=colormap)
# Display the chart
sunburstV.show()
#
#
#
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
functionCounts = dfCountry["Nome Função"].value_counts()
functionCounts
#
#
#
#
#
#
#| classes: custompython
cpy = dfCountry.groupby(["Nome Função","Ano da Emenda"]).size().\
        reset_index(name='Count')
cpy
#
#
#
#
#
#| classes: custompython
# Create a faceted line plot
fig = px.line(cpy, 
              x='Ano da Emenda', 
              y='Count', 
              color='Nome Função',
              facet_col='Nome Função', 
              facet_col_wrap=3,
              title='Amendments per Year per Function',
              labels={'Ano da Emenda': 'Year', 'Count': 'Amendments', 
                      'Nome Função': ''},
              markers=True)
# Update layout for better spacing and readability
fig.update_layout(
    height=1020,
    showlegend=False,
    margin=dict(t=80) 
)
# Remove the automatic subplot titles
for annotation in fig['layout']['annotations']:
    annotation['text'] = annotation['text'].split("=")[-1]
# Update x-axes to show ticks and labels for all subplots
years = cpy["Ano da Emenda"].unique()
years.sort()
fig.update_xaxes(showticklabels=True,tickvals=years,tickangle=90,
                 tickfont=dict(size=10))  
fig.update_yaxes(title_font=dict(size=10))
# Display the plot
fig.show()
#
#
#
#
#
#
#
#| classes: custompython
# Group by "Nome Função" and "Ano da Emenda" and sum the values
spy = dfCountry.groupby(["Nome Função", "Ano da Emenda"])["Valor"].sum().\
        reset_index(name='Total Value')
spy
#
#
#
#
#
#| classes: custompython
# Create a faceted line plot
fig = px.line(spy, 
              x='Ano da Emenda', 
              y='Total Value', 
              color='Nome Função',
              facet_col='Nome Função', 
              facet_col_wrap=3,
              title='Amendments Total Value per Year per Function',
              labels={'Ano da Emenda': 'Year', 'Count': 'Amendmts', 'Nome Função': ''},
              markers=True)
# Update layout for better spacing and readability
fig.update_layout(
    height=990,
    showlegend=False,
    margin=dict(t=80)     
)
# Remove the automatic subplot titles
for annotation in fig['layout']['annotations']:
    annotation['text'] = annotation['text'].split("=")[-1]
# Update x-axes to show ticks and labels for all subplots
years = spy["Ano da Emenda"].unique()
years.sort()
fig.update_xaxes(showticklabels=True,tickvals=years,tickangle=90,tickfont=dict(size=10))  
fig.update_yaxes(title_font=dict(size=10))
# Display the plot
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
#| classes: custompython
dfStatesPrep = dfStates.groupby(["Localidade do gasto"]).size().reset_index(name='Count')
dfStatesPrep['Localidade do gasto'] = \
  dfStatesPrep['Localidade do gasto'].str.replace(r'\ \(UF\)', '', regex=True)
dfStatesPrep
#
#
#
#
#
#| classes: custompython
with open("Resources/Data/Emendas/br_states.json") as f:
    geojson_data = json.load(f)
for feature in geojson_data['features']:
    feature['properties']['Estado'] = feature['properties']['Estado'].upper()
#
#
#
#
#
#| classes: custompython
fig = px.choropleth(
    dfStatesPrep, # The dataframe
    geojson=geojson_data, # The GeoJSON data
    # These two parameters identify the field on the dataframe and 
    # property on the GeoJSON data that must match.
    locations='Localidade do gasto', 
    featureidkey="properties.Estado", 
    color='Count', 
    hover_name='Localidade do gasto',
    hover_data=['Count'],
    title='Number of Amendments per State',
    color_continuous_scale="Viridis"
)
# Update layout for better spacing and readability
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":35,"l":0,"b":0})
# Display the map
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
#| classes: custompython
countAdE = df["Código do Autor da Emenda"].value_counts()
# Print the result
print(countAdE)
#
#
#
#
#
#| classes: custompython
dfSI = df[df["Código do Autor da Emenda"] == "S/I"]
dfWI = df[df["Código do Autor da Emenda"] != "S/I"]
recordSI = len(dfSI)
print(f"Total records in dfSI DataFrame: {recordSI}")
#
#
#
#
#
#
#
#| classes: custompython
SIdist = dfSI.groupby(["Nome Função","Nome Subfunção"])["Valor"].sum().reset_index(name='Amount')
WIdist = dfWI.groupby(["Nome Função","Nome Subfunção"])["Valor"].sum().reset_index(name='Amount')
#
#
#
#
#
#| classes: custompython
sunburstSI = px.sunburst(SIdist, 
                         path=['Nome Função', 'Nome Subfunção'], 
                         values='Amount', 
                         title='Amount of SI Amendments by Function and Subfunction',
                         labels={'Nome Função': 'Function', 'Nome Subfunção': \
                             'Subfunction', 'Count': 'Number of Amendments'},
                         color='Nome Função',
                         color_discrete_map=colormap)
# Display the chart
sunburstV.show()
#
#
#
#| classes: custompython
# Create a Sunburst chart
sunburstV = px.sunburst(WIdist, 
                        path=['Nome Função', 'Nome Subfunção'], 
                        values='Amount', 
                        title='Amount of WI Amendments by Function and Subfunction',
                        labels={'Nome Função': 'Function', 'Nome Subfunção': \
                            'Subfunction', 'Count': 'Number of Amendments'},
                        color='Nome Função',
                        color_discrete_map=colormap)
# Display the chart
sunburstV.show()
#
#
#
#
#
#
#
#
#
#
#
#
#
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
# For the ones without identification
grDfSI = dfSI.groupby("Ano da Emenda").size().reset_index(name='Count')
grDfSI['Type'] = 'Without Id.'
# For the ones with identification
grDfWI = dfWI.groupby("Ano da Emenda").size().reset_index(name='Count')
grDfWI['Type'] = 'With Id.'
# Combine them
bothDfs = pd.concat([grDfSI,grDfWI])
#
#
#
#
#
#| classes: custompython
fig = px.line(bothDfs, x="Ano da Emenda", y="Count", color='Type',
              title="Total Amount of Amendments per Year",
              labels={"Ano da Emenda": "Year", "Count": "Number of Amendments", "Type": "Type"})
fig.show()
#
#
#
#
#
#
#
#| classes: custompython
top12 = dfWI["Código do Autor da Emenda"].value_counts().nlargest(12).index
dftop12 = dfWI[dfWI["Código do Autor da Emenda"].isin(top12)]
dfG = dftop12.groupby(["Código do Autor da Emenda", "Ano da Emenda"]).size().\
               reset_index(name='Count')
#
#
#
#
#
#| classes: custompython
fig = px.line(dfG, x="Ano da Emenda", y="Count", color="Código do Autor da Emenda",
              markers=True,
              title="Number of Amendments per Year by Top 12 Authors",
              labels={"Ano da Emenda": "Year", "Count": "Number of Amendments",
                      "Código do Autor da Emenda": "Author"})
fig.update_yaxes(type='log')
# Display the plot
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
dfDefense = dfCountry[dfCountry["Nome Função"] == "Defesa nacional"]
dfDefenseY = dfDefense.groupby("Ano da Emenda")["Valor"].sum().reset_index()
dfDefenseY['Type'] = 'Defesa Nacional'
dfEducation = dfCountry[dfCountry["Nome Função"] == "Educação"]
dfEducationY = dfEducation.groupby("Ano da Emenda")["Valor"].sum().reset_index()
dfEducationY['Type'] = 'Educação'
dfHealth = dfCountry[dfCountry["Nome Função"] == "Saúde"]
dfHealthY = dfHealth.groupby("Ano da Emenda")["Valor"].sum().reset_index()
dfHealthY['Type'] = 'Saúde'
# Combine them
bothDfs = pd.concat([dfDefenseY,dfHealthY])
print(bothDfs)
#
#
#
#
#| classes: custompython
fig = px.line(bothDfs, x="Ano da Emenda", y="Valor", color='Type',
              title="Total Amount of Amendments per Year",
              labels={"Ano da Emenda": "Year", "Count": "Number of Amendments", "Type": "Type"})
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
#| classes: custompython

#
#
#
#| classes: custompython

#
#
#
#| classes: custompython

#
#
#
#| classes: custompython

#
#
#
#| classes: custompython

```
#
#| classes: custompython

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
dfDefesaNacional = dfCountry[dfCountry["Nome Função"] == "Defesa nacional"]
dfValueByYear = dfDefesaNacional.groupby("Ano da Emenda")["Valor"].sum().reset_index()
# Create a histogram
fig = px.bar(dfValueByYear, x='Ano da Emenda', y='Valor', 
             title='Total Values per Year in National Defense',
             labels={'Ano da Emenda': 'Year', 'Valor': 'Total Value'})
# Show the plot
fig.show()
#
#
#
#
#
#
#| classes: custompython
subfuncCounts = dfDefesaNacional["Nome Subfunção"].value_counts()
print("\nOccurrences of each unique 'Nome Subfunção':")
print(subfuncCounts)
#
#
#
#
#
#| classes: custompython

# Create a pivot table to see spending per year on different "Nome Subfunção"
pivot_table = dfDefesaNacional.pivot_table(
    values='Valor',
    index='Ano da Emenda',
    columns='Nome Subfunção',
    aggfunc='sum',
    fill_value=0
)
pivot_table
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
