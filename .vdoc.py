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
#| classes: custompython
import pandas as pd
import matplotlib.pyplot as plt
#
#
#
#
#
#| classes: custompython
file = 'Resources/Data/Emendas/Emendas.csv'
# Read the CSV file using the specified separator and encoding.
df = pd.read_csv(file, sep=';', encoding='ISO-8859-1')
# Display the head of the dataframe.
print(df.head())
#
#
#
#
