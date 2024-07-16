import sqlite3

banco = sqlite3.connect('ceasa.db')

cursor = banco.cursor()
cursor.execute("CREATE TABLE Produtos(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, data TEXT NOT NULL, produto TEXT NOT NULL, tipo TEXT, unidade_embalagem TEXT, valor_unidade_de_medidas REAL, unidade_de_medidas TEXT, situacao_mercado TEXT, valor_min NUMERIC, valor_m_c_do_dia NUMERIC, valor_max NUMERIC, valor_variacao REAL, estados_siglas TEXT, cidade TEXT)")

banco.commit()

banco.close()