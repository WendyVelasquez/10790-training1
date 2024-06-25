import random
import sqlite3
import tkinter as tk
from tkinter import PhotoImage

con = sqlite3.connect("capitais.db")
cur = con.cursor()

janela = tk.Tk()
janela.title("GeoQuiz")
janela.geometry("600x550")
janela.resizable(width=False, height=False)

fonte_title = ("Cascadia Code", 20, "bold")
fonte_texto = ("Cascadia Code", 13)

nome = ""
nroPerguntas = 0
pontos_totais = 0
perguntas_restantes = 0
resultado = []
capital_correta = ""

imagen_jogar = PhotoImage(file="jugar.png")
imagen_sair = PhotoImage(file="exit.png")
imagen_iniciar = PhotoImage(file="check.png")
imagen_repetir = PhotoImage(file="repetir.png")
imagen_check = PhotoImage(file="check.png")

bemvindo_label = tk.Label(janela, text="Bem-vindo ao\nGeoQuiz!", font=fonte_title)
bemvindo_label.pack(pady=60)
jogar_button = tk.Button(janela, image=imagen_jogar, command=lambda: mostrar_entrada_nome())
jogar_button.pack(pady=10)

nome_label = tk.Label(janela, text="\n\nQual é o seu nome?:", font=fonte_texto)
nome_entry = tk.Entry(janela, font=fonte_texto)
iniciar_button = tk.Button(janela, image=imagen_iniciar, command=lambda: iniciar_juego())

pergunta_label = tk.Label(janela, text="", wraplength=500, font=fonte_texto)
pergunta_label.pack(pady=20)
pergunta_label.pack_forget()

botoes_opcoes = [tk.Button(janela, text="", font=fonte_texto, command=lambda i=i: verificar_resposta(i)) for i in range(4)]
for botao in botoes_opcoes:
 botao.pack(pady=5)
 botao.pack_forget()

result_label = tk.Label(janela, text="", font=fonte_texto)
result_label.pack(pady=10)

botao_jogar_novamente = tk.Button(janela, image=imagen_repetir, command=lambda: reiniciar_jogo())
botao_jogar_novamente.pack(pady=20)
botao_jogar_novamente.pack_forget()

botao_sair = tk.Button(janela, image=imagen_sair, command=janela.quit)
botao_sair.pack(side=tk.BOTTOM, pady=10)

def mostrar_entrada_nome():
    bemvindo_label.pack_forget()
    jogar_button.pack_forget()

    nome_label.pack(pady=10)
    nome_entry.pack(pady=5)
    iniciar_button.pack(pady=20)

def iniciar_juego():
    global nome, nroPerguntas, pontos_totais, perguntas_restantes

    nome = nome_entry.get()
    if not nome:
        result_label.config(text="\n\nPor favor, insira seu nome.")
        return

    nome_label.pack_forget()
    nome_entry.pack_forget()
    iniciar_button.pack_forget()

    perguntas_label = tk.Label(janela, text="\n\nQuantas perguntas deseja responder nesta volta?:", font=fonte_texto)
    perguntas_label.pack(pady=10)
    perguntas_entry = tk.Entry(janela, font=fonte_texto)
    perguntas_entry.pack(pady=5)
    confirmar_button = tk.Button(janela, image=imagen_check, command=lambda: confirmar_perguntas(perguntas_entry, perguntas_label, confirmar_button))
    confirmar_button.pack(pady=20)

def confirmar_perguntas(perguntas_entry, perguntas_label, confirmar_button):
    global nroPerguntas, pontos_totais, perguntas_restantes

    try:
        nroPerguntas = int(perguntas_entry.get())
        if nroPerguntas <= 0:
            raise ValueError
    except ValueError:
        result_label.config(text="Resposta invalida.\nDigite um número válido de perguntas.")
        return

    perguntas_label.pack_forget()
    perguntas_entry.pack_forget()
    confirmar_button.pack_forget()

    pontos_totais = 0
    perguntas_restantes = nroPerguntas

    result_label.config(text=f"Instruções:\nTem 4 opções para cada pergunta, 1 é verdadeira.\nSe a sua resposta estiver correta você somará 100 pontos.\nBoa sorte.")
    
    pergunta_label.pack(pady=20)
    for botao in botoes_opcoes:
     botao.pack(pady=5)
    obtener_pais()

def obtener_pais():
    global resultado, capital_correta, perguntas_restantes

    if perguntas_restantes == 0:
        finalizar_jogo()
        return

    continentes = ['europa', 'americas', 'asiaticas', 'africa', 'oceania']
    random.shuffle(continentes)
    resultado = cur.execute(f'SELECT pais, capital FROM {continentes[0]}').fetchall()
    random.shuffle(resultado)
    pais, capital_correta = resultado[0]
    mostrar_pregunta(pais)

def mostrar_pregunta(pais):
    global capital_correta

    pergunta_label.config(text=f"Restam {perguntas_restantes}º de {nroPerguntas}º perguntas.\n\nQual é a capital de {pais}?")
    opcoes = obtener_opcoes(capital_correta)

    for i, opcao in enumerate(opcoes):
        botoes_opcoes[i].config(text=opcao)

def verificar_resposta(index):
    global pontos_totais, perguntas_restantes

    resposta_ut = botoes_opcoes[index].cget('text')

    if resposta_ut == capital_correta:
        pontos_totais += 100
        result_label.config(text=f"Muito bom {nome}! Resposta correta!\nVocê ganhou 100 puntos.\nTotal de pontos: {pontos_totais}")
    else:
        result_label.config(text=f"Resposta incorreta.\nA resposta correta é: {capital_correta}.\nTotal de pontos: {pontos_totais}")

    perguntas_restantes -= 1
    if perguntas_restantes > 0:
        obtener_pais()
    else:
        finalizar_jogo()

def obtener_opcoes(capital_correta):
    opcoes = [capital_correta]

    while len(opcoes) < 4:
        resposta_aleatoria = cur.execute('SELECT capital FROM (SELECT capital FROM europa UNION SELECT capital FROM americas UNION SELECT capital FROM asiaticas UNION SELECT capital FROM africa UNION SELECT capital FROM oceania) ORDER BY RANDOM() LIMIT 1;').fetchone()[0]
        if resposta_aleatoria not in opcoes:
            opcoes.append(resposta_aleatoria)

    random.shuffle(opcoes)
    return opcoes

def finalizar_jogo():
    result_label.config(text=f"\n\n\nMuito obrigado {nome} por jogar GeoQuiz.\nNesta rodada de {nroPerguntas} perguntas\nSua pontuação final é: {pontos_totais} pontos.\n\nGostaria de jogar novamente?")
    pergunta_label.pack_forget()
    for botao in botoes_opcoes:
        botao.pack_forget()
    botao_jogar_novamente.pack(pady=60)

def reiniciar_jogo():
    global nome, nroPerguntas, pontos_totais, perguntas_restantes

    nome = ""
    nroPerguntas = 0
    pontos_totais = 0
    perguntas_restantes = 0

    pergunta_label.config(text="")
    for botao in botoes_opcoes:
        botao.pack_forget()
    result_label.config(text="")

    bemvindo_label.pack(pady=20)
    jogar_button.pack(pady=20)
    botao_jogar_novamente.pack_forget()

janela.mainloop()
con.close()
