# Aula 1 — Séries temporais: conhecendo os dados
# Duração sugerida: 60 minutos.
# Execute cada célula (# %%) em ordem no Jupyter interativo.
# Use a pasta aulas/aula_01_eda como diretório de trabalho.

# %%
# 1. Importar as ferramentas
# pandas: ler e organizar tabelas.
# plotly.express: criar gráficos interativos.
import pandas as pd
import plotly.express as px

# %%
# 2. Ler o arquivo
# A base simula as vendas de uma cafeteria. Os dados são fictícios.
# Cada linha representa um dia.
# data: dia da venda. vendas: quantidade de unidades vendidas.
df = pd.read_csv('../data/coffee_sales.csv')
df.head()

# %%
# 3. Transformar a coluna data em datas reconhecidas pelo Python
# Ao ler um CSV, as datas podem ser interpretadas como texto.
df['data'] = pd.to_datetime(df['data'])
df.head()

# %%
# 4. Colocar os registros em ordem de data
# Em séries temporais, a ordem dos acontecimentos importa.
df = df.sort_values('data')
df.head()

# %%
# 5. Conhecer o tamanho da base
# Quantos dias temos registrados?
print('Quantidade de linhas:', len(df))
print('Primeira data:', df['data'].min())
print('Última data:', df['data'].max())

# %%
# 6. Verificar valores vazios
# O resultado mostra quantos valores vazios existem em cada coluna.
# Zero significa que não há valores vazios naquela coluna.
# Isso não verifica se um dia inteiro ficou sem registro.
df.isna().sum()

# %%
# 7. Resumir as vendas
# count: quantidade de valores preenchidos.
# mean: média. std: desvio padrão (uma medida de dispersão).
# min e max: menor e maior valor.
# 25%, 50% e 75%: quartis; 50% é a mediana.
# Nesta primeira leitura, concentre-se em mean, min e max.
df['vendas'].describe()

# %%
# 8. Fazer o primeiro gráfico
# No eixo horizontal: datas. No eixo vertical: unidades vendidas.
# Pergunta: as vendas parecem aumentar, diminuir ou ficar estáveis?
# x indica a coluna do eixo horizontal; y, a do eixo vertical.
fig = px.line(df, x='data', y='vendas', title='Vendas diárias da cafeteria')
fig.update_layout(xaxis_title='Data', yaxis_title='Unidades vendidas')
fig.show()

# %%
# 9. Calcular a média de vendas de sete dias consecutivos
# A média móvel suaviza as oscilações e ajuda a observar a tendência.
# Tendência: movimento de crescimento ou queda ao longo do tempo.
# Cada ponto usa o dia atual e os seis dias anteriores.
# Os primeiros seis resultados ficam vazios: ainda não há sete dias.
# Nesta base, há uma linha para cada dia, sem dias faltantes.
# A média móvel descreve o que aconteceu; não é uma previsão.
df['media_7_dias'] = df['vendas'].rolling(7).mean()
df.head(10)

# %%
# 10. Comparar as vendas com a média móvel
# Pergunta: ficou mais fácil enxergar a direção geral das vendas?
# Uma lista em y permite mostrar duas linhas no mesmo gráfico.
fig = px.line(df, x='data', y=['vendas', 'media_7_dias'], title='Vendas e média móvel')
fig.update_layout(xaxis_title='Data', yaxis_title='Unidades vendidas', legend_title='Série')
fig.show()

# %%
# 11. Identificar o dia da semana
# O pandas representa os dias com números:
# 0 = segunda, 1 = terça, 2 = quarta, 3 = quinta,
# 4 = sexta, 5 = sábado, 6 = domingo.
df['dia_semana'] = df['data'].dt.dayofweek
df.head()

# %%
# 12. Comparar as vendas médias por dia da semana
# groupby reúne os registros de cada dia da semana.
# mean calcula a média das vendas em cada grupo.
# Assim, comparamos todas as segundas, todas as terças etc.
media_por_dia = df.groupby('dia_semana')['vendas'].mean()
media_por_dia

# %%
# 13. Mostrar essa comparação em um gráfico de barras
# Sazonalidade: um padrão que se repete em intervalos regulares.
# Pergunta: quais dias têm a maior e a menor média de vendas?
# Este gráfico sugere um padrão semanal; não explica sua causa.
# Colocamos nomes nos dias para facilitar a leitura do gráfico.
media_por_dia.index = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
fig = px.bar(x=media_por_dia.index, y=media_por_dia.values, title='Média de vendas por dia da semana')
fig.update_layout(xaxis_title='Dia da semana', yaxis_title='Média de unidades vendidas')
fig.show()

# %%
# Boxplots: as vendas variam muito dentro de cada dia da semana?
# Cada caixa resume as vendas de todas as segundas, terças etc.
# A linha dentro da caixa é a mediana.
# A caixa contém a metade central dos valores (do quartil 25% ao 75%).
# Pontos além dos bigodes merecem investigação, mas não são erros comprovados.
fig = px.box(df, x='dia_semana', y='vendas', points='outliers',
             title='Distribuição das vendas por dia da semana')
fig.update_xaxes(tickvals=[0, 1, 2, 3, 4, 5, 6],
                 ticktext=['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'])
fig.update_layout(xaxis_title='Dia da semana', yaxis_title='Unidades vendidas')
fig.show()
# Compare com as médias: uma média sozinha não mostra a dispersão das vendas.

# %%
# 14. Comparar os meses
# Extraímos ano e mês da data. Exemplo: 2025-01.
df['mes'] = df['data'].dt.strftime('%Y-%m')

# %%
# Somamos as vendas de cada mês.
total_mensal = df.groupby('mes')['vendas'].sum()
total_mensal

# %%
# Também calculamos a média diária de cada mês.
# Atenção: fevereiro tem menos dias que janeiro.
# Um total menor não significa necessariamente vender menos por dia.
media_mensal = df.groupby('mes')['vendas'].mean()
media_mensal

# %%
# Quanto foi vendido em cada mês?
fig = px.bar(
    x=total_mensal.index, 
    y=total_mensal.values, 
    title='Total de vendas por mês'
)
fig.update_layout(xaxis_title='Mês', yaxis_title='Unidades vendidas no mês')
fig.show()
# Compare janeiro e fevereiro com a tabela de médias acima.

# %%
# 15. Investigar os maiores valores
# Ordenamos pelas vendas, da maior para a menor.
# Usamos outra variável para manter df em ordem de data.
# Um valor alto não é necessariamente um erro.
maiores_vendas = df.sort_values('vendas', ascending=False)
maiores_vendas[['data', 'vendas']].head()

# %%
# 16. Observar os dias próximos ao pico
# A primeira linha da tabela ordenada contém a maior venda.
data_pico = maiores_vendas['data'].iloc[0]
print('Data do pico:', data_pico)

# %%
# Escolhemos duas semanas antes e duas semanas depois dessa data.
inicio = data_pico - pd.Timedelta(days=14)
fim = data_pico + pd.Timedelta(days=14)

# Filtramos em duas etapas: primeiro a data inicial, depois a final.
recorte = df[df['data'] >= inicio]
recorte = recorte[recorte['data'] <= fim]

# %%
# O pico foi isolado ou os dias vizinhos também venderam muito?
# markers=True coloca um ponto em cada observação.
fig = px.line(recorte, 
              x='data', 
              y='vendas', 
              markers=True, 
              title='Vendas próximas ao maior pico'
)
fig.update_layout(xaxis_title='Data', yaxis_title='Unidades vendidas')

# Adicionamos uma bolinha vermelha sobre o maior valor observado.
# O destaque ajuda a investigar o pico; não é um detector automático de outliers.
venda_pico = maiores_vendas['vendas'].iloc[0]
fig.add_scatter(x=[data_pico], y=[venda_pico], mode='markers',
                marker=dict(color='red', size=13), name='Maior venda')
fig.show()

# %%
# 17. Discussão final
# Responda com base nas tabelas e nos gráficos:
# 1. O que cada linha representa? Em qual unidade medimos as vendas?
# 2. Existem valores vazios nas duas colunas originais?
# 3. As vendas apresentam uma tendência de crescimento?
# 4. Qual dia da semana tem a maior média de vendas?
# 5. Em qual data ocorreu a maior venda?
# 6. Podemos explicar esse pico somente com esses dados?
# 7. Por que comparar só o total mensal pode ser enganoso?
#
# Escreva três frases sobre o que você descobriu.
# Diferencie o que observou de uma possível explicação.
# Exemplo: um pico pode motivar investigar uma promoção,
# mas estes dados não mostram se houve uma promoção.
#
# Referência conceitual: capítulos 1 a 3 dos notebooks locais de
# Modern Time Series Forecasting with Python, 2ª edição.
