# Projeto de automação para o estudo de inglês

Esse é um programa com interface gráfica que visa automatizar a parte chata do meu estudo de inglês. Ele é específico para minha necessidade, portanto, talvez não seja útil para todas as pessoas. Abaixo encontrará mais detalhes sobre o projeto, e até mesmo um [vídeo explicativo no YouTube](https://www.youtube.com/watch?v=6v5oCyA6ISs).


> ⚠️ **Atenção:** este repositório tem fins demonstrativos apenas. Apesar de conter todo o código-fonte, nem todos os arquivos necessários para o funcionamento completo estão disponíveis — como é o caso do banco de dados utilizado.  
> Optei por **não executar esse banco de dados na nuvem**, mas se quiser ter acesso a ele, é só entrar em contato comigo!

## Vídeo de explicação

Caso queira ver sobre os detalhes do programa sem ler a explicação abaixo, você pode visualizar este vídeo no meu canal do YouTube:  
[Assista no YouTube](https://www.youtube.com/watch?v=6v5oCyA6ISs)

## Detalhes sobre o programa

Esse programa cria uma interface gráfica que oferece duas opções para seguir:  
1. Abrir uma janela de pesquisa  
2. Abrir uma janela de automação Anki

### Etapa 1

A janela de pesquisa permite a busca de significados de palavras em inglês, separadas por vírgula. Essa busca é feita com o Selenium, extraindo dados do site [Reverso Context](https://context.reverso.net/traducao/), retornando os 4 primeiros resultados, quando houver.

Nessa etapa, acontecem outras coisas:

1. Uma nova janela é criada para mostrar frases que contenham as palavras buscadas, e essas frases são provenientes do banco de dados que estou utilizando (ele não está disponível aqui, mas foi populado através de um arquivo do site [Tatoeba](https://tatoeba.org/pt-br/)).
2. Os significados das palavras são buscados através de web scraping com o Selenium, e são adicionados a uma planilha (.xlsx), juntamente com a palavra em inglês.

No final dessa etapa, quando as frases forem selecionadas pelo usuário e o botão **"Salvar dados"** for acionado, será aberta uma janela para escolher o local que o arquivo `.xlsx` será armazenado.  
Com o arquivo gerado, nós passamos para a segunda etapa do programa, que é a janela de automação do Anki.

### Etapa 2

Nessa etapa, será automatizada a inserção de cartões no programa Anki, contendo a frase em inglês na parte frontal, e no verso os significados da palavra que é o alvo do estudo.

Como essa etapa utiliza a API **AnkiConnect** para inserir os dados no programa Anki de forma automatizada, o programa precisa estar em execução no computador.

A partir disso, o usuário deverá escolher o arquivo gerado na Etapa 1 (contendo as frases, palavras e traduções) e em seguida clicar em **"Iniciar"**.  
Uma nova janela será aberta para que o usuário escolha o deck (baralho do Anki) que ele deseja inserir os novos cartões. Com isso feito, a automação iniciará, gerando informações do que foi feito no campo de **Log**.

---

## Habilidades utilizadas

- Python  
- Selenium  
- Requests  
- CustomTkinter  
- Web scraping  
- Programação Orientada a Objetos e modularização  
- Banco de dados para consulta de frases (populado através de arquivo baixado do site [Tatoeba](https://tatoeba.org/pt-br/))  
- Threads para tarefas simultâneas  
- Automação de planilhas  
- Tratamento de exceções  
- Integração com o programa **Anki** através da API **AnkiConnect**  
- Projeto estruturado com uso de diferentes diretórios e múltiplos arquivos  
- Uso de Git e GitHub, com uma *branch* adicional para desenvolver features novas sem afetar a *main branch*


## Considerações finais

Como dito anteriormente, esse projeto foi criado com um objetivo pessoal e atende a uma necessidade específica. 
Porém, se por algum motivo você quiser utilizá-lo na sua máquina, precisará também do banco de dados que eu não coloquei aqui nos arquivos. Para isso, pode entrar em contato comigo que eu faço o envio! :)

Se quiser mais detalhes sobre o projeto ou se precisar entrar em contato comigo, pode me enviar uma mensagem através do LinkedIn ou e-mail, estão na bio do meu perfil!
