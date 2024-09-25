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
        "RFV data", type=['csv', 'xlsx'])

    # Verifica se há conteúdo carregado na aplicação
    if (data_file_1 is not None):
        try:
            if data_file_1.name.endswith('.csv'):
                df_compras = pd.read_csv(data_file_1)
            elif data_file_1.name.endswith('.xlsx'):
                # Tenta carregar o arquivo sem parse_dates
                df_compras = pd.read_excel(data_file_1)
                st.write(df_compras.columns)  # Verifica as colunas para garantir que tudo está correto

        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")
            return

        # Verifica se o DataFrame está vazio
        if df_compras.empty:
            st.error('O arquivo carregado está vazio.')
            return

        # Continue o processamento dos dados sem usar `parse_dates`
        st.write('## Recência (R)')
        st.write('Quantos dias faz que o cliente fez a sua última compra?')

        # Considerando que os dados de recência já existem no arquivo
        df_recencia = df_compras[['ID_cliente', 'Recencia']]
        st.write(df_recencia.head())

        st.write('## Frequência (F)')
        st.write('Quantas vezes cada cliente comprou com a gente?')
        df_frequencia = df_compras[['ID_cliente', 'Frequencia']]
        st.write(df_frequencia.head())

        st.write('## Valor (V)')
        st.write('Quanto que cada cliente gastou no período?')
        df_valor = df_compras[['ID_cliente', 'Valor']]
        st.write(df_valor.head())

        st.write('## Tabela RFV final')
        df_RF = df_recencia.merge(df_frequencia, on='ID_cliente')
        df_RFV = df_RF.merge(df_valor, on='ID_cliente')
        df_RFV.set_index('ID_cliente', inplace=True)

        # Exibir a tabela completa com rolagem
        st.write('## Tabela após a criação dos grupos')
        st.dataframe(df_RFV, height=400)  # Ajuste a altura conforme necessário

        st.write('## Segmentação utilizando o RFV')
        st.write("Um jeito de segmentar os clientes é criando quartis para cada componente do RFV, sendo que o melhor quartil é chamado de 'A', o segundo melhor quartil de 'B', o terceiro melhor de 'C' e o pior de 'D'. O melhor e o pior depende da componente. Por exemplo, quanto menor a recência melhor é o cliente (pois ele comprou com a gente tem pouco tempo) logo o menor quartil seria classificado como 'A', já para a componente frequência a lógica se inverte, ou seja, quanto maior a frequência do cliente comprar com a gente, melhor ele/a é, logo, o maior quartil recebe a letra 'A'.")

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
        st.dataframe(df_RFV, height=400)  # Exibir tabela com rolagem

        st.write('Quantidade de clientes por grupos')
        st.write(df_RFV['RFV_Score'].value_counts())  # Contar perfis

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
                      'BAA': 'Enviar cupons de desconto para tentar recuperar clientes com alto valor de compra.',
                      'BAB': 'Manter contato com promoções personalizadas.',
                      'BAC': 'Oferecer incentivos para compras adicionais e aumentar a frequência.',
                      'BAD': 'Enviar cupons de desconto para tentar recuperar clientes.',
                      'BBA': 'Manter contato e enviar promoções para aumentar o engajamento.',
                      'BBB': 'Enviar promoções regulares para manter o cliente engajado.',
                      'BBC': 'Enviar ofertas especiais para incentivar compras adicionais.',
                      'BBD': 'Oferecer promoções para tentar recuperar clientes.',
                      'BCA': 'Enviar ofertas especiais para aumentar o valor médio de compra.',
                      'BCB': 'Manter contato e enviar promoções para incentivar mais compras.',
                      'BCC': 'Oferecer incentivos para compras adicionais e aumentar o valor de compra.',
                      'BCD': 'Enviar promoções para tentar recuperar clientes.',
                      'BDA': 'Enviar cupons de desconto para tentar aumentar a frequência de compra.',
                      'BDB': 'Oferecer promoções para incentivar compras adicionais.',
                      'BDC': 'Enviar ofertas para tentar aumentar a frequência de compra.',
                      'BDD': 'Enviar promoções para tentar recuperar clientes.',
                      'CAA': 'Enviar cupons de desconto para tentar aumentar o engajamento.',
                      'CAB': 'Oferecer promoções para tentar recuperar clientes.',
                      'CAC': 'Enviar promoções para incentivar compras adicionais.',
                      'CAD': 'Oferecer descontos para tentar recuperar clientes.',
                      'CBA': 'Enviar promoções para tentar aumentar a frequência de compra.',
                      'CBB': 'Manter contato e enviar ofertas para manter o cliente engajado.',
                      'CBC': 'Oferecer incentivos para compras adicionais e aumentar o valor médio de compra.',
                      'CBD': 'Enviar promoções para tentar recuperar clientes.',
                      'CCA': 'Oferecer promoções para aumentar o valor médio de compra.',
                      'CCB': 'Enviar ofertas especiais para incentivar mais compras.',
                      'CCC': 'Manter contato com ofertas personalizadas para aumentar o engajamento.',
                      'CCD': 'Enviar promoções para tentar recuperar clientes.',
                      'CDA': 'Enviar cupons de desconto para aumentar a frequência de compra.',
                      'CDB': 'Oferecer promoções para incentivar compras adicionais.',
                      'CDC': 'Enviar ofertas para tentar aumentar a frequência de compra.',
                      'CDD': 'Enviar promoções para tentar recuperar clientes.',
                      'DAA': 'Enviar cupons de desconto para tentar recuperar clientes com alto valor de compra.',
                      'DAB': 'Oferecer promoções para tentar recuperar clientes.',
                      'DAC': 'Enviar promoções para incentivar compras adicionais.',
                      'DAD': 'Enviar ofertas para tentar recuperar clientes.',
                      'DBA': 'Enviar cupons de desconto para aumentar a frequência de compra.',
                      'DBB': 'Oferecer promoções para tentar aumentar o valor médio de compra.',
                      'DBC': 'Enviar ofertas especiais para incentivar compras adicionais.',
                      'DBD': 'Enviar promoções para tentar recuperar clientes.',
                      'DCA': 'Oferecer promoções para tentar aumentar o valor médio de compra.',
                      'DCB': 'Enviar ofertas especiais para incentivar mais compras.',
                      'DCC': 'Manter contato e oferecer promoções para manter o cliente engajado.',
                      'DCD': 'Enviar promoções para tentar recuperar clientes.',
                      'DDA': 'Enviar cupons de desconto para aumentar a frequência de compra.',
                      'DDB': 'Oferecer promoções para incentivar compras adicionais.',
                      'DDC': 'Enviar ofertas para tentar aumentar a frequência de compra.',
                      'DDD': 'Clientes que gastaram pouco e compraram pouco; considerar se vale a pena ações adicionais ou focar em clientes mais promissores.'
                      }

        df_RFV['acoes de marketing/crm'] = df_RFV['RFV_Score'].map(dict_acoes)
        st.dataframe(df_RFV, height=400)  # Exibir tabela com rolagem

        # Download do arquivo RFV segmentado
        df_xlsx = to_excel(df_RFV)
        st.download_button(label='📥 Download',
                           data=df_xlsx,
                           file_name='RFV_output.xlsx')

        st.write('Quantidade de clientes por tipo de ação')
        st.write(df_RFV['acoes de marketing/crm'].value_counts(dropna=False))


if __name__ == '__main__':
    main()
