import random

import pandas as pd

# Carregar apenas a primeira coluna (caso o .tsv tenha várias colunas)
df = pd.read_csv("eng_sentences.tsv", sep="\t", names=["frase"], usecols=[2], dtype=str)

# Filtrar frases que contêm a palavra desejada (ignorando maiúsculas/minúsculas)
palavra = "weather"
resultado = df[df["frase"].str.contains(palavra, case=False, na=False)]

# Exibir algumas frases encontradas
print(resultado.sample(10))

# # Salvar o resultado em um novo arquivo
# resultado.to_csv("frases_filtradas.tsv", sep="\t", index=False)