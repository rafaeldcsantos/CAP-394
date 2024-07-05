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
#| classes: custompython
import pandas as pd
import plotly.express as px
#
#
#
#
#
#| classes: custompython
file = 'Resources/Data/Emendas/Emendas.csv'
# Read the CSV file using the specified separator and encoding.
df = pd.read_csv(file, sep=';', encoding='ISO-8859-1')
# Convert the Valor field to numeric, taking care of the decimals'
# separator:
df['Valor'] = df['Valor Empenhado'].str.replace('.', '', regex=False).\
                                    str.replace(',', '.').astype(float)
# We don't really need some of the fields (redundant ones):
df = df.drop(['Código da Emenda', 'Nome do Autor da Emenda', 'Número da emenda',
              'Código Função','Código Subfunção'], axis=1)
# We don't really need some of the payment fields (only 'Valor'):
df = df.drop(['Valor Empenhado', 'Valor Liquidado', 'Valor Pago', 
              'Valor Restos A Pagar Inscritos','Valor Restos A Pagar Cancelados',
              'Valor Restos A Pagar Pagos'], axis=1)                                    
# Display part of the data.
df
#
#
#
#
#
#| classes: custompython
countLoG = df["Localidade do gasto"].value_counts()
# Print the result
print(countLoG)
#
#
#
#
#
#| classes: custompython
countNF = df["Nome Função"].value_counts()
# Print the result
print(countNF)
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
dfId = df[df["Código do Autor da Emenda"] != "S/I"]
#
#
#
#
#
#| classes: custompython
dfNacional = dfId[dfId["Localidade do gasto"] == "Nacional"]
dfStates = dfId[dfId["Localidade do gasto"].str.contains(r"\(\w{2}\)", regex=True)]
#
#
#
#
#
#| classes: custompython
dfDefesaNacional = dfNacional[dfNacional["Nome Função"] == "Defesa nacional"]
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
