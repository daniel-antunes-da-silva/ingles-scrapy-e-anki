# Procurar uma forma de encontrar FRASES com as palavras. Pode ser nesse site com Selenium, ou em outro. Ou chat gpt, sei lá!

import requests
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

url = 'https://context.reverso.net/traducao/ingles-portugues/weather'

resposta = requests.get(url, headers=headers).text

# print(resposta)
print(resposta.count('<span class="text" lang="en">'))

# print(resposta)
# Expressão regular para capturar o conteúdo dentro do <span class="display-term">
# padrao_palavras = r'<span class="display-term">(.*?)</span>'
# palavras = re.findall(padrao_palavras, resposta)
# print(palavras)
#
# padrao_frases = r'<span class="text" lang="en">([\s\S]*?)</span>'
# frases = re.findall(padrao_frases, resposta)
#
# print(frases)
