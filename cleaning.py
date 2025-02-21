import pandas as pd
import numpy as np
import re
import ast
import uuid
from fractions import Fraction

#=============================================================================================================================================

# Corrigindo colunas com erros parecidos:

# Colunas:

# - obito
# - luz_eletrica
# - em_situacao_de_rua
# - possui_plano_saude
# - vulnerabilidade_social
# - familia_beneficiaria_auxilio_brasil
# - crianca_matriculada_creche_pre_escola

def boolean_para_int(df, col):
    """
    Converte valores booleanos (True/False) em inteiros (1/0) em uma coluna específica do DataFrame.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna a ser convertida.

    Retorna:
        pd.DataFrame: O DataFrame com a coluna convertida.
    """
    df[col] = df[col].replace({'False': 0, 'True': 1}).astype(int)
    return df

#-------------------------------------------------------------------------------------------------------------------------------------

# Colunas:

# - data_cadastro
# - data_nascimento
# - data_atualizacao_cadastro
# - updated_at

def padronizar_data(df, col):
    """
    Padroniza uma coluna de datas no DataFrame, convertendo para o formato datetime.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna de datas.

    Retorna:
        pd.DataFrame: O DataFrame com a coluna de datas padronizada.
    """
    try:
        df[col] = pd.to_datetime(df[col])
    except:
        df[col] = df[col].apply(lambda x: x if '.' in x else x + '.000')
        df[col] = pd.to_datetime(df[col])
    return df

#-------------------------------------------------------------------------------------------------------------------------------------

# Colunas:

# - meios_transporte
# - doencas_condicoes
# - meios_comunicacao
# - em_caso_doenca_procura

def limpar_valores(value):
    """
    Limpa um valor individual ou uma lista de strings, convertendo listas em strings separadas por vírgulas.

    Parâmetros:
        value (str ou list): O valor a ser processado.

    Retorna:
        str: O valor limpo.
    """
    try:
        if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
            value = ast.literal_eval(value)
        
        if isinstance(value, list):
            value = ", ".join(value)
        
        if value in ([], ""):
            value = "Não informado"
        
        return value
    except Exception:
        return "Não informado"

def limpar_coluna(df, col):
    """
    Limpa uma coluna específica de um DataFrame usando a função limpar_valores.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna a ser limpa.

    Retorna:
        pd.DataFrame: O DataFrame com a coluna especificada limpa.
    """
    df[col] = df[col].apply(limpar_valores)
    return df

#-------------------------------------------------------------------------------------------------------------------------------------

# Colunas com erros específicos:

# id_paciente

def checar_formato_id(df, col):
    """
    Verifica se os valores na coluna de ID do paciente estão no formato UUID.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna de ID.

    Retorna:
        bool: True se todos os IDs estiverem no formato correto, False caso contrário.
    """
    id_pattern = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', re.IGNORECASE)
    invalid_ids = df[~df['id_paciente'].astype(str).str.match(id_pattern, na=False)]
    if not invalid_ids.empty:
        print(f"Foram encontrados {len(invalid_ids)} valores inválidos na coluna {col}:")
        print(invalid_ids[[col]].head())
    else:
        print('Nenhum problema de formato encontrado na coluna id_paciente.')
        return True

def checar_duplicatas(df, col):
    """
    Verifica se há valores duplicados em uma coluna específica do DataFrame.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna a ser verificada.

    Retorna:
        tuple: Uma tupla contendo listas de IDs duplicados e IDs com mais de duas ocorrências.
    """
    repeated_entries = df.loc[df.duplicated(col, keep=False)]
    repeated_entries = list(repeated_entries[col])

    num_duplicates = {i: len(df.loc[df['id_paciente'] == i]) for i in repeated_entries}

    only_2_entries = [key for key, value in num_duplicates.items() if value == 2]
    more_than_2_entries = [key for key, value in num_duplicates.items() if value > 2]

    if len(only_2_entries) != 0:
        print(f'Encontrados 2 valores repetidos para um mesmo id na coluna {col} em {len(only_2_entries)} entrada(s).\n')

    if len(more_than_2_entries) != 0:
        print(f"Mais de 2 valores repetidos encontrados para um mesmo id na coluna {col} em {len(more_than_2_entries)} entrada(s).\n")
    else:
        print(f"Nenhuma duplicata encontrada para a coluna {col}")
        return False

    return only_2_entries, more_than_2_entries

def gerar_id_unico(df):
    """
    Gera um ID único que não existe na coluna 'id_paciente' do DataFrame.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.

    Retorna:
        str: Um ID único no formato UUID.
    """
    while True:
        novo_id = str(uuid.uuid4())
        if novo_id not in df['id_paciente'].values:
            return novo_id

def corrigir_duplicatas(df, ids):
    """
    Corrige entradas duplicadas no DataFrame, mantendo o registro mais atual ou gerando novos IDs.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        ids (list): Lista de IDs duplicados.
    """
    for id_paciente in ids:
        subset = df[df['id_paciente'] == id_paciente]
        
        if subset['data_nascimento'].nunique() == 1:
            registro_mais_atual = subset.loc[subset['data_atualizacao_cadastro'].idxmax()]
            df.drop(subset.index, inplace=True)
            df = df.append(registro_mais_atual)
        else:
            for i in range(1, len(subset)):
                novo_id = gerar_id_unico(df)
                df.loc[subset.index[i], 'id_paciente'] = novo_id

#-------------------------------------------------------------------------------------------------------------------------------------

# Colunas cujo problema é resolvido com substituição de string 

def limpar_identidade_genero(df, col='identidade_genero'):
    """
    Limpa a coluna de identidade de gênero, substituindo valores inconsistentes.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna de identidade de gênero.

    Retorna:
        pd.DataFrame: O DataFrame com a coluna limpa.
    """
    df[col] = df[col].replace('Homossexual (gay / lésbica)', 'Homossexual')
    df[col] = df[col].replace([np.nan, 'Não', 'Sim'], 'Não informado')
    return df

def limpar_orientacao_sexual(df, col='orientacao_sexual'):
    """
    Limpa a coluna de orientação sexual, substituindo valores inconsistentes.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna de orientação sexual.

    Retorna:
        pd.DataFrame: O DataFrame com a coluna limpa.
    """
    df[col] = df[col].replace('Homossexual (gay / lésbica)', 'Homossexual')
    return df

def limpar_raca_cor(df, col='raca_cor'):
    """
    Limpa a coluna de raça/cor, substituindo valores inconsistentes.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna de raça/cor.

    Retorna:
        pd.DataFrame: O DataFrame com a coluna limpa.
    """
    df[col] = df[col].replace('Não', 'Não deseja informar')
    return df

def limpar_religiao(df, col='religiao'):
    """
    Limpa a coluna de religião, substituindo valores inconsistentes.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna de religião.

    Retorna:
        pd.DataFrame: O DataFrame com a coluna limpa.
    """
    random_entries = ['Acomp. Cresc. e Desenv. da Criança', 'ORQUIDEA', 'ESB ALMIRANTE', '10 EAP 01']
    df[col] = df[col].replace(random_entries, 'Sem informação')
    df[col] = df[col].replace('Não', 'Sem religião')
    df[col] = df[col].replace('Sim', 'Outra')
    return df

def limpar_escolaridade(df, col='escolaridade'):
    """
    Limpa a coluna de escolaridade, substituindo valores inconsistentes.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna de escolaridade.

    Retorna:
        pd.DataFrame: O DataFrame com a coluna limpa.
    """
    df[col] = df[col].replace('Não sabe ler/escrever', 'Iletrado')
    df[col] = df[col].replace('Especialização/Residência', 'Especialização ou Residência')
    return df

def limpar_situacao_profissional(df, col='situacao_profissional'):
    """
    Limpa a coluna de situação profissional, substituindo valores inconsistentes.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna de situação profissional.

    Retorna:
        pd.DataFrame: O DataFrame com a coluna limpa.
    """
    df[col] = df[col].replace('SMS CAPS DIRCINHA E LINDA BATISTA AP 33', 'Não informado')
    df[col] = df[col].replace('Pensionista / Aposentado', 'Pensionista ou Aposentado')
    df[col] = df[col].replace(['Não se aplica', 'Não trabalha'], 'Desempregado')
    df[col] = df[col].replace('Médico Urologista', 'Emprego Formal')
    return df

def limpar_renda_familiar(df, col='renda_familiar'):
    """
    Limpa a coluna de renda familiar, substituindo valores inconsistentes.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna de renda familiar.

    Retorna:
        pd.DataFrame: O DataFrame com a coluna limpa.
    """
    df[col] = df[col].replace(['Manhã', 'Internet'], 'Não informado')
    return df

#-------------------------------------------------------------------------------------------------------------------------------------

def extrair_categoria(text):
    """
    Extrai a informação entre parênteses de um texto.

    Parâmetros:
        text (str): O texto a ser processado.

    Retorna:
        str: O texto extraído ou None.
    """
    match = re.search(r'\((.*?)\)', text)
    return match.group(1) if match else None

def remover_categoria(text):
    """
    Remove o texto entre parênteses de um texto.

    Parâmetros:
        text (str): O texto a ser processado.

    Retorna:
        str: O texto sem a parte entre parênteses.
    """
    return re.sub(r'\(.*?\)', '', text).strip()

def criar_col_categoria(df, col, new_col):
    """
    Cria uma nova coluna com a categoria extraída da coluna original e limpa a coluna original.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna original.
        new_col (str): O nome da nova coluna.

    Retorna:
        pd.DataFrame: O DataFrame com a nova coluna e a coluna original limpa.
    """
    df[new_col] = df[col].apply(extrair_categoria)
    df[col] = df[col].apply(remover_categoria)
    return df

def criar_col_previdencia_social(df, col='previdencia_social'):
    """
    Cria uma nova coluna indicando se o paciente tem previdência social com base na situação profissional.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da nova coluna.

    Retorna:
        pd.DataFrame: O DataFrame com a nova coluna.
    """

    regras = {
        'Emprego Formal': 1,
        'Autônomo com previdência social': 1,
        'Pensionista ou Aposentado': 1,
        'Desempregado': 0,
        'Outro': 0,
        'Autônomo': 0,
        'Emprego Informal': 0,
        'Autônomo sem previdência social': 0,
        'Empregador': 0,
        'Não informado': 0}
    
    df[col] = df['situacao_profissional'].map(regras)
    return df

#-------------------------------------------------------------------------------------------------------------------------------------

def value_to_float(value):
    """
    Converte um valor de renda familiar em um número float.

    Parâmetros:
        value (str): O valor a ser convertido.

    Retorna:
        float: O valor convertido ou None.
    """
    if 'Mais de 4' in value:
        return '+4'
    
    match = re.search(r'(\d+\/\d+|\d+)', value)
    if match:
        num = match.group(1)
        if '/' in num:
            return float(Fraction(num))
        else:
            return float(num)
    return None

def transform_renda_familiar(df, col='renda_familiar'):
    """
    Transforma a coluna de renda familiar em valores numéricos.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna de renda familiar.

    Retorna:
        pd.DataFrame: O DataFrame com a coluna transformada.
    """
    df[col] = df[col].apply(value_to_float)
    return df

#-------------------------------------------------------------------------------------------------------------------------------------

# Colunas quantitativas:

def calculate_IQR_lims(data, col, factor=1.5):
    """
    Calcula os limites inferior e superior para identificar outliers com base no intervalo interquartil (IQR).

    Parâmetros:
        data (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna numérica.
        factor (float): O fator multiplicativo para o IQR.

    Retorna:
        list: Uma lista contendo o limite inferior e superior.
    """
    Q1 = data[col].quantile(0.25)
    Q3 = data[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_lim = Q1 - factor * IQR
    upper_lim = Q3 + factor * IQR
    return [lower_lim, upper_lim]

def identificar_outliers(df, col, limite_inferior, limite_superior):
    """
    Identifica outliers em uma coluna numérica com base em limites inferior e superior.

    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser processado.
        col (str): O nome da coluna numérica.
        limite_inferior (float): O limite inferior do intervalo válido.
        limite_superior (float): O limite superior do intervalo válido.

    Retorna:
        pd.DataFrame: O DataFrame com uma nova coluna indicando se o valor é um outlier (0 ou 1).
    """
    df[col + '_outlier_flag'] = ~df[col].between(limite_inferior, limite_superior)
    df[col + '_outlier_flag'] = df[col + '_outlier_flag'].astype(int)
    return df

#========================================================================================================================================

def main():
    """
    Função principal que executa a limpeza e transformação dos dados.
    """
    file_path = '/home/micah/dados_ficha_a_desafio.csv' # alterar para o caminho adequado da sua máquina.
    data = pd.read_csv(file_path)

    # Limpando colunas qualitativas:
    lims_altura = calculate_IQR_lims(data, 'altura')
    lims_altura[0] = 40 # assumindo crianças recém nascidas
    lims_peso = calculate_IQR_lims(data, 'peso')
    lims_pressao_diastolica = calculate_IQR_lims(data, 'pressao_diastolica')
    lims_pressao_sistolica = calculate_IQR_lims(data, 'pressao_sistolica')

    data = identificar_outliers(data, 'altura', lims_altura[0], lims_altura[1])
    data = identificar_outliers(data, 'peso', lims_peso[0], lims_peso[1])
    data = identificar_outliers(data, 'pressao_diastolica', lims_pressao_diastolica[0], lims_pressao_diastolica[1])
    data = identificar_outliers(data, 'pressao_sistolica', lims_pressao_sistolica[0], lims_pressao_sistolica[1])

    # Limpando colunas com erros de True e False:

    colunas_boolean_para_int = [
    'obito',
    'luz_eletrica',
    'em_situacao_de_rua',
    'possui_plano_saude',
    'vulnerabilidade_social',
    'familia_beneficiaria_auxilio_brasil',
    'crianca_matriculada_creche_pre_escola'
    ]

    # Aplicando a função boolean_para_int para cada coluna
    for coluna in colunas_boolean_para_int:
        data = boolean_para_int(data, coluna)

    # Limpando colunas com erros de strings:

    colunas_erros_string = ['meios_transporte', 'doencas_condicoes', 'meios_comunicacao', 'em_caso_doenca_procura']

    # Aplicando a função limpar_coluna para cada coluna
    for coluna in colunas_erros_string:
        data = limpar_coluna(data, coluna)

    # Limpando colunas de data:

    colunas_data = ['data_cadastro', 'data_nascimento', 'data_atualizacao_cadastro', 'updated_at']

    # Aplicando a função padronizar_data para cada coluna
    for coluna in colunas_data:
        data = padronizar_data(data, coluna)

    # Limpando colunas específicas:
    checar_formato_id(data, 'id_paciente')
    duas, mais_que_duas = checar_duplicatas(data, 'id_paciente')
    print('Corrigindo duplicatas...')
    corrigir_duplicatas(data, duas)
    corrigir_duplicatas(data, mais_que_duas)
    checar_duplicatas(data, 'id_paciente')

    # Lista de funções a serem aplicadas
    funcoes = [
        limpar_raca_cor,
        limpar_identidade_genero,
        limpar_orientacao_sexual,
        limpar_escolaridade,
        limpar_religiao,
        (criar_col_categoria, 'ocupacao', 'categoria_ocupacao'),
        limpar_renda_familiar,
        transform_renda_familiar,
        limpar_situacao_profissional,
        criar_col_previdencia_social
    ]

    # Iterando sobre as funções e aplicando no dataframe
    for func in funcoes:
        if isinstance(func, tuple):
            # Função que precisa de parâmetros adicionais
            data = func[0](data, *func[1:])
        else:
            # Função sem parâmetros adicionais
            data = func(data)

    data.to_csv('tabela_limpa.csv', index=False)

if __name__ == "__main__":
    main()