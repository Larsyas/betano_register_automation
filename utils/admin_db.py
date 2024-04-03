import pandas as pd
import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DB_NAME = 'db.sqlite3'
DB_FILE = f'{ROOT_DIR}\\utils\\{DB_NAME}'
TABLE_NAME = 'data'

dataframe = pd.read_excel('data.xlsx', dtype={'CPF': str})
connection = sqlite3.connect(DB_NAME)


cursor = connection.cursor()
cursor.execute(f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} '
               '('
               'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               'EMAIL VARCHAR,'
               'SENHA VARCHAR,'
               'CPF INTEGER,'
               'NOME VARCHAR,'
               'NASCIMENTO DATETIME,'
               'SENHA_CONTA VARCHAR,'
               'LINK_JOGO VARCHAR,'
               'CUPOM VARCHAR,'
               'QUANTIDADE INTEGER,'
               'DATA_CADASTRO DATETIME'
               ')'
               )

# cursor.execute(f'DELETE FROM your_table WHERE index IS NULL;')

cursor.close()
# connection.commit()

# Copiar os dados do dataframe para a tabela do banco de dados
# dataframe = pd.read_excel('data.xlsx', dtype={'CPF': str})
# dataframe.to_sql(TABLE_NAME, connection, if_exists='replace', index=True)


# dataframe = dataframe.drop(dataframe[dataframe.index < 576].index)
# dataframe = dataframe.reset_index(drop=True)
dataframe.to_sql(TABLE_NAME, connection, if_exists='replace', index=True)
connection.commit()
connection.close()
