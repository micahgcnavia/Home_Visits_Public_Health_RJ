# Análise e Limpeza de Dados de Questionário de Visitas Domiciliares no Rio de Janeiro

Este repositório foi desenvolvido para o **desafio para a vaga de Cientista de Dados** da **Diretoria de Inovação e Tecnologia da Prefeitura do Rio**, na área da saúde.

O desafio desse projeto consiste em analisar, estruturar e transformar dados fornecidos em um arquivo que contém diversas entradas dos questionários preenchidos por agentes de saúde durante visitas domiciliares aos pacientes. Os dados fornecem informações cadastrais cruciais para entender o perfil de cada família e são atualizados constantemente ao longo do acompanhamento dos pacientes pela CF/CMS. Para uma introdução aos dados, consultar o arquivo ```descricao_de_campos.xlsx```. O sumário do que se espera para o projeto se encontra no arquivo ```Desafio Vaga de Cientista de Dados.docx```.

## Objetivo 🎯

O objetivo deste projeto é detectar problemas em cada coluna da tabela fornecida, ponderar sobre a causa do problema e resolvê-los usando ```Python``` e, posteriormente, ```dbt```.

## Estrutura do Projeto 📦

### 1. **`cleaning.py`**
Esse arquivo contém a resolução completa do processo de limpeza e transformação dos dados. Nele, realizei as seguintes etapas:
- Identificação e tratamento de erros nos dados
- Conversão de valores de variáveis para formatos adequados
- Criação de novas variáveis, quando necessário
- Estruturação final dos dados para análise

### 2. **`exploring_data.ipynb`**
Esse arquivo é um notebook Jupyter onde realizei a análise exploratória dos dados. Nele, busquei:
- Identificar padrões, tendências e inconsistências nos dados
- Investigar as possíveis causas de erros
- Sugerir soluções para os problemas encontrados

## Como Usar 💻

1. Faça o download ou clone o repositório:
   ```bash
   git clone https://github.com/micahgcnavia/DIT-Test.git
   ```

2. Baixe o arquivo `dados_ficha_a_desafio.csv` através do [link do Google Drive](https://drive.google.com/file/d/1dWC1ZUPNlCQBalYPY8uP4Zzs0aue9nkQ/view?usp=sharing)

3. Mude ```file_path``` nos arquivos .py e .ipynb para o caminho correspondente ao arquivo na sua máquina.

4. ```dbt```: em construção 🛠️.
