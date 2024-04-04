import sqlite3
import random
import string
from pathlib import Path
from pynput.keyboard import Controller, Key
from utils.addresses import avenidas
import pyautogui

UTILS_DIR = Path(__file__).parent
ADDRESS_DB = UTILS_DIR / 'enderecos.sqlite3'

# Conecte-se ao banco de dados SQLite (ou crie um se não existir)
conn = sqlite3.connect(ADDRESS_DB)
c = conn.cursor()

# Cria a tabela de endereços, se não existir
c.execute('''
    CREATE TABLE IF NOT EXISTS enderecos (
        endereco TEXT PRIMARY KEY
    )
''')


# Dicionário de DDDs por estado
ddd_por_estado = {
    "SP": "11",
    "RJ": "21",
    "RN": "84",
    "PB": "83",
    "CE": "85",
    "SC": "49",
}


class FakeAddress():
    def __init__(self):
        self.fake_rua = None
        self.fake_numero_casa = None
        self.fake_estado = None
        self.fake_phone = None
        self.fake_endereco = None

    def gerar_endereco_e_phone_unicos(self):
        while True:
            # Escolha aleatoriamente uma avenida
            self.fake_rua, self.fake_estado = random.choice(avenidas)

            # Gere um número de casa aleatório que não seja maior do que 75
            self.fake_numero_casa = random.randint(400, 800)

            # Crie um número fictício com o DDD do estado
            self.fake_phone = f"{ddd_por_estado[self.fake_estado]}99{''.join(random.choices(string.digits, k=7))}"

            # Junte tudo em uma string
            self.fake_endereco = f"{self.fake_estado} {self.fake_rua}{self.fake_numero_casa} - Número fictício: {self.fake_phone}"

            return {
                "rua": self.fake_rua,
                "numero_casa": self.fake_numero_casa,
                "estado": self.fake_estado,
                "phone": self.fake_phone,
                "endereco_completo": self.fake_endereco
            }

    def save_fake_data_usage(self):
        # Verifique se o endereço já foi usado
        c.execute('SELECT * FROM enderecos WHERE endereco = ?',
                  (self.fake_endereco,))
        if c.fetchone() is None:
            # Se não foi usado, adicione ao banco de dados e retorne o endereço
            c.execute('INSERT INTO enderecos VALUES (?)',
                      (self.fake_endereco,))
            conn.commit()


if __name__ == '__main__':
    fake_data_income = FakeAddress()
    fake_data_income.gerar_endereco_e_phone_unicos()

    print(fake_data_income.fake_endereco)
    print(fake_data_income.fake_numero_casa)
    print(fake_data_income.fake_estado)
    print(fake_data_income.fake_phone)
    print(fake_data_income.fake_rua)

    fake_data_income.save_fake_data_usage()
