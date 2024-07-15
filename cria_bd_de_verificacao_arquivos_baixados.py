import sqlite3

# Conecta ao banco de dados (cria um novo se não existir)
'''CRIADO'''
conn = sqlite3.connect('BASE_CEASA_PR.db')

# Cria um cursor para interagir com o banco de dados
cursor = conn.cursor()

# Cria a tabela de usuários
'''Criado'''
cursor.execute('''
    CREATE TABLE IF NOT EXISTS arquivos_baixados (
        id INTEGER PRIMARY KEY,
        nome_arquivo TEXT NOT NULL,
        url_arquivo VARCHAR(255) NOT NULL
    )
''')

# Salva as alterações
conn.commit()
