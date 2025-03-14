# Limpeza, Transformação e Análise de Dados de Visitas Domiciliares de Agentes de Saúde na cidade do Rio de Janeiro

Este repositório foi inicialmente criado para um **desafio para a vaga de Cientista de Dados** da **Diretoria de Inovação e Tecnologia da Prefeitura do Rio**, na área da saúde. No entanto, aproveitei a oportunidade para ir além e implementar análises estatísticas após a limpeza e tratamento dos dados.

O desafio inicial consistia em analisar, estruturar e transformar dados fornecidos em um arquivo que contém diversas entradas dos questionários preenchidos por agentes de saúde durante visitas domiciliares aos pacientes. Os dados fornecem informações cadastrais cruciais para entender o perfil de cada família e são atualizados constantemente ao longo do acompanhamento dos pacientes pela CF/CMS.

## Objetivos 🎯

- Compreender o significado de cada coluna
- Detectar problemas (erros de formatação, valores ausentes, valores incorretos, etc.)
- Resolver os problemas
- Extras: analisar os dados e criar um relatório usando **Microsoft Power BI**

## Estrutura do Projeto 📦

### 1. **`cleaning.py`**
Esse arquivo contém a resolução completa do processo de limpeza e transformação dos dados. Nele, realizei as seguintes etapas:
- Identificação e tratamento de erros nos dados
- Conversão de valores de variáveis para formatos adequados
- Criação de novas variáveis, quando necessário
- Estruturação final dos dados para análise

### 2. **`exploring_data.ipynb`**
Esse arquivo é um Jupyter notebook onde realizei a análise exploratória dos dados. Nele, busquei:
- Identificar padrões, tendências e inconsistências nos dados
- Investigar as possíveis causas de erros
- Sugerir soluções para os problemas encontrados

## Como Usar 💻

1. Faça o download ou clone o repositório:
   ```bash
   git clone https://github.com/micahgcnavia/DIT-Test.git
   ```

2. Baixe o arquivo `dados_ficha_a_desafio.csv` através do [link do Google Drive](https://drive.google.com/file/d/1dWC1ZUPNlCQBalYPY8uP4Zzs0aue9nkQ/view?usp=sharing)

3. Mude ```file_path``` nos arquivos .py e .ipynb para o caminho correspondente ao arquivo na sua máquina
