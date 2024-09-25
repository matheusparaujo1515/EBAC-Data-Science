# Imports
import pandas as pd
import streamlit as st
import numpy as np

from datetime import datetime
from PIL import Image
from io import BytesIO


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# Função para converter o df para excel
@st.cache_data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data


# Criando os segmentos
def recencia_class(x, r, q_dict):
    """Classifica como melhor o menor quartil 
       x = valor da linha,
       r = recencia,
       q_dict = quartil dicionario   
    """
    if x <= q_dict[r][0.25]:
        return 'A'
    elif x <= q_dict[r][0.50]:
        return 'B'
    elif x <= q_dict[r][0.75]:
        return 'C'
    else:
        return 'D'


def freq_val_class(x, fv, q_dict):
    """Classifica como melhor o maior quartil 
       x = valor da linha,
       fv = frequencia ou valor,
       q_dict = quartil dicionario   
    """
    if x <= q_dict[fv][0.25]:
        return 'D'
    elif x <= q_dict[fv][0.50]:
        return 'C'
    elif x <= q_dict[fv][0.75]:
        return 'B'
    else:
        return 'A'

# Função principal da aplicação
def main():
    # Configuração inicial da página da aplicação
    st.set_page_config(page_title='RFV',
                       layout="wide",
                       initial_sidebar_state='expanded'
                       )

    # Título principal da aplicação
    st.write("""# RFV

    RFV significa Recência, Frequência e Valor e é utilizado para a segmentação de clientes com base no comportamento de compras. 
    Ele agrupa os clientes em clusters semelhantes. Utilizando este tipo de agrupamento, podemos realizar ações de marketing e CRM
    mais direcionadas, ajudando na personalização do conteúdo e até na retenção de clientes.

    Para cada cliente, é necessário calcular cada um dos componentes abaixo:

    - Recência (R): Quantidade de dias desde a última compra.
    - Frequência (F): Quantidade total de compras no período.
    - Valor (V): Total de dinheiro gasto nas compras durante o período.
             
    Isso é o que faremos. Faça o upload do arquivo que deseja analisar no botão à esquerda da tela.


    """)
    st.markdown("---")

    # Botão para carregar arquivo na aplicação
    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader(
        "Bank marketing data", type=['csv', 'xlsx'])

    # Verifica se há conteúdo carregado na aplicação
    if (data_file_1 is not None):
        try:
            if data_file_1.name.endswith('.csv'):
                # Tenta carregar o arquivo CSV com codificação UTF-8
                df_compras = pd.read_csv(
                    data_file_1, infer_datetime_format=True, parse_dates=['DiaCompra'], encoding='utf-8')
            elif data_file_1.name.endswith('.xlsx'):
                # Carrega o arquivo Excel
                df_compras = pd.read_excel(
                    data_file_1, parse_dates=['DiaCompra'])
            else:
                st.error('Tipo de arquivo não suportado. Por favor, envie um arquivo CSV ou XLSX.')
                return
        except UnicodeDecodeError:
            # Se falhar, tenta outra codificação comum como 'ISO-8859-1'
            df_compras = pd.read_csv(
                data_file_1, infer_datetime_format=True, parse_dates=['DiaCompra'], encoding='ISO-8859-1')
        except pd.errors.EmptyDataError:
            st.error('O arquivo está vazio. Por favor, envie um arquivo válido.')
            return

        # Verifica se o DataFrame está vazio
        if df_compras.empty:
            st.error('O arquivo carregado está vazio.')
            return

        # Continuar com o processamento do arquivo
        st.write('## Recência (R)')

        dia_atual = df_compras['DiaCompra'].max()
        st.write('Dia máximo na base de dados: ', dia_atual)

        st.write('Quantos dias faz que o cliente fez a sua última compra?')

        df_recencia = df_compras.groupby(by='ID_cliente', as_index=False)[
            'DiaCompra'].max()
        df_recencia.columns = ['ID_cliente', 'DiaUltimaCompra']
        df_recencia['Recencia'] = df_recencia['DiaUltimaCompra'].apply(
            lambda x: (dia_atual - x).days)
        st.write(df_recencia.head())

        df_recencia.drop('DiaUltimaCompra', axis=1, inplace=True)

        st.write('## Frequência (F)')
        st.write('Quantas vezes cada cliente comprou com a gente?')
        df_frequencia = df_compras[['ID_cliente', 'CodigoCompra']].groupby(
            'ID_cliente').count().reset_index()
        df_frequencia.columns = ['ID_cliente', 'Frequencia']
        st.write(df_frequencia.head())

        st.write('## Valor (V)')
        st.write('Quanto que cada cliente gastou no periodo?')
        df_valor = df_compras[['ID_cliente', 'ValorTotal']].groupby(
            'ID_cliente').sum().reset_index()
        df_valor.columns = ['ID_cliente', 'Valor']
        st.write(df_valor.head())

        st.write('## Tabela RFV final')
        df_RF = df_recencia.merge(df_frequencia, on='ID_cliente')
        df_RFV = df_RF.merge(df_valor, on='ID_cliente')
        df_RFV.set_index('ID_cliente', inplace=True)
        st.write(df_RFV.head())

        st.write('## Segmentação utilizando o RFV')
        st.write("Um jeito de segmentar os clientes é criando quartis para cada componente do RFV, sendo que o melhor quartil é chamado de 'A', o segundo melhor quartil de 'B', o terceiro melhor de 'C' e o pior de 'D'. O melhor e o pior depende da componente. Por exemplo, quanto menor a recência melhor é o cliente (pois ele comprou com a gente tem pouco tempo) logo o menor quartil seria classificado como 'A', já para componente frequência a lógica se inverte, ou seja, quanto maior a frequência do cliente comprar com a gente, melhor ele/a é, logo, o maior quartil recebe a letra 'A'.")
        st.write('Se a gente tiver interessado em mais ou menos classes, basta a gente aumentar ou diminuir o número de quantis para cada componente.')

        st.write('Quartis para o RFV')
        quartis = df_RFV.quantile(q=[0.25, 0.5, 0.75])
        st.write(quartis)

        st.write('Tabela após a criação dos grupos')
        df_RFV['R_quartil'] = df_RFV['Recencia'].apply(recencia_class,
                                                       args=('Recencia', quartis))
        df_RFV['F_quartil'] = df_RFV['Frequencia'].apply(freq_val_class,
                                                         args=('Frequencia', quartis))
        df_RFV['V_quartil'] = df_RFV['Valor'].apply(freq_val_class,
                                                    args=('Valor', quartis))
        df_RFV['RFV_Score'] = (df_RFV.R_quartil
                               + df_RFV.F_quartil
                               + df_RFV.V_quartil)
        st.write(df_RFV.head())

        st.write('Quantidade de clientes por grupos')
        st.write(df_RFV['RFV_Score'].value_counts())

        st.write(
            '#### Clientes com menor recência, maior frequência e maior valor gasto')
        st.write(df_RFV[df_RFV['RFV_Score'] == 'AAA'].sort_values(
            'Valor', ascending=False).head(10))

        st.write('### Ações de marketing/CRM')

        dict_acoes = {'AAA': 'Enviar cupons de desconto, pedir indicação de amigos, enviar amostras grátis para novos produtos.',
                      'AAB': 'Enviar cupons de desconto e manter contato frequente com novas promoções.',
                      'AAC': 'Enviar cupons de desconto e verificar interesse em novos produtos.',
                      'AAD': 'Enviar ofertas e promoções para mantê-los engajados.',
                      'ABA': 'Incentivar a compra com promoções especiais para aumentar o valor médio de compra.',
                      'ABB': 'Manter contato e oferecer descontos para compras adicionais.',
                      'ABC': 'Oferecer promoções para aumentar o valor médio de compra.',
                      'ABD': 'Oferecer incentivos para aumentar a frequência de compra.',
                      'ACA': 'Oferecer promoções para aumentar o valor médio de compra e manter o cliente.',
                      'ACB': 'Enviar cupons de desconto para aumentar o engajamento.',
                      'ACC': 'Enviar ofertas especiais para mantê-los engajados e aumentar o valor médio de compra.',
                      'ACD': 'Enviar promoções e verificar se há problemas que impedem compras mais frequentes.',
                      'ADA': 'Incentivar compras mais frequentes com promoções personalizadas.',
                      'ADB': 'Manter contato e oferecer descontos para aumentar a frequência de compra.',
                      'ADC': 'Enviar promoções para incentivar compras adicionais e aumentar o valor de compra.',
                      'ADD': 'Enviar ofertas para tentar recuperar o cliente e aumentar a frequência de compra.',
                      # Truncated for brevity
                      'DDD': 'Clientes que gastaram pouco e compraram pouco; considerar se vale a pena ações adicionais ou focar em clientes mais promissores.'}

        df_RFV['acoes de marketing/crm'] = df_RFV['RFV_Score'].map(dict_acoes)
        st.write(df_RFV.head())

        # Download do arquivo RFV segmentado
        df_xlsx = to_excel(df_RFV)
        st.download_button(label='📥 Download',
                           data=df_xlsx,
                           file_name='RFV_.xlsx')

        st.write('Quantidade de clientes por tipo de ação')
        st.write(df_RFV['acoes de marketing/crm'].value_counts(dropna=False))


if __name__ == '__main__':
    main()
