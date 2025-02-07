import sqlite3
import csv

# Nome dos arquivos
tsv_file = "eng_sentences.tsv"
db_name = "frases.db"
log_file = "erros_importacao.log"

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Criar a tabela (se ainda não existir)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS frases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto TEXT NOT NULL
    )
""")

# Contadores
total_linhas = 0
linhas_inseridas = 0
linhas_com_erro = 0

# Abrir o arquivo de log para registrar erros
with open(log_file, "w", encoding="utf-8") as log:
    log.write("Linhas com erro durante a importação:\n\n")

    # Abrir e ler o arquivo TSV
    with open(tsv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")  # Define o delimitador como TAB

        for linha_num, row in enumerate(reader, start=1):
            total_linhas += 1

            try:
                if len(row) >= 3:  # Garante que há pelo menos 3 colunas
                    frase = row[2].strip()  # Pega a terceira coluna e remove espaços extras
                    if frase:  # Evita inserir frases vazias
                        cursor.execute("INSERT INTO frases (texto) VALUES (?)", (frase,))
                        linhas_inseridas += 1
                else:
                    linhas_com_erro += 1
                    log.write(f"Linha {linha_num}: Número insuficiente de colunas - {row}\n")
            except Exception as e:
                linhas_com_erro += 1
                log.write(f"Linha {linha_num}: Erro inesperado - {e}\n")

# Confirmar as alterações
conn.commit()

# Contar os registros no banco após inserção
cursor.execute("SELECT COUNT(*) FROM frases")
total_no_banco = cursor.fetchone()[0]

# Fechar conexão
conn.close()

# Exibir resumo da importação
print("Processo de importação concluído!")
print(f"Total de linhas no TSV: {total_linhas}")
print(f"Linhas inseridas com sucesso: {linhas_inseridas}")
print(f"Linhas com erro: {linhas_com_erro}")
print(f"Total de registros no banco: {total_no_banco}")

# Se houver erros, avisar o usuário
if linhas_com_erro > 0:
    print(f"⚠️ Algumas linhas apresentaram problemas. Verifique o arquivo '{log_file}' para mais detalhes.")
