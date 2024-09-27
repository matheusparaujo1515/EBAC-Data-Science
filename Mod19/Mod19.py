import pandas            as pd
import seaborn           as sns
import matplotlib.pyplot as plt
import streamlit         as st
import xlsxwriter
from io                  import BytesIO
from PIL                 import Image


#Config para melhorar visual dos gráficos
custom_params = {'axes.spines.right': False, 'axes.spines.top': False}
sns.set_theme(style='ticks', rc = custom_params)

#Função para adicionar all nas caixas de filtro
@st.cache_data
def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

#Função para ler os dados mais rápido
@st.cache_data(show_spinner= True)
def load_data(file_data):
    try:
        return pd.read_csv(file_data, sep=';')
    except:
        return pd.read_excel(file_data)

# Função para converter o df para csv
@st.cache_data(show_spinner= True)
def df_toString(df):
    return df.to_csv(index=False).encode('utf-8')

#Função para converter o df para excel
@st.cache_data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data


# App principal
def main():
    icon = 'https://github.com/matheusparaujo1515/EBAC-Data-Science/blob/main/Mod19/img/icon.png'
    logo = 'https://github.com/matheusparaujo1515/EBAC-Data-Science/blob/main/Mod19/img/logo.png'
    
    st.set_page_config(page_title= 'Telemarketing analisys', 
                       page_icon= icon,
                       layout= 'wide',
                       initial_sidebar_state='expanded')

    st.write('# Telemarketing Analisys')
    st.sidebar.image(logo, use_column_width=True)
    
    
    #UPLOAD ARQUIVO DA BASE DE DADOS
    st.sidebar.write('## Faça upload do arquivo: ')
    data_file = st.sidebar.file_uploader('Bank marketing data', type=['csv', 'xlsx'])
    
    if (data_file is not None):
        bank_raw = load_data(data_file)
        bank = bank_raw.copy()

        st.write('## Antes dos filtros')
        st.write(bank_raw.head())
        st.markdown('---')
        
        with st.sidebar.form(key='my_form'):
            #SELECIONA O TIPO DE GRÁFICO
            graph_type = st.radio('Tipo de gráfico: ', ('Barras', 'Pizza'))           
            
            
            # IDADES
            max_age = int(bank.age.max())
            min_age = int(bank.age.min())
            idades = st.slider(label='Idade',
                                    min_value=min_age, 
                                    max_value=max_age, 
                                    value=(min_age, max_age), 
                                    step=1)
            st.write('IDADES: ', idades)
            st.write('IDADE MIN: ', idades[0])
            st.write('IDADE MAX: ', idades[1])
            
            
            #PROFISSOES
            jobs_list = bank.job.unique().tolist()
            jobs_list.append('all')
            jobs_selected = st.multiselect('Profissões', jobs_list, ['all'])
            
            #ESTADO CÍVIL
            marital_list = bank.marital.unique().tolist()
            marital_list.append('all')
            marital_selected = st.multiselect('Estado Cívil', marital_list, ['all'])
            
            #DEFAULT
            default_list = bank.default.unique().tolist()
            default_list.append('all')
            default_list = st.multiselect('Default: ', default_list, ['all'])
            
            #HOUSING
            housing_list = bank.housing.unique().tolist()
            housing_list.append('all')
            housing_list = st.multiselect('Possui fin. Imobiliário: ', housing_list, ['all'])
            
            #LOAN
            loan_list = bank.loan.unique().tolist()
            loan_list.append('all')
            loan_list = st.multiselect('Empréstimo: ', loan_list, ['all'])
            
            #CONTACT
            contact_list = bank.contact.unique().tolist()
            contact_list.append('all')
            contact_list = st.multiselect('Contato: ', contact_list, ['all'])      
            
            #MONTH
            month_list = bank.month.unique().tolist()
            month_list.append('all')
            month_list = st.multiselect('Mês', month_list, ['all'])
            
            #DAY_OF_WEEK
            day_list = bank.day_of_week.unique().tolist()
            day_list.append('all')
            day_list = st.multiselect('Dia da semana: ', day_list, ['all'])
            
            #Y
            y_list = bank.y.unique().tolist()
            y_list.append('all')
            y_list = st.multiselect('Aceite: ', y_list, ['all'])
            
        
            #FILTROS
            bank = bank[(bank['age'] >= idades[0]) & (bank['age'] <= idades[1])]
            bank = multiselect_filter(bank, 'job', jobs_selected)
            bank = multiselect_filter(bank, 'marital', marital_list)
            bank = multiselect_filter(bank, 'default', default_list)
            bank = multiselect_filter(bank, 'housing', housing_list)
            bank = multiselect_filter(bank, 'loan', loan_list)
            bank = multiselect_filter(bank, 'contact', contact_list)
            bank = multiselect_filter(bank, 'month', month_list)
            bank = multiselect_filter(bank, 'day_of_week', day_list)
            bank = multiselect_filter(bank, 'y', y_list)
            
            
            #BOTÃO APLICAR
            submit_button = st.form_submit_button(label='Aplicar')
            
            
        st.write('## Após os filtros')
        st.write(bank.head())
        
        csv = df_toString(bank)
        df_xlsx = to_excel(bank)
        st.write('### Faça Download do arquivo filtrado')
        st.download_button(label='📥 Download data as EXCEL',
                            data=df_xlsx ,
                            file_name= 'df_excel.xlsx')
        st.markdown('---')

        
        #PLOT1.0
        bank_raw_target_perc = bank_raw.y.value_counts(normalize = True).to_frame()*100
        bank_raw_target_perc = bank_raw_target_perc.sort_index()
        
        bank_target_perc = bank.y.value_counts(normalize = True).to_frame()*100
        bank_target_perc = bank_target_perc.sort_index()

        #PLOT1.1
        if graph_type == 'Barras':
            fig, ax = plt.subplots(1, 2, figsize=(5,3))
            sns.barplot(x=bank_raw_target_perc.index, y='proportion', data=bank_raw_target_perc, ax=ax[0])
            ax[0].bar_label(ax[0].containers[0])
            ax[0].set_title('Dados brutos', fontweight="bold")

            # Para os dados filtrados
            sns.barplot(x=bank_target_perc.index, y='proportion', data=bank_target_perc, ax=ax[1])
            ax[1].bar_label(ax[1].containers[0])
            ax[1].set_title('Dados filtrados', fontweight="bold")
        else:
            fig, ax = plt.subplots(1, 2, figsize=(5,3))
            ax[0].pie(bank_raw_target_perc['proportion'], labels=bank_raw_target_perc.index, autopct='%1.1f%%')
            ax[0].set_title('Dados brutos', fontweight="bold")

            # Gráfico de pizza para os dados filtrados
            ax[1].pie(bank_target_perc['proportion'], labels=bank_target_perc.index, autopct='%1.1f%%')
            ax[1].set_title('Dados filtrados', fontweight="bold")

        st.write('### Proporção de aceite')
        st.pyplot(plt)

main()
