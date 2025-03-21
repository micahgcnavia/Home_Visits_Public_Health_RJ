from imp import reload 
import lib.functions as functions
reload(functions) 
from lib.functions import *

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

    data = internet_flag(data) # Filtering which patients have access to the Internet
    data = public_transport_flag(data) # Filtering which patients use public transportation (subway, metro or bus)
    data = deseases_flag(data) # Filtering which patients have common deseases
    data = private_health_care_flag(data) # Filtering whether the patient has access to private health care facilities

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

    data_no_null_values = data.dropna() # Table with no null values

    print('-'*40, 'Finish cleaning table!', '-'*40)

    retrieve_data = input("Do you wish to retrieve the cleaned dataset? (y/n)")

    if retrieve_data == 'y':

        null_values = input("Do you want to include rows with null values? (y/n)") 

        if null_values == 'y':

            data.to_csv('final_dataset.csv', index=False, sep =';', decimal=',') # you can change decimal delimiter to '.' if you want

        else:
            data_no_null_values.to_csv('final_dataset_dropna.csv', index=False, sep =';', decimal=',')
    else:
        pass

if __name__ == "__main__":
    main()