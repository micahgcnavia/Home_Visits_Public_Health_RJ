import pandas as pd
import numpy as np
import re
import ast
import uuid
from fractions import Fraction
from datetime import datetime

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

def standardize_date(df, col): # add flag for invalid entries
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

def date_flag(df, col):
    """
    Creates a flag column to indicate whether the date entry is incorrect

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the date column (already in datetime)
    new_col : str
        Name of the date flag column

    Returns:
    --------
    df: pandas.DataFrame
    """
    current_year = datetime.now().year
    min_year = current_year - 120 # oldest person, maybe?

    df[col+'_flag'] = df[col].dt.year.apply(lambda x: 1 if x < min_year or x > current_year else 0) # 1 for incorrect entries
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

def handle_lists(value):
    """
    Transform the values of a column in a list. Works for single or multiple elements.

    Parameters:
    -----------
    value : str
        Element to be transformed

    Returns:
    --------
    value: list
        Transformed string into a list of string(s)
    """
    if ',' in value:
        
        #return value.replace(' ', '').split(',')
        values = value.split(',')
        values = [i.strip() for i in values]
        return values
        
    else:
        return [value]

def split_string(df, col):
    """
    Transforms a specific column from a DataFrame using the handle_lists ​​function.

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the column to transform

    Returns:
    --------
    df: pandas.DataFrame
        Dataframe with transformed column
    """
    df[col] = df[col].apply(handle_lists)
    return df  

#-------------------------------------------------------------------------------------------------------------------------------------

# Creating flags

def internet_flag(df, col='meios_comunicacao', flag_col='internet_flag'):
    """
    Add a flag column to indicate whether the patient has access to the Internet

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the means of communication column
    flag_col : str
        Name of the flag column

    Returns:
    --------
    df : pandas.DataFrame
    """
    df[flag_col] = (df[col].apply(lambda x: 1 if 'Internet' in x else 0)).astype(int)

    return df

def public_transport_flag(df, col='meios_transporte', flag_col='public_transport_flag'):
    """
    Add a flag to indicate whether the patient uses at least one of these means of public transport: subway, bus or train

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the means of transport column
    flag_col : str
        Name of the flag column

    Returns:
    --------
    df : pandas.DataFrame
    """
    Public_Transports = {'Metrô', 'Trem', 'Ônibus'}

    df[flag_col] = (df[col].apply(lambda x: 1 if any(item in Public_Transports for item in x) else 0)).astype(int)

    return df

def deseases_flag(df, col='doencas_condicoes'):
    """
    Add a flag to indicate whether the patient has one or more deseases listed

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the deseases column

    Returns:
    --------
    df : pandas.DataFrame
    """

    deseases = ['Hipertensão', 'Diabetes', 'Tabagismo', 'AIDS', 'Gestante', 'Alcoolismo', 'Usuário de Drogas Ilícitas']

    for desease in deseases:

        name = desease.lower()

        if ' ' in name:
            name = name.replace(' ', '_')

        df[name+'_flag'] = (df[col].apply(lambda x: 1 if desease in x else 0)).astype(int)

    return df


def private_health_care_flag(df, col='em_caso_doenca_procura'):
    """
    Add a flag column to indicate whether the patient has access to private health care facilities when sick

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the column that describes which facilities the patient visits when sick (public hospital, pharmacy, etc.)

    Returns:
    --------
    df : pandas.DataFrame
    """
    df['private_health_care_flag'] = (df[col].apply(lambda x: 1 if 'Rede Privada' in x else 0)).astype(int)

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
        print(f'2 repeated values found in column {col} in {len(only_2_entries)} entry(ies).')

    if len(more_than_2_entries) != 0:
        print(f"More than 2 repeated values found in column {col} in {len(more_than_2_entries)} entry(ies).")
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
                new_id = generate_patient_id(df, col)
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
    return match.group(1) if match else 'Não se aplica'

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
        'Empregador': 1,
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
        return 5
    elif 'Não informado' in value: # Not informed
        return 0
    
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

def family_income_flag(df, col='renda_familiar', flag_col='renda_familiar_flag'):
    """
    Add a flag column to indicate whether the family income is greater than 4 minimum wages or if the entry is incorrect

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        Name of the family income column
    flag_col : str
        Name of the family income flag column

    Returns:
    --------
    df : pandas.DataFrame
    """
    df[flag_col] = (df['renda_familiar'].apply(lambda x: 1 if x in [5, 0] else 0)).astype(int)
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

def identify_outliers(df, col, lower_limit, upper_limit):
    """
    Identifies outliers in a numeric column based on lower and upper limits.

    Parameters:
    -----------
    df : pandas.DataFrame
    col : str
        The name of the numeric column
    lower_limit : float
    upper_limit : float

    Returns:
    --------
    df : pandas.DataFrame 
        The DataFrame with a new flag column indicating whether the value is an outlier (0 or 1).
    """
    df[col + '_outlier_flag'] = (~df[col].between(lower_limit, upper_limit)).astype(int)
    return df

#-------------------------------------------------------------------------------------------------------------------------------------

# Check null values

def check_null_values(df):
    """
    Check if there are any null values in the dataframe after applying cleaning functions.
    
    Parameters:
    -----------
    df : pandas.DataFrame
    """

    N_null = len(df[df.isnull().any(axis=1)])

    if N_null != 0:
        print(f'There are {N_null} null values in the dataframe.'.format(N_null))

    else:
        print('No null values in the dataframe.')


#========================================================================================================================================