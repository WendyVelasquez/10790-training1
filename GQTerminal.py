# nome(s): WENDY CUELLAR // DANIEL CARDOZO
# Geo_Quiz: Quiz aleatório sob cidades capitais do mundo. Descobre o quanto sabes de geografia.
# data de entrega: 29/04/2024


import random
import sqlite3 #Importa base de dados

con = sqlite3.connect("capitais.db")
cur = con.cursor()

nome = input("\nQual é o seu nome?: ")

print(f"\nOlá {nome}!\nBem-vindo a Geo-Quiz\n")

while True:

    nroPerguntas = input("Quantas perguntas deseja responder nesta volta?: ")
    if not nroPerguntas.isdigit():
        print("\nResposta invalida. Digite o número de perguntas para poder jogar.\n") #Mostra uma mensagem se a resposta não for um número
    else:
        pontos_totais = 0  #Contador de pontos totais em 0
        break

print("\nRegras:\nVocê tem 4 opções disponíveis para cada pergunta, 1 é verdadeira.\nSe a sua resposta estiver correta você somará 100 pontos.\nBoa sorte.\n") #Regras do jogo

def obtener_pais():
    global pontos_totais  
    continentes = ['europa', 'americas', 'asiaticas', 'africa', 'oceania']
    random.shuffle(continentes) #Pesquisa um continente aleatoriamente na base de dados

    for i in range(int(nroPerguntas)): #Executa o ciclo dependendo da quantidade de perguntas que o usuário deseja responder       
        resultado = cur.execute(f'SELECT pais, capital FROM {continentes[0]}').fetchall() 
        random.shuffle(resultado)
        pais, capital_correta = resultado[0] #Pesquisa um país e a capital correspondente na base de dados
        print(f"\n{i+1}º pergunta de {nroPerguntas}:\n"
              f"\nQual é a capital de {pais}?\n")
        pontos_totais += responder_pergunta(capital_correta) #Soma de pontos

def responder_pergunta(capital_correta):
    opcoes = obtener_opcoes(capital_correta)
    
    pontos = 0 #Contador de pontos em 0

    for i, opcao in enumerate(opcoes, start=1): #Enumera as opções para responder de 1 a 4
        print(f"{i}. {opcao}")

    while True:
        
        resposta_usuario = input("\nEscolha a opção correta (digite o número): ")
        if not resposta_usuario.isdigit():
            print("\nResposta invalida. Digite um número de 1 a 4: ") #Mostra uma mensagem se a resposta não for um número
        else:
            resposta_usuario = int(resposta_usuario)
            if resposta_usuario not in [1, 2, 3, 4]:
                print("\nResposta invalida. Digite o número da opção que considera correta:") #Mostra uma mensagem se a resposta não estiver entre 1 e 4
            else:
                break

    if opcoes[resposta_usuario - 1] == capital_correta:
        pontos += 100 #Soma de 100 pontos no contador
        print(f"\nMuito bom {nome}! Resposta correta! Você ganhou 100 pontos.\n" 
              f"Total de pontos: {pontos_totais + pontos}\n") #Soma de 100 pontos pela resposta correta
        print("* "*40)

    else:
        print(f"\nResposta incorreta. A resposta correta é: {capital_correta}. Total de pontos: {pontos_totais}\n") #Indica a resposta correta, mantem os pontos acummulados
        print("* "*40)
        
    return pontos

def obtener_opcoes(capital_correta): #Retorna uma lista de opções para responder à pergunta, incluindo a capital correta e três capitais aleatórias adicionais
    opcoes = [capital_correta]

    while len(opcoes) < 4:
        resposta_aleatoria = cur.execute('SELECT capital FROM (SELECT capital FROM europa UNION SELECT capital FROM americas UNION SELECT capital FROM asiaticas UNION SELECT capital FROM africa UNION SELECT capital FROM oceania) ORDER BY RANDOM() LIMIT 1;').fetchone()[0]
        if resposta_aleatoria not in opcoes:
            opcoes.append(resposta_aleatoria) #Pesquisa 3 capitais na base de dados

    random.shuffle(opcoes) #Pesquisa 3 capitais aleatórias como opções na base de dados
    return opcoes

obtener_pais()
con.close()

print(f"\nMuito obrigado {nome} por jogar GeoQuiz.\nNesta rodada de {nroPerguntas} perguntas, sua pontuação final é: {pontos_totais} pontos.\n") #Mensagem de despedida com a soma do total de pontos
print("* "*40)