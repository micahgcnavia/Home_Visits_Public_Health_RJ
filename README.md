# Análise e Limpeza de Dados de Questionário de Visitas Domiciliares no Rio de Janeiro

Este projeto tem como objetivo analisar, estruturar e transformar dados fornecidos em um arquivo que contém um questionário preenchido por agentes de saúde durante visitas domiciliares aos pacientes. Os dados fornecem informações cadastrais cruciais para entender o perfil de cada família e são atualizados constantemente ao longo do acompanhamento dos pacientes pela CF/CMS.

Este repositório foi desenvolvido para o **desafio para a vaga de Cientista de Dados** da **Diretoria de Inovação e Tecnologia da Prefeitura do Rio**, na área da saúde.

## Objetivo 🎯

O objetivo deste projeto é processar esses dados brutos (raw), identificar e corrigir erros, e transformar o conjunto de dados em um formato mais adequado para análise. A ideia original é usar `dbt` para levar as queries do `Python` para `SQL`, utilizando algum banco de dados como nuvem. No entanto, essa etapa ainda está em andamento. Por outro lado, toda a análise e limpeza já foram feitas inteiramente em `Python`.

## Estrutura do Projeto 📦

### 1. **`cleaning.py`**
Esse arquivo contém a resolução completa do processo de limpeza e transformação dos dados. Nele, realizamos as seguintes etapas:
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
