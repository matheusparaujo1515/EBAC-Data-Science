# Imports
import pandas as pd
import streamlit as st
import joblib
import numpy as np
import os


# URL do ícone para a página
icon = 'https://github.com/matheusparaujo1515/EBAC-Data-Science/blob/c338eeb7c28bf946f95ce9daf4829fba4756a321/Projeto_Final/icon.png'

# Configuração inicial da página da aplicação
st.set_page_config(page_title='Classificador de diabetes',
                   page_icon=icon,
                   layout="wide",
                   initial_sidebar_state='expanded')

# Determinar o caminho absoluto do arquivo 'model.pkl'
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')

# Carregar o modelo salvo
pipeline = joblib.load('model.pkl')

# Carregar as colunas que o modelo viu durante o treinamento
expected_columns = pipeline.named_steps['scaler'].feature_names_in_

# Título da aplicação
st.markdown("<h1 style='text-align: center;'>Classificação de Pacientes com Diabetes</h1>",
            unsafe_allow_html=True)

# Perguntas para o usuário
st.header('Responda as perguntas abaixo:')

HighBP = st.selectbox('Paciente possui pressão alta?',
                      ['', 'Sim', 'Não'], index=0)
HighChol = st.selectbox('Paciente foi diagnosticado com colesterol alto?', [
                        '', 'Sim', 'Não'], index=0)
CholCheck = st.selectbox('Paciente fez um exame de colesterol nos últimos 5 anos?', [
                         '', 'Sim', 'Não'], index=0)
BMI = st.number_input('Qual o Índice de Massa Corporal (IMC) do paciente?',
                      min_value=10.0, max_value=100.0, step=0.1)
Smoker = st.selectbox('Paciente é fumante?', ['', 'Sim', 'Não'], index=0)
Stroke = st.selectbox('Paciente já teve derrame?', ['', 'Sim', 'Não'], index=0)
HeartDiseaseorAttack = st.selectbox(
    'Paciente já teve doença cardíaca ou ataque cardíaco?', ['', 'Sim', 'Não'], index=0)
PhysActivity = st.selectbox('Paciente fez atividade física nos últimos 30 dias?', [
                            '', 'Sim', 'Não'], index=0)
Fruits = st.selectbox('Paciente consome frutas diariamente?', [
                      '', 'Sim', 'Não'], index=0)
Veggies = st.selectbox('Paciente consome vegetais diariamente?', [
                       '', 'Sim', 'Não'], index=0)
HvyAlcoholConsump = st.selectbox('Paciente consome álcool excessivamente?', [
                                 '', 'Sim', 'Não'], index=0)
AnyHealthcare = st.selectbox('Paciente tem acesso a serviços de saúde?', [
                             '', 'Sim', 'Não'], index=0)
NoDocbcCost = st.selectbox('Paciente não consultou um médico por questões financeiras?', [
                           '', 'Sim', 'Não'], index=0)
GenHlth = st.slider(
    'Como o paciente se autoavalia de 1 a 5 com sua saúde em geral? (Sendo 1 excelente e 5 ruim)', 1, 5)
MentHlth = st.number_input(
    'Número de dias nos últimos 30 em que o paciente sentiu que sua saúde mental não estava boa', min_value=0, max_value=30)
PhysHlth = st.number_input(
    'Número de dias nos últimos 30 em que o paciente sentiu que sua saúde física não estava boa', min_value=0, max_value=30)
DiffWalk = st.selectbox('Paciente tem dificuldade para caminhar?', [
                        '', 'Sim', 'Não'], index=0)
Sex = st.selectbox('Qual o sexo do paciente?', [
                   '', 'Masculino', 'Feminino'], index=0)
Age = st.selectbox('Qual a faixa etária do paciente?', [
                   '', '18-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+'], index=0)
Education = st.selectbox('Qual o nível educacional do paciente?', [
                         '', 'Never attended school/kindergarten', 'Elementary incomplete', 'Elementary complete', 'Some high school', 'High school graduate', 'College'], index=0)
Income = st.selectbox('Qual a faixa de renda anual do paciente?', [
                      '', '<10k', '10-15k', '15-20k', '20-25k', '25-35k', '35-50k', '50-75k', '>75k'], index=0)

# Converter as respostas para o formato adequado (Sim/Não para 1/0, sexo para 1/0 e etc.)
input_data = {
    'HighBP': 1 if HighBP == 'Sim' else (None if HighBP == '' else 0),
    'HighChol': 1 if HighChol == 'Sim' else (None if HighChol == '' else 0),
    'CholCheck': 1 if CholCheck == 'Sim' else (None if CholCheck == '' else 0),
    'BMI': BMI,
    'Smoker': 1 if Smoker == 'Sim' else (None if Smoker == '' else 0),
    'Stroke': 1 if Stroke == 'Sim' else (None if Stroke == '' else 0),
    'HeartDiseaseorAttack': 1 if HeartDiseaseorAttack == 'Sim' else (None if HeartDiseaseorAttack == '' else 0),
    'PhysActivity': 1 if PhysActivity == 'Sim' else (None if PhysActivity == '' else 0),
    'Fruits': 1 if Fruits == 'Sim' else (None if Fruits == '' else 0),
    'Veggies': 1 if Veggies == 'Sim' else (None if Veggies == '' else 0),
    'HvyAlcoholConsump': 1 if HvyAlcoholConsump == 'Sim' else (None if HvyAlcoholConsump == '' else 0),
    'AnyHealthcare': 1 if AnyHealthcare == 'Sim' else (None if AnyHealthcare == '' else 0),
    'NoDocbcCost': 1 if NoDocbcCost == 'Sim' else (None if NoDocbcCost == '' else 0),
    'GenHlth': GenHlth,
    'MentHlth': MentHlth,
    'PhysHlth': PhysHlth,
    'DiffWalk': 1 if DiffWalk == 'Sim' else (None if DiffWalk == '' else 0),
    'Sex': 1 if Sex == 'Masculino' else (None if Sex == '' else 0),
    'Age': Age if Age != '' else None,
    'Education': Education if Education != '' else None,
    'Income': Income if Income != '' else None
}

# Verificar se todos os campos obrigatórios foram preenchidos
if all(value is not None for key, value in input_data.items()):
    # Criar um DataFrame a partir dos dados inseridos
    df_input = pd.DataFrame([input_data])

    # Transformar as variáveis categóricas em dummies, como no treinamento
    df_input = pd.get_dummies(
        df_input, columns=['Age', 'Education', 'Income'], drop_first=True)

    # Ajustar para que as colunas correspondam às do modelo treinado
    df_input = df_input.reindex(
        columns=expected_columns, fill_value=0)

    # Fazer a previsão com o pipeline carregado
    if st.button('Prever Diabetes'):
        prediction = pipeline.predict(df_input)[0]

        if prediction == 1:
            st.markdown(
                '<p style="color:red; font-weight:bold; font-size:24px;">Paciente diabético(a)</p>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                '<p style="color:green; font-weight:bold; font-size:24px;">Paciente não  diabético(a)</p>',
                unsafe_allow_html=True)
else:
    st.warning('Por favor, preencha todos os campos antes de fazer a previsão.')
