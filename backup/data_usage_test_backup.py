import sqlite3
from pathlib import Path
import time


ROOT_DIR = Path(__file__).parent.parent
DB_FILE = f'{ROOT_DIR}\\utils\\db.sqlite3'
TABLE_NAME = 'data'


class Conta:
    def __init__(self, row):
        self.email = row[1]
        self.email_password = row[2]
        self.cpf = row[3]
        self.name = row[4]
        self.date_of_birth = row[5]
        self.game_link = row[7]
        self.coupon = row[8]
        self.date_of_creation = row[10]

    def to_dict(self):
        return {
            'email': self.email,
            'email_password': self.email_password,
            'cpf': self.cpf,
            'name': self.name,
            'date_of_birth': self.date_of_birth,
            'game_link:': self.game_link,
            'coupon': self.coupon,
            'date_of_creation': self.date_of_creation,
        }


class AccountIterator():
    def __init__(self):
        self.account_num = 0
        self.total_accounts = 0
        self.cicle_num = 1
        self.connection: sqlite3.Connection
        self.cursor: sqlite3.Cursor
        self.rows = None
        self.contas = []  # Lista para armazenar as instâncias da classe Conta

    def connect_to_db(self):
        self.connection = sqlite3.connect(DB_FILE)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f'SELECT * FROM {TABLE_NAME} ')
        self.rows = self.cursor.fetchall()

    def account_loop(self):
        if self.rows is not None:
            for row in self.rows:
                conta = Conta(row)
                self.account_num += 1
                self.total_accounts += 1

                if self.account_num == 16:
                    self.cicle_num += 1
                    self.account_num = 0

                yield conta  # Aqui usamos 'yield' em vez de 'return'
        else:
            self.connect_to_db()


iterador = AccountIterator()
iterador.connect_to_db()

for conta in iterador.account_loop():
    print(conta.name)


iterador.cursor.close()
iterador.connection.close()
