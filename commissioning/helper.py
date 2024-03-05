import matplotlib.pyplot as plt
import numpy as np # for linear algebra
import pandas as pd # for data handling
import plotly_express as px
import plotly.graph_objects as go

#read csv to get rms measurements and return data frames
def get_df(directory, date):
    
    df = pd.read_csv(directory+'test_results__LD_'+date+'.csv', index_col=False)
    df = df[['APA','Crate','WIB_CONNECTION','RMS Noise','Wire_type','Wire_No']]
    df.rename(columns={'FEMB_SN':'FEMB Serial Number', 'POSITION':'Position', 'WIB_CONNECTION':'WIB Connection', 'RMS Noise':'RMS', 'Wire_type':'Wire Type', 'Wire_No':'Wire Number'}, inplace=True)

    #separate E from W APA
    east_df = df.loc[(df['APA']=='NE') | (df['APA']=='SE')]
    west_df = df.loc[(df['APA']=='NW') | (df['APA']=='SW')]

    return east_df, west_df


#get df and return dictionary of mean rms per layer
def get_layer_mean(df, date):
    
    mean = {}    
    mean['U'] = df.loc[df['Wire Type']=='U', 'RMS'].mean()
    mean['V'] = df.loc[df['Wire Type']=='V', 'RMS'].mean()
    mean['Y'] = df.loc[df['Wire Type']=='Y', 'RMS'].mean()
   
    #standard error of the mean
    #print(size(df.loc[df['Wire Type']=='U']))
    std = {}   
    std['U'] = df.loc[df['Wire Type']=='U', 'RMS'].std()
    std['V'] = df.loc[df['Wire Type']=='V', 'RMS'].std()
    std['Y'] = df.loc[df['Wire Type']=='Y', 'RMS'].std()
        
    #print(mean_u, mean_v, mean_y)
    
    return mean, std


#susbtract rms between different dfs
def get_df_difference(df1, df2, wire_type):
    
    df = df1.loc[(df1['Wire Type']==wire_type)].copy(deep=False)
    df.loc[:,'RMS2']= df2['RMS'].loc[(df2['Wire Type']==wire_type)] 
    df = df.assign(Difference=df['RMS'] - df['RMS2']) 
    
    #print('df1\n', df1.head())
    #print('df2\n', df2.head())
    #print('df\n', df.head())
    
    return df


#auto separate plots by wire type
def get_simple_figure(df, x, y, name='Wire Type'):
    
    fig = go.Scatter(x=df[x], y=df[y], name=name)
    
    return fig


#auto separate plots by wire type
def get_scatter_figure(df, x, y, x_label='Wire Number', y_label='RMS'):
    
#    fig = px.scatter(combo_east_df, x="Date", y="RMS", color="Wire Type", symbol="Wire Type")
    fig = px.scatter(df, x=df[x], y=df[y], color='Wire Type', facet_col='Wire Type')
    
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend_title="Layer",
        hovermode="x",
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="RebeccaPurple"
        )
    )
    
    return fig