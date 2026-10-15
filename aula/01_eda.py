import pandas as pd
import plotly.express as px

# read the data
df = pd.read_csv('data/coffee_sales.csv')
df.head(10)

# convert data column to datetime
df['data'] = pd.to_datetime(df['data'])
df.head()

# ensuring that date is in order
df = df.sort_values('data')
df.head()

# counting na's
df.isna().sum()


# plot time series
fig = px.line(df, 
    x='data', 
    y='vendas', 
    title='Vendas diárias da cafeteria'
)

fig.update_layout(
    xaxis_title='Data', 
    yaxis_title='Unidades vendidas'
)

# moving average 
df['media_7_dias'] = df['vendas'].rolling(7).mean()
df.head(10)

# plot time series with MA
fig = px.line(df, 
    x='data', 
    y=['vendas', 'media_7_dias'], 
    title='Vendas e média móvel'
)

fig.update_layout(
    xaxis_title='Data', 
    yaxis_title='Unidades vendidas', 
    legend_title='Série'
)


