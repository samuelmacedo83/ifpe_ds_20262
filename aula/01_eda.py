import pandas as pd
import plotly.express as px

# read the data
df = pd.read_csv('../data/coffee_sales.csv')
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

# dias da semana 
df['dia_semana'] = df['data'].dt.dayofweek
df.head()

# media por dia 
media_por_dia = df.groupby('dia_semana')['vendas'].mean()

media_por_dia.index = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
fig = px.bar(
    x=media_por_dia.index, 
    y=media_por_dia.values, 
    title='Média de vendas por dia da semana'
)
fig.update_layout(
    xaxis_title='Dia da semana', 
    yaxis_title='Média de unidades vendidas'
)

# boxplots
fig = px.box(
    df, 
    x='dia_semana', 
    y='vendas', 
    points='outliers',
    title='Distribuição das vendas por dia da semana'
)
fig.update_xaxes(
    tickvals=[0, 1, 2, 3, 4, 5, 6],
    ticktext=['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
)
fig.update_layout(
    xaxis_title='Dia da semana', 
    yaxis_title='Unidades vendidas'
)

