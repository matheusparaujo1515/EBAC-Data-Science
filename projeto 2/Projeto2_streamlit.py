import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
import numpy as np

sns.set(context='talk', style='ticks')

st.set_page_config(
     page_title="Projeto 2",
     page_icon="https://cdn-icons-png.flaticon.com/512/7500/7500336.png",
     layout="wide",
)

st.write('# Análise exploratória da previsão de renda')

st.write('\n')
st.write('\n')


renda = pd.read_csv('C:/Users/mathe/OneDrive/16 - MODULO - MÉTODOS DE ANÁLISE/projeto 2/input/previsao_de_renda.csv')

st.write('Iremos utilizar apenas as variáveis que o modelo final de regressão selecionou.')
st.write('Sendo elas:')

st.markdown('''
| Variável  | Descrição | Tipo   |
| --------- | ------- | -------- |
| tempo_emprego | tempo de emprego em anos  | ponto flutuante |
| sexo| M = 'Masculino'; F = 'Feminino' |  inteiro |
| educacao | Nível de educação (ex: secundário, superior etc | texto  |
| idade | Idade em anos | inteiro  |
| posse_de_imovel |   T = 'possui'; F = 'não possui' | binária  |
| renda |   Valor renda mensal | ponto flutuante |            
''')


st.markdown('## Gráficos de contagem')
variaveis = ['sexo', 'educacao', 'tipo_renda', 'qtd_filhos', 'idade', 'posse_de_imovel']

for variavel in variaveis:
    fig, ax = plt.subplots(figsize=(12,8))
    sns.countplot(data=renda, x=variavel, ax=ax)
    ax.set_title(f'Contagem por {variavel}')
    ax.set_xlabel(variavel)
    ax.set_ylabel('Contagem')
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)

intervalos = pd.cut(renda['tempo_emprego'], bins=10)
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=renda, x=intervalos, ax=ax)
ax.set_title('Contagem por Tempo de Emprego')
ax.set_xlabel('Tempo de Emprego em anos')
ax.set_ylabel('Contagem')
ax.tick_params(axis='x', rotation=90)
st.pyplot(fig)


st.write('## Gráficos ao longo do tempo')
fig, ax = plt.subplots(4, 1, figsize=(15, 60))

variaveis = ['sexo', 'educacao', 'tipo_renda', 'posse_de_imovel']

for i, variavel in enumerate(variaveis):
    sns.lineplot(x='data_ref', y='renda', hue=variavel, data=renda, ax=ax[i])
    ax[i].set_ylabel('Renda')
    ax[i].set_xlabel('Data de Referência')
    ax[i].set_title(f'Renda ao longo do tempo por {variavel.capitalize()}')
    ax[i].tick_params(axis='x', rotation=90)
    plt.setp(ax[i].get_legend().get_texts(), fontsize='small')
plt.subplots_adjust(hspace=0.5)
st.pyplot(fig)


st.markdown('## Gráfico de correlação')

variaveis = renda[['renda', 'tempo_emprego', 'sexo', 'educacao', 'tipo_renda', 'qtd_filhos', 'idade', 'posse_de_imovel']]
variaveis_encoded = pd.get_dummies(variaveis, drop_first=True)
correlation_matrix = variaveis_encoded.corr()

plt.figure(figsize=(10, 8))
heatmap = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, annot_kws={"size": 10})
heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=90)
heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=0)
plt.title('Matriz de Correlação')
st.pyplot(plt)


st.markdown('### A variável que teve maior correlação com renda foi tempo de emprego. Vamos analisá-la mais de perto.')
st.markdown('\n')

@st.cache_data()
def load_data(nrows):
    return renda.head(nrows)


data = load_data(15000)

if st.checkbox('Mostrar dataframe renda X tempo_emprego'):
    st.subheader('Dados')
    st.write(data[['data_ref', 'tempo_emprego', 'renda']])


# Plotar o barplot
st.subheader('Renda média por tempo de emprego')

renda_cleaned = renda.dropna(subset=['tempo_emprego'])

bar_chart = alt.Chart(renda_cleaned).mark_bar().encode(
    x=alt.X('tempo_emprego:O', bin=alt.Bin(
        maxbins=10), title='Tempo de Emprego'),
    y=alt.Y('mean(renda):Q', title='Renda Média'),
    tooltip=[alt.Tooltip('tempo_emprego:O', title='Tempo de Emprego'), alt.Tooltip(
        'mean(renda):Q', title='Renda Média')]
).properties(
    width=600,
    height=400
)

st.altair_chart(bar_chart, use_container_width=True)


# Plotar o countplot
st.subheader('Tempo de emprego x Renda')

count_data = pd.cut(renda_cleaned['tempo_emprego'],
                    bins=10).value_counts().reset_index()
count_data.columns = ['intervalo', 'contagem']

count_data['intervalo'] = count_data['intervalo'].astype(str)
count_data['intervalo'] = count_data['intervalo'].str.replace('(', '[')
count_data['intervalo'] = pd.Categorical(count_data['intervalo'], categories=sorted(
    count_data['intervalo'].unique()), ordered=True)

bar_chart2 = alt.Chart(count_data).mark_bar().encode(
    x=alt.X('intervalo', sort=None, title='Intervalo em anos'),
    y='contagem:Q',
    tooltip=['intervalo', 'contagem']
).properties(
    width=600,
    height=400
)

st.altair_chart(bar_chart2, use_container_width=True)















