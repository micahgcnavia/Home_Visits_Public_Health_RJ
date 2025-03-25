# Limpeza, Transformação e Análise de Dados de Visitas Domiciliares de Agentes de Saúde na cidade do Rio de Janeiro

Este repositório foi inicialmente criado para um **desafio para a vaga de Cientista de Dados** da **Diretoria de Inovação e Tecnologia da Prefeitura do Rio**, na área da saúde. No entanto, aproveitei a oportunidade para ir além e implementar análises estatísticas após a limpeza e tratamento dos dados.

O desafio inicial consistia em analisar, estruturar e transformar dados fornecidos em um arquivo que contém diversas entradas dos questionários preenchidos por agentes públicos de saúde durante visitas domiciliares aos pacientes. Os dados fornecem informações cadastrais cruciais para entender o perfil de cada família e são atualizados constantemente ao longo do acompanhamento dos pacientes pela CF/CMS.

## Objetivos 🎯

- Compreender o significado de cada coluna
- Detectar problemas (erros de formatação, valores ausentes, valores incorretos, etc.)
- Resolver os problemas
- Extras: analisar os dados e criar um relatório usando **Microsoft Power BI**

## Estrutura do Projeto 📦

### 1. **`exploring_data.ipynb`**
Esse arquivo é um Jupyter notebook onde realizei a análise exploratória dos dados. Nele, busquei:
- Identificar padrões, tendências e inconsistências nos dados
- Investigar as possíveis causas de erros
- Sugerir soluções para os problemas encontrados

### 2. **`cleaning.py`**
Esse arquivo contém a resolução completa do processo de limpeza e transformação dos dados. Nele, realizei as seguintes etapas:
- Identificação e tratamento de erros nos dados
- Conversão de valores de variáveis para formatos adequados
- Criação de novas colunas, quando necessário
- Estruturação final dos dados para análise

## Como Usar 💻

1. Faça o download ou clone o repositório:
   ```bash
   git clone https://github.com/micahgcnavia/Home_Visits_Public_Health_RJ.git
   ```
2. Use o arquivo `cleaning.py` para obter a tabela limpa e pronta para análise
3. Confira o relatório final baixando o arquivo `dashboard.pbix` ou visite o [site do relatório](https://app.powerbi.com/reportEmbed?reportId=d145b337-32d0-4f60-bd09-98865e847c13&autoAuth=true&ctid=8a425f8e-ceea-4039-8816-b9cb7af9f4cd) (você talvez precisará ter uma conta no Microsoft Power BI para abrir o relatório).

### Citação 📰

Se você sentir vontade de usar esses dados em seus próprios projetos, considere citar este repositório! Obrigado! :)

