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
        
        return value.replace(' ', '').split(',')
        
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
    df[flag_col] = df[col].apply(lambda x: 'Internet' in x if x else False)

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
    df[flag_col] = df['renda_familiar'].apply(lambda x: 1 if x in [5, 0] else 0)
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
    df[col + '_outlier_flag'] = ~df[col].between(lower_limit, upper_limit)
    df[col + '_outlier_flag'] = df[col + '_outlier_flag'].astype(int)
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

def main():
    """
    Main function that performs data cleaning and transformation.
    """
    url = "https://drive.google.com/file/d/1dWC1ZUPNlCQBalYPY8uP4Zzs0aue9nkQ/view?usp=sharing"
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]

    try:
        data = pd.read_csv(path)
        print('Table loaded with success.')

    except:
        print('Error when loading the table. Please contact the author.')

    # Checking for null values
    check_null_values(data)

    print('Cleaning quantitative columns...')

    lims_altura = calculate_IQR_lims(data, 'altura')
    lims_altura[0] = 40 # considering newborn babies
    lims_peso = calculate_IQR_lims(data, 'peso')
    lims_pressao_diastolica = calculate_IQR_lims(data, 'pressao_diastolica')
    lims_pressao_sistolica = calculate_IQR_lims(data, 'pressao_sistolica')

    data = identify_outliers(data, 'altura', lims_altura[0], lims_altura[1])
    data = identify_outliers(data, 'peso', lims_peso[0], lims_peso[1])
    data = identify_outliers(data, 'pressao_diastolica', lims_pressao_diastolica[0], lims_pressao_diastolica[1])
    data = identify_outliers(data, 'pressao_sistolica', lims_pressao_sistolica[0], lims_pressao_sistolica[1])

    print('Cleaning columns with True / False errors...')

    boolean_to_int_cols = [
    'obito',
    'luz_eletrica',
    'em_situacao_de_rua',
    'possui_plano_saude',
    'vulnerabilidade_social',
    'familia_beneficiaria_auxilio_brasil',
    'crianca_matriculada_creche_pre_escola'
    ]

    # Applying boolean_to_int function to each column
    for column in boolean_to_int_cols:
        data = boolean_to_int(data, column)

    print('Cleaning columns with string errors...')

    standardize_string_cols = ['meios_transporte', 'doencas_condicoes', 'meios_comunicacao', 'em_caso_doenca_procura']

    # Applying clean_column and split_string functions to each column
    for column in standardize_string_cols:
        data = clean_column(data, column)
        data = split_string(data, column)

    means_of_communication = ['Internet', 'Rádio', 'Televisão', 'Jornal', 'Não informado', 'Revista', 'Outros']

    data['meios_comunicacao'] = data['meios_comunicacao'].apply(
        lambda x: ['Outros' if item not in means_of_communication else item for item in x]
    ) # Cleaning incorrect entries

    data = internet_flag(data)''

    print('Cleaning date columns...')

    date_columns = ['data_cadastro', 'data_nascimento', 'data_atualizacao_cadastro', 'updated_at']

    # Applying the standardize_date function to each column and adding flags for incorrect entries
    for column in date_columns:
        data = standardize_date(data, column)
        data = date_flag(data, column)

    print('Cleaning columns with specific errors...')

    check_id_format(data, 'id_paciente')
    duplicates, over_2_repeated_values = check_id_duplicates(data, 'id_paciente')
    print('Fixing duplicates in id_paciente column...')
    fix_duplicates(data, 'id_paciente', duplicates)
    fix_duplicates(data, 'id_paciente', over_2_repeated_values)

    # Check for duplicates in id_paciente column
    check_id_duplicates(data, 'id_paciente')

    print('Cleaning columns with incorrect and/or random entries...')

    random_entries = ['Acomp. Cresc. e Desenv. da Criança', 'ORQUIDEA', 'ESB ALMIRANTE', '10 EAP 01']

    replace_string_columns = {'identidade_genero': [(['Homossexual (gay / lésbica)', 'Heterossexual', 'Bissexual', np.nan, 'Não', 'Sim'], 'Não informado')],
                              'raca_cor': [('Não', 'Não deseja informar')],
                              'orientacao_sexual': [('Homossexual (gay / lésbica)', 'Homossexual')],
                              'religiao': [(random_entries, 'Sem informação'),
                                           ('Não', 'Sem religião'), ('Sim', 'Outra')],
                              'escolaridade': [('Não sabe ler/escrever', 'Iletrado'), 
                                               ('Especialização/Residência', 'Especialização ou Residência')],
                              'situacao_profissional': [('SMS CAPS DIRCINHA E LINDA BATISTA AP 33', 'Não informado'),
                                                        ('Pensionista / Aposentado', 'Pensionista ou Aposentado'),
                                                        (['Não se aplica', 'Não trabalha'], 'Desempregado'),
                                                        ('Médico Urologista', 'Emprego Formal')],
                              'renda_familiar': [(['Manhã', 'Internet'], 'Não informado')]}

    for col in list(replace_string_columns.keys()):

        for item in replace_string_columns[col]:

            data = replace_strings(data, col, item[0], item[1])

    # List of functions to be applied
    functions = [(create_category_col, 'ocupacao', 'categoria_ocupacao'), 
                transform_family_income,
                family_income_flag,
                create_social_security_col]

    # Iterating over the functions and applying them to the dataframe
    for func in functions:
        if isinstance(func, tuple):
            # Function that needs additional parameters
            data = func[0](data, *func[1:])
        else:
            # Function with no additional parameters
            data = func(data)

    # Checking for null values again
    check_null_values(data)

    data[['renda_familiar', 'altura', 'peso', 'pressao_sistolica', 'pressao_diastolica']] = data[['renda_familiar', 'altura', 'peso', \
         'pressao_sistolica', 'pressao_diastolica']].apply(pd.to_numeric)

    data_no_null_values = data.dropna()


    print('-'*40, 'Finish cleaning table!', '-'*40)

    retrieve_data = input("Do you wish to retrieve the cleaned dataset? (y/n)")

    if retrieve_data == 'y':

        null_values = input("Do you want to include rows with null values? (y/n)") 

        if null_values == 'y':

            data.to_csv('final_dataset.csv', index=False, sep =';', decimal=',') # you can change to '.' if you want

        else:
            data_no_null_values.to_csv('final_dataset_dropna.csv', index=False, sep =';', decimal=',')
    else:
        pass

if __name__ == "__main__":
    main()