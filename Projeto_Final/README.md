# Projeto Final - Classificação de Pacientes com Diabetes

[streamlit.webm](https://github.com/user-attachments/assets/cb35672e-b0cf-460c-a921-16bf6ec2690c)

[Visualização online do deploy](https://ebac-data-science-proejto-final.streamlit.app)

O objetivo deste modelo de machine learning é, a partir de algumas informações dos pacientes, consegui classificar se eles são ou não diabéticos, baseando-se em uma série de dados de saúde e estilo de vida. Para o desenvolvimento deste projeto, utilizaremos a base de dados [Diabetes Health Indicators Dataset](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset/data?select=diabetes_012_health_indicators_BRFSS2015.csv), que contém 253.680 respostas a uma pesquisa conduzida em 2015 pelo CDC (Centers for Disease Control and Prevention) dos Estados Unidos. O objetivo dessa pesquisa foi coletar informações sobre indicadores de saúde relacionados ao diabetes. A base de dados faz parte do Behavioral Risk Factor Surveillance System (BRFSS), um sistema de vigilância de fatores de risco à saúde.

Link para acessar a base de dados: https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset/data?select=diabetes_012_health_indicators_BRFSS2015.csv

## Conteúdo

- `Projeto_Final.ipynb`: Este Notebook Jupyter contém o código do projeto de Classificação de Pacientes com Diabetes. Ele inclui análises exploratórias de dados, desenvolvimento e treinamento de modelos de machine learning, visualizações de dados e outras análises relacionadas ao projeto.
- ``app.py``: Este arquivo contém o código para criar o aplicativo Streamlit com o deploy do projeto.
- `model.pkl`: Pipeline do modelo LightGBM treinado gerado pelo `Projeto_Final.ipynb`.
- `logs.log`: Arquivo de log com registros das etapas de execução do pipeline.
- `data`: Pasta contém a base de dados utilizada na análise.
- `outputs`: Pasta contém os arquivos que são gerados como saída durante a execução do notebook Jupyter do projeto. Isso pode incluir gráficos, imagens, e arquivos html ou qualquer outra saída produzida durante a análise de dados.
- `requirements.txt`: Arquivo de texto contendo todas as bibliotecas que o projeto necessita para funcionar corretamente.
- `visualizacao_deploy.webm`: Este vídeo apresenta o deploy criado com o aplicativo Streamlit.
- `icon.png`: Arquivo de imagem usado para ser o icone da página do deploy.

Este repositório foi criado como parte do projeto final do curso de Ciência de Dados da Escola Britânica de Artes Criativas e Tecnologia (EBAC), com o objetivo de consolidar o aprendizado e fornecer um recurso para referência futura.

## Como rodar o projeto

  1. Clone este repositório:
  
     ```bash
     git clone https://github.com/seu-usuario/EBAC-Data-Science.git
     streamlit run app.py
     ```
  2. Instale as dependências:
     ```bash
     pip install -r requirements.txt
     ```
  3. Execute o aplicativo:
     ```bash
     streamlit run app.py
     ```
    
## Referências

Para mais informações sobre como utilizar as ferramentas e técnicas abordadas neste módulo, consulte a documentação oficial das seguintes bibliotecas:

- [Pandas](https://pandas.pydata.org/docs/)
- [Warnings](https://docs.python.org/3/library/warnings.html)
- [Scikit-learn](https://scikit-learn.org/stable/)
- [Pycaret](https://pycaret.gitbook.io/docs)
- [Streamlit](https://docs.streamlit.io/)
- [os](https://docs.python.org/3/library/os.html)
- [NumPy](https://numpy.org/doc/stable/)
- [Seaborn](https://seaborn.pydata.org/)
- [Matplotlib](https://matplotlib.org/stable/contents.html)
- [LightGBM](https://lightgbm.readthedocs.io/en/latest/)
- [ydata_profiling](https://ydata-profiling.ydata.ai/docs/master/index.html)
- [Joblib](https://joblib.readthedocs.io/en/stable/)
- [Imbalanced-learn (imblearn)](https://imbalanced-learn.org/stable/)
- [BorutaPy](https://github.com/scikit-learn-contrib/boruta_py)
