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
#| classes: custompython
import pandas as pd
import re
import warnings
import networkx as nx
#
#
#
#| classes: custompython
dir = "Resources/Data/CAPES-Projetos/"
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UserWarning, 
                            module=re.escape('openpyxl.styles.stylesheet'))
    dfProjetos = pd.read_excel(dir+"br-capes-colsucup-projeto-2020-2021-11-10.xlsx")
    dfMembros = pd.read_excel(dir+"br-capes-colsucup-membro-2020-2021-11-10.xlsx")
#
#
#
#
#| classes: custompython
dfProjetos = dfProjetos[
    (dfProjetos['NM_TIPO_SITUACAO_ATUAL']=='EM ANDAMENTO') &
    (dfProjetos['SG_ENTIDADE_ENSINO'] == 'INPE')]
     
dfProjetos = dfProjetos[['AN_BASE','NM_PROGRAMA_IES','AN_INICIO_PROGRAMA',
                         'SG_ENTIDADE_ENSINO',
                         'NM_AREA_AVALIACAO','NM_MODALIDADE_PROGRAMA',
                         'NM_AREA_CONCENTRACAO','ID_PROJETO','NM_PROJETO',
                         'NM_NATUREZA_PROJETO','DH_INICIO','DT_SITUACAO_ATUAL',
                         'IN_BOLSA','IN_OUTRO_AUXILIO']]
dfMembros = dfMembros[['ID_PROJETO','IN_RESPONSAVEL_PROJETO','ID_PESSOA',
                       'DS_TIPO_MEMBRO','NM_PAIS_NACIONALIDADE_MEMBRO']]
#
#
#
#| classes: custompython
dfUnião = pd.merge(dfProjetos, dfMembros, on='ID_PROJETO', how='inner')
#
#
#
#| classes: custompython
print(dfProjetos.shape)
print(dfMembros.shape)
print(dfUnião.shape)
#
#
#
#
#| classes: custompython
dfUnião.to_csv(dir+'INPE2020.csv', index=False)
#
#
#
#
#
#| classes: custompython
dfRede = dfUnião[['ID_PROJETO', 'ID_PESSOA', 'NM_PROJETO', 'DS_TIPO_MEMBRO']]
dfRede.to_csv(dir+'INPE2020-Rede.csv', index=False)
#
#
#
#
#| classes: custompython

# Create the graph
G = nx.Graph()

# Add nodes with attributes
for _, row in df.iterrows():
    G.add_node(row['ID_PESSOA'], label=row['ID_PESSOA'], tipo_membro=row['DS_TIPO_MEMBRO'])

# Add edges based on project collaboration
projects = df.groupby('ID_PROJETO')['ID_PESSOA'].apply(list)
for project, participants in projects.items():
    for i in range(len(participants)):
        for j in range(i + 1, len(participants)):
            G.add_edge(participants[i], participants[j], project=project)

            

nx.write_gexf(G,dir+"INPE2020-Rede.gexf")


#
#
#
#
#
#| classes: custompython
#
#
#
#
#
#| classes: custompython
#
#
#
#
#
#| classes: custompython
#
#
#
#
#
