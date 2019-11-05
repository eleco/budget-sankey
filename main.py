import pandas as pd 
import plotly.graph_objects as go
import random

def rebuild_index(dataframe):
    dataframe.index = pd.RangeIndex(len(dataframe.index))
    dataframe.index = range(len(dataframe.index))


#import csv
df = pd.read_csv('./budget.csv') 

#drop columns with nan
df=df.dropna(axis=1, how='all')

#sum by category
df=df.groupby(['Category'])[["Amount"]].sum()

#create index
df.reset_index(inplace=True)

#create the nodes dataframe
nodes= pd.DataFrame(columns=['label','color'])
nodes['label'] = df['Category'].copy()
nodes['color'] = 'red'
nodes=nodes.append([{ 'label':'Income','color':'blue' }])
rebuild_index(nodes)

#split positive from negative cashflows
df_inflow = df[df['Amount'] > 0]
df_outflow = df[df['Amount'] < 0]

#link positive cashflows
link_in=pd.DataFrame(columns=['source','target','value'])
link_in['source'] = df_inflow.index.map(str)
rebuild_index(df_inflow)
link_in['target'] = str(nodes.index.max())
link_in['value'] = df_inflow['Amount'].map(str)

#link negative cashflows
link_out=pd.DataFrame(columns=['source','target','value'])
link_out['target'] = df_outflow.index.map(str)
rebuild_index(df_outflow)
link_out['value'] = (df_outflow['Amount']*-1).map(str)
link_out['source'] = str(nodes.index.max())

links=link_in.append(link_out, ignore_index=True)

#draw sankey diagram
fig = go.Figure(data=[go.Sankey(node=nodes.to_dict('list'), link=links.to_dict('list'))])
fig.update_layout(title_text="Sankey Diagram", font_size=10)
fig.show()