import sqlite3
#cria bd
banco = sqlite3.connect('CEASA.db')
#para conseguir dar comandos sql
cursor = banco.cursor()
#cria a tabela

cursor.execute("CREATE TABLE Produtos(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, data TEXT NOT NULL, produto TEXT NOT NULL, tipo TEXT, unidade_embalagem TEXT, valor_unidade_de_medidas REAL, unidade_de_medidas TEXT, situacao_mercado TEXT, valor_min NUMERIC, valor_m_c_do_dia NUMERIC, valor_max NUMERIC, valor_variacao REAL, estados_siglas TEXT)")

banco.commit()

# cursor.execute("SELECT * FROM Produtos")
# rows = cursor.fetchall()

# # Exibindo os resultados
# for row in rows:
#     print(row)

# # Fechando a conexão
# banco.close()
####DELETAR BD
##cursor.execute("DELETE FROM Produtos")

# Commitar a transação para efetivar a deleção
#banco.commit()

# Fechar a conexão
banco.close()
