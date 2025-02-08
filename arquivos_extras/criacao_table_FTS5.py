import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("frases.db")
cursor = conn.cursor()

# Criar a tabela FTS5 com id e texto
cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS frases_fts USING fts5(id UNINDEXED, texto)")

# Copiar dados da tabela original para a tabela FTS (evita duplicação)
cursor.execute("""
    INSERT INTO frases_fts (id, texto)
    SELECT id, texto FROM frases
    WHERE id NOT IN (SELECT id FROM frases_fts)
""")

# Salvar mudanças e fechar conexão
conn.commit()
conn.close()
