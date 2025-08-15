import pandas as pd

def treating_appointments(appointments_sheet):

    appointments_df = pd.read_excel(appointments_sheet)

    appointments_df_columns = ['ID agendamento', 'ID cliente','Email','Telefone',
                            'Unidade do agendamento', 'Procedimento', 'Data', 'Status']

    appointments_df = appointments_df[appointments_df_columns]

    branches_to_consider = ['TUCURUVI', 'SANTOS', 'LAPA', 'IPIRANGA', 'COPACABANA',
                                'CAMPINAS','JARDINS', 'SOROCABA','TIJUCA','SANTO AMARO',
                                'ITAIM', 'LONDRINA', 'MOEMA','TATUAPÉ', 'MOOCA','OSASCO',
                                'ALPHAVILLE','SÃO BERNARDO', 'VILA MASCOTE', 'GUARULHOS']

    appointments_df = appointments_df.loc[appointments_df['Unidade do agendamento'].isin(branches_to_consider)]

    # Treating the date values
    appointments_df['Data'] = pd.to_datetime(appointments_df['Data'], format='%d/%m/%Y')
    appointments_df["Mes"] = appointments_df['Data'].dt.month

    # Data in pt-Br format
    appointments_df['Data'] = appointments_df['Data'].dt.strftime('%d/%m/%Y')

    appointments_df = appointments_df.loc[appointments_df["Procedimento"].str.contains("AVALIAÇÃO",case= False)]
    appointments_df = appointments_df.loc[appointments_df["Status"] == "Atendido"]

    appointments_df_columns = ['ID agendamento', 'Data', 'Mes',
                            'Unidade do agendamento','ID cliente',
                            'Email','Telefone', 'Status']

        # Reordering the columns
    appointments_df = appointments_df[appointments_df_columns]

    appointments_df['Telefone'] = appointments_df['Telefone'].astype(str)

    def split_Telefones(df):
    # Crie uma nova lista para armazenar as novas linhas
        new_rows = []

        for _, row in df.iterrows():
            # Verifique se o valor de 'Telefones' não é nulo
            if pd.notna(row['Telefone']):
                Telefoness = row['Telefone'].split(' / ')
                for Telefones in Telefoness:
                    # Crie uma nova linha para cada Telefones
                    new_row = row.copy()
                    new_row['Telefone'] = Telefones
                    new_rows.append(new_row)

        return pd.DataFrame(new_rows)

    appointments_df = split_Telefones(appointments_df)

    return appointments_df

# Carregar o arquivo Excel

def treating_indicate(indicate_excel):
    
    xls = pd.ExcelFile(indicate_excel)

    # Lista para guardar os dataframes de cada aba
    dfs = []

    # Iterar por cada aba
    for sheet_name in xls.sheet_names:
        # Ler a aba
        df = pd.read_excel(xls, sheet_name=sheet_name)
        # Selecionar colunas específicas
        # Adicionar coluna 'Unidade' com o nome da aba
        df['Unidade'] = sheet_name
        df['Unidade'] = df['Unidade'].str.upper()
        # Append ao lista
        dfs.append(df)

    # Concatenar todos os dataframes
    indique_df = pd.concat(dfs, ignore_index=True)

    return indique_df

def merge_and_groupby(indique_df,appointments_df):

    indique_appointments_merge_email = pd.merge(indique_df,appointments_df,
                                        left_on='Email compartilhador',
                                        right_on='Email',
                                        how='left')

    indique_appointments_merge_telefone = pd.merge(indique_df,appointments_df,
                                        left_on='Telefone compartilhador',
                                        right_on='Telefone',
                                        how='left')

    indique_appointments_merge_final = pd.concat([indique_appointments_merge_email,indique_appointments_merge_telefone])

    indique_appointments_merge_final = indique_appointments_merge_final.loc[~indique_appointments_merge_final['ID agendamento'].isna()]

    indique_appointments_merge_final = indique_appointments_merge_final.drop_duplicates(subset=['ID'])

    base_indique_final = indique_appointments_merge_final

    base_indique_final_columns = ['ID', 'Compartilhador', 'Email compartilhador',
                                'Telefone compartilhador', 'Consultor','Unidade', 'Criado em',
                                'ID agendamento', 'Data','ID cliente', 'Status','Leads Gerados']

    base_indique_final = base_indique_final[base_indique_final_columns]


    ## Aguardando confirmação da Pat se consider ou não.
    # duplicados = base_indique_final.loc[base_indique_final['ID agendamento'].duplicated(keep=False)]

    # duplicados = duplicados.sort_values(by=['ID agendamento'])

    # duplicados

    indique_gp = base_indique_final.groupby(["Consultor",'Unidade']).agg({'Leads Gerados' : 'sum'}).reset_index()

    indique_gp = indique_gp.sort_values(by=['Leads Gerados'],ascending=False)

    return indique_gp
