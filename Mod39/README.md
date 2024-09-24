# Projeto-Final-SQL

Este repositório é a entrega do projeto final deste módulo de SQL. O foco deste projeto de SQL é manusear dados desde a obtenção, resgate no bucket, execução de queries e toda a parte de análise descritiva. Além do SQL, em algumas partes do projeto, utilizaremos Python para gerar gráficos que melhoram nossa percepção e nos ajudam a criar insights. Estamos utilizando uma base de dados fictícia de uma instituição bancária, e o principal objetivo deste trabalho é gerar insights quanto a melhorias de serviços, processos e estratégias para a empresa.

Para utilizarmos SQL, empregamos o AWS Athena juntamente com o S3 Bucket, com uma versão reduzida dos dados disponibilizados em: [GitHub](https://github.com/andre-marcos-perez/ebac-course-utils/tree/main/dataset).

As principais habilidades que aprendemos no módulo incluem:
- Compreender o que é uma base de dados e como os dados são organizados em softwares de bancos de dados;
- Utilizar a linguagem de programação SQL para manipular dados em bases de dados;
- Entender os termos fundamentais de armazenamento de dados físicos e lógicos;
- Distinguir entre armazenamento de dados físico e lógico para explicar como os dados são armazenados fisicamente nos computadores;
- Entender a estrutura de um sistema de gerenciamento de banco de dados e sua função no armazenamento e recuperação de dados;
- Compreender os fundamentos e aprender a sintaxe básica do SQL;
- Praticar a criação de consultas SQL;
- Compreender a interface do AWS Console;
- Compreender os termos básicos do armazenamento de objetos em nuvem com AWS S3, além de criar, configurar e gerenciar buckets do S3 para armazenar dados;
- Conhecer as principais funcionalidades e recursos do S3 para gerenciamento, segurança e acesso aos dados armazenados;
- Compreender o AWS Athena e como ele se encaixa no ecossistema da AWS;
- Criar tabelas e consultas para explorar e analisar dados armazenados no Amazon S3;
- Utilizar recursos avançados do AWS Athena, como funções, expressões e partições;
- Compreender a importância das restrições de dados para manter a integridade dos dados;
- Compreender a importância dos filtros na seleção de dados em SQL;
- Identificar os diferentes caracteres coringa (wildcards) disponíveis em SQL;
- Compreender o uso da estrutura CASE/WHEN/THEN para realizar seleções condicionais em SQL;
- Aplicar a função COUNT juntamente com a cláusula GROUP BY para obter informações agregadas em uma tabela;
- Entender como as funções MIN, MAX, SUM e AVG podem ser usadas em conjunto com a cláusula GROUP BY para obter informações agregadas por grupos em uma tabela;
- Compreender o que é a cláusula HAVING e como ela se difere da cláusula WHERE em SQL;
- Compreender o que é a operação UNION e quando ela pode ser utilizada;
- Utilizar a junção INNER para combinar dados de duas ou mais tabelas;
- Compreender o que é uma junção CROSS e quando ela deve ser utilizada;
- Compreender o que são as junções LEFT e RIGHT e quando elas devem ser utilizadas;
- Identificar as diferentes formas de utilização de subqueries em SQL;
- Aplicar subqueries em SQL para filtrar e manipular dados de uma tabela;
- Compreender a definição de agregação por particionamento em SQL;
- Criar visões em SQL para simplificar consultas complexas.

## Conteúdo

- `Projeto Final - SQL.ipynb`: Este notebook Jupyter contém o código da análise de dados de crédito. Ele inclui análises exploratórias de dados, visualizações de dados e outras análises relacionadas ao projeto.
- `Gráficos`: Pasta que contém os arquivos dos gráficos gerados como saída durante a execução do notebook Jupyter do projeto.
- `Queries`: Esta pasta contém capturas de imagem dos resultados das queries feitas no AWS Athena.
- `credit_base.csv`: Este arquivo CSV é a base de dados usada para a análise.

Este repositório foi criado como parte do projeto final do módulo de SQL para análise de dados da Ebac, com o objetivo de consolidar o aprendizado e fornecer um recurso para referência futura.

## Referências

Para mais informações sobre como utilizar as ferramentas e técnicas abordadas neste módulo, consulte a documentação oficial das seguintes bibliotecas:

- [Pandas](https://pandas.pydata.org/docs/)
- [Seaborn](https://seaborn.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
