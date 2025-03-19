import pandas as pd
import numpy as np
import re
import ast
import uuid
from fractions import Fraction

#=============================================================================================================================================

# Fixing columns with alike errors:

# Columns:

# - obito
# - luz_eletrica
# - em_situacao_de_rua
# - possui_plano_saude
# - vulnerabilidade_social
# - familia_beneficiaria_auxilio_brasil
# - crianca_matriculada_creche_pre_escola

def boolean_to_int(df, col):
    """
    Converts boolean values ​​(True/False) to integers (1/0) in a specific column of the DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the column to apply the conversion

    Returns:
    --------
    df: pandas.DataFrame
        Dataframe converted
    """
    df[col] = df[col].replace({'False': 0, 'True': 1}).astype(int)
    return df

#-------------------------------------------------------------------------------------------------------------------------------------

# Columns:

# - data_cadastro
# - data_nascimento
# - data_atualizacao_cadastro
# - updated_at

def standardize_date(df, col):
    """
    Standardizes a date column in the DataFrame, converting it to Pandas datetime format.

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the column to apply the conversion

    Returns:
    --------
    df: pandas.DataFrame
        Dataframe column converted to datetime
    """
    try:
        df[col] = pd.to_datetime(df[col])
    except:
        df[col] = df[col].apply(lambda x: x if '.' in x else x + '.000')
        df[col] = pd.to_datetime(df[col])
    return df

#-------------------------------------------------------------------------------------------------------------------------------------

# Columns:

# - meios_transporte
# - doencas_condicoes
# - meios_comunicacao
# - em_caso_doenca_procura

def clean_values(value):
    """
    Cleans an individual value or a list of strings, converting lists to comma-separated strings.

    Parameters:
    -----------
    value : str
        Element to be cleaned

    Returns:
    --------
    value: str
        Cleaned string or 'Não informado' (Not informed) when getting null values
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

def clean_column(df, col):
    """
    Cleans a specific column from a DataFrame using the clean_values ​​function.

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the column to clean

    Returns:
    --------
    df: pandas.DataFrame
        Dataframe with cleaned columns
    """
    df[col] = df[col].apply(clean_values)
    return df

#-------------------------------------------------------------------------------------------------------------------------------------

# Columns with specific errors:

# id_paciente

def check_id_format(df, col):
    """
    Checks if the values ​​in the patient ID column are in UUID format.

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the patient ID column

    Returns:
    --------
    True if all IDs are in the correct format, False otherwise.
    """

    id_pattern = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', re.IGNORECASE)
    invalid_ids = df[~df['id_paciente'].astype(str).str.match(id_pattern, na=False)]
    if not invalid_ids.empty:
        print(f"{len(invalid_ids)} invalid values were found in column {col}:")
        print(invalid_ids[[col]].head())
        return False
    else:
        print('No format issues found in patient ID column.')
        return True

def check_id_duplicates(df, col):
    """
    Checks for duplicate values ​​in the patient ID column.

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the patient ID column

    Returns:
    --------
    only_2_entries: list
        List with duplicates
    more_than_2_entries: list
        List with values repeated more than 2 times
    """
    repeated_entries = df.loc[df.duplicated(col, keep=False)]
    repeated_entries = list(repeated_entries[col])

    num_duplicates = {i: len(df.loc[df['id_paciente'] == i]) for i in repeated_entries}

    only_2_entries = [key for key, value in num_duplicates.items() if value == 2]
    more_than_2_entries = [key for key, value in num_duplicates.items() if value > 2]

    if len(only_2_entries) != 0:
        print(f'2 repeated values found in column {col} in {len(only_2_entries)} entry(ies).\n')

    if len(more_than_2_entries) != 0:
        print(f"More than 2 repeated values found in column {col} in {len(more_than_2_entries)} entry(ies).\n")
    else:
        print(f"No duplicates found in column {col}.")
        return False

    return only_2_entries, more_than_2_entries

def generate_patient_id(df, col):
    """
    Generates a unique ID that does not exist in the patient ID column of the DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the patient ID column

    Returns:
    --------
    new_id: str
        A unique ID in UUID format
    """
    while True:
        new_id = str(uuid.uuid4())
        if new_id not in df[col].values:
            return new_id

def fix_duplicates(df, col, ids):
    """
    Fixes duplicate entries in the DataFrame by keeping the most current record or generating new IDs.

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the patient ID column
    ids : list
        List of duplicate IDs
    """
    for id_paciente in ids:
        subset = df[df[col] == id_paciente]
        
        if subset['data_nascimento'].nunique() == 1:
            most_recent_entry = subset.loc[subset['data_atualizacao_cadastro'].idxmax()]
            df.drop(subset.index, inplace=True)
            df = df.append(most_recent_entry)
        else:
            for i in range(1, len(subset)):
                new_id = generate_patient_id(df)
                df.loc[subset.index[i], col] = new_id

#-------------------------------------------------------------------------------------------------------------------------------------

# Columns whose problem is solved with string replacement

def replace_strings(df, col, Input, output):
    """
    Replace inconsistent entries in the DataFrame with correct values.

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the column
    Input : list
        List of unwanted values
    output : list
        List of values to replace
    """

    df[col] = df[col].replace(Input, output)
    return df

# def limpar_identidade_genero(df, col='identidade_genero'):
#     """
#     Limpa a coluna de identidade de gênero, substituindo valores inconsistentes.

#     Parâmetros:
#         df (pd.DataFrame): O DataFrame a ser processado.
#         col (str): O nome da coluna de identidade de gênero.

#     Retorna:
#         pd.DataFrame: O DataFrame com a coluna limpa.
#     """
#     df[col] = df[col].replace('Homossexual (gay / lésbica)', 'Homossexual')
#     df[col] = df[col].replace([np.nan, 'Não', 'Sim'], 'Não informado')
#     return df

# def limpar_orientacao_sexual(df, col='orientacao_sexual'):
#     """
#     Limpa a coluna de orientação sexual, substituindo valores inconsistentes.

#     Parâmetros:
#         df (pd.DataFrame): O DataFrame a ser processado.
#         col (str): O nome da coluna de orientação sexual.

#     Retorna:
#         pd.DataFrame: O DataFrame com a coluna limpa.
#     """
#     df[col] = df[col].replace('Homossexual (gay / lésbica)', 'Homossexual')
#     return df

# def limpar_raca_cor(df, col='raca_cor'):
#     """
#     Limpa a coluna de raça/cor, substituindo valores inconsistentes.

#     Parâmetros:
#         df (pd.DataFrame): O DataFrame a ser processado.
#         col (str): O nome da coluna de raça/cor.

#     Retorna:
#         pd.DataFrame: O DataFrame com a coluna limpa.
#     """
#     df[col] = df[col].replace('Não', 'Não deseja informar')
#     return df

# def limpar_religiao(df, col='religiao'):
#     """
#     Limpa a coluna de religião, substituindo valores inconsistentes.

#     Parâmetros:
#         df (pd.DataFrame): O DataFrame a ser processado.
#         col (str): O nome da coluna de religião.

#     Retorna:
#         pd.DataFrame: O DataFrame com a coluna limpa.
#     """
#     random_entries = ['Acomp. Cresc. e Desenv. da Criança', 'ORQUIDEA', 'ESB ALMIRANTE', '10 EAP 01']
#     df[col] = df[col].replace(random_entries, 'Sem informação')
#     df[col] = df[col].replace('Não', 'Sem religião')
#     df[col] = df[col].replace('Sim', 'Outra')
#     return df

# def limpar_escolaridade(df, col='escolaridade'):
#     """
#     Limpa a coluna de escolaridade, substituindo valores inconsistentes.

#     Parâmetros:
#         df (pd.DataFrame): O DataFrame a ser processado.
#         col (str): O nome da coluna de escolaridade.

#     Retorna:
#         pd.DataFrame: O DataFrame com a coluna limpa.
#     """
#     df[col] = df[col].replace('Não sabe ler/escrever', 'Iletrado')
#     df[col] = df[col].replace('Especialização/Residência', 'Especialização ou Residência')
#     return df

# def limpar_situacao_profissional(df, col='situacao_profissional'):
#     """
#     Limpa a coluna de situação profissional, substituindo valores inconsistentes.

#     Parâmetros:
#         df (pd.DataFrame): O DataFrame a ser processado.
#         col (str): O nome da coluna de situação profissional.

#     Retorna:
#         pd.DataFrame: O DataFrame com a coluna limpa.
#     """
#     df[col] = df[col].replace('SMS CAPS DIRCINHA E LINDA BATISTA AP 33', 'Não informado')
#     df[col] = df[col].replace('Pensionista / Aposentado', 'Pensionista ou Aposentado')
#     df[col] = df[col].replace(['Não se aplica', 'Não trabalha'], 'Desempregado')
#     df[col] = df[col].replace('Médico Urologista', 'Emprego Formal')
#     return df

# def limpar_renda_familiar(df, col='renda_familiar'):
#     """
#     Limpa a coluna de renda familiar, substituindo valores inconsistentes.

#     Parâmetros:
#         df (pd.DataFrame): O DataFrame a ser processado.
#         col (str): O nome da coluna de renda familiar.

#     Retorna:
#         pd.DataFrame: O DataFrame com a coluna limpa.
#     """
#     df[col] = df[col].replace(['Manhã', 'Internet'], 'Não informado')
#     return df

#-------------------------------------------------------------------------------------------------------------------------------------

def extract_category(text):
    """
    Extracts information between parentheses from a text.

    Parameters:
    -----------
    text : str
        Text to be evaluated

    Returns:
    --------
    Extracted text or None
    """
    match = re.search(r'\((.*?)\)', text)
    return match.group(1) if match else None

def remove_category(text):
    """
    Removes text between parentheses from a text.

    Parameters:
    -----------
    text : str
        Text to be evaluated

    Returns:
    --------
    Text with no parentheses
    """
    return re.sub(r'\(.*?\)', '', text).strip()

def create_category_col(df, col, new_col):
    """
    Creates a new column with the category extracted and clears the original column.

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the original column
    new_col : str
        Name of the new column

    Returns:
    --------
    df : pandas.DataFrame
    """
    df[new_col] = df[col].apply(extract_category)
    df[col] = df[col].apply(remove_category)
    return df

def create_social_security_col(df, col='previdencia_social'):
    """
    Creates a new column indicating whether the patient has social security based on employment status.

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the new column

    Returns:
    --------
    df : pandas.DataFrame
    """

    rules = {
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
    
    df[col] = df['situacao_profissional'].map(rules)
    return df

#-------------------------------------------------------------------------------------------------------------------------------------

def family_income_to_float(value):
    """
    Converts family income string into float

    Parameters:
    -----------
    value : str
        Value to be converted

    Returns:
    --------
    Converted value as float, '+4' or None
    """
    if 'Mais de 4' in value: # More than 4
        return '+4'
    
    match = re.search(r'(\d+\/\d+|\d+)', value)
    if match:
        num = match.group(1)
        if '/' in num:
            return float(Fraction(num))
        else:
            return float(num)
    return None

def transform_family_income(df, col='renda_familiar'):
    """
    Transform family income column in numeric type

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the family income column

    Returns:
    --------
    df : pandas.DataFrame
    """
    df[col] = df[col].apply(family_income_to_float)
    return df

#-------------------------------------------------------------------------------------------------------------------------------------

# Quantitative columns:

def calculate_IQR_lims(df, col, factor=1.5):
    """
    Calculate the lower and upper limits for identifying outliers using the Interquartile Range (IQR) method.

    Parameters:
    -----------
    data : pandas.DataFrame
        The dataset containing the column for which the IQR limits are to be calculated.
    col : str
        The name of the column in the dataset to calculate the IQR limits for.
    factor : float, optional (default=1.5)
        The multiplier for the IQR to determine the lower and upper limits. A common choice is 1.5, 
        but it can be adjusted based on the desired sensitivity for outlier detection.

    Returns:
    --------
    lower_lim : float
        The lower limit for identifying outliers. Values below this limit are considered outliers.
    upper_lim : float
        The upper limit for identifying outliers. Values above this limit are considered outliers.

    Notes:
    ------
    The IQR method identifies outliers by calculating the range between the first quartile (Q1) 
    and the third quartile (Q3). Outliers are typically defined as values that fall below 
    `Q1 - factor * IQR` or above `Q3 + factor * IQR`.
    """
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
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

    colunas_boolean_to_int = [
    'obito',
    'luz_eletrica',
    'em_situacao_de_rua',
    'possui_plano_saude',
    'vulnerabilidade_social',
    'familia_beneficiaria_auxilio_brasil',
    'crianca_matriculada_creche_pre_escola'
    ]

    # Aplicando a função boolean_to_int para cada coluna
    for coluna in colunas_boolean_to_int:
        data = boolean_to_int(data, coluna)

    # Limpando colunas com erros de strings:

    colunas_erros_string = ['meios_transporte', 'doencas_condicoes', 'meios_comunicacao', 'em_caso_doenca_procura']

    # Aplicando a função clean_column para cada coluna
    for coluna in colunas_erros_string:
        data = clean_column(data, coluna)

    # Limpando colunas de data:

    colunas_data = ['data_cadastro', 'data_nascimento', 'data_atualizacao_cadastro', 'updated_at']

    # Aplicando a função standardize_date para cada coluna
    for coluna in colunas_data:
        data = standardize_date(data, coluna)

    # Limpando colunas específicas:
    check_id_format(data, 'id_paciente')
    duas, mais_que_duas = check_id_duplicates(data, 'id_paciente')
    print('Corrigindo duplicatas...')
    fix_duplicates(data, duas)
    fix_duplicates(data, mais_que_duas)
    check_id_duplicates(data, 'id_paciente')

    # Lista de funções a serem aplicadas
    funcoes = [
        limpar_raca_cor,
        limpar_identidade_genero,
        limpar_orientacao_sexual,
        limpar_escolaridade,
        limpar_religiao,
        (create_category_col, 'ocupacao', 'categoria_ocupacao'),
        limpar_renda_familiar,
        transform_family_income,
        limpar_situacao_profissional,
        create_social_security_col
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