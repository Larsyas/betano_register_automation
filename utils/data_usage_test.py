import sqlite3
from pathlib import Path


ROOT_DIR = Path(__file__).parent.parent
DB_FILE = f'{ROOT_DIR}\\utils\\db.sqlite3'
TABLE_NAME = 'data'


class Conta:
    def __init__(self, row: tuple):
        self.email: str = row[1]
        self.email_password: str = row[2]
        self.cpf: str = row[3]
        self.name: str = row[4]
        self.date_of_birth: str = row[5]
        self.betano_password: str = row[6]
        self.game_link: str = row[7]
        self.coupon: str = row[8]
        self.date_of_creation: str = row[10]

    def to_dict(self):
        return {
            'email': self.email,
            'email_password': self.email_password,
            'cpf': self.cpf,
            'name': self.name,
            'date_of_birth': self.date_of_birth,
            'betano_password': self.betano_password,
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
        self._account_gen = self._yield_account()

    def connect_to_db(self):
        self.connection = sqlite3.connect(DB_FILE)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f'SELECT * FROM {TABLE_NAME} ')
        self.rows: list = self.cursor.fetchall()

    # def next_account(self):
    #     try:
    #         return next(self._yield_account())
    #     except StopIteration:
    #         return None

    def _yield_account(self):
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

    def next_account(self):
        try:
            return next(self._account_gen)
        except StopIteration:
            return None


######################################################

# if __name__ == '__main__':
#      a = AccountIterator()
#      a.connect_to_db()
#      a.yield_account()
#      print('Total de contas: ', a.total_accounts)
#      print('Total de ciclos: ', a.cicle_num)

#      a.cursor.close()
#      a.connection.close()
