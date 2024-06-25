import random
import sqlite3
import tkinter as tk
from tkinter import PhotoImage

# Conexión a la base de datos
con = sqlite3.connect("capitais.db")
cur = con.cursor()

# Configuración de la ventana principal
janela = tk.Tk()
janela.title("GeoQuiz")
janela.geometry("600x550")
janela.resizable(width=False, height=False)

# Configuración de fuentes
fonte_title = ("Cascadia Code", 20, "bold")
fonte_texto = ("Cascadia Code", 13)

# Variables globales
nome = ""
nroPerguntas = 0
pontos_totais = 0
perguntas_restantes = 0
resultado = []
capital_correta = ""
paises_ja_perguntados = []
continente_selecionado = ""

# Cargar imágenes para los botones
imagen_jogar = PhotoImage(file="jugar.png")
imagen_sair = PhotoImage(file="exit.png")
imagen_iniciar = PhotoImage(file="check.png")
imagen_repetir = PhotoImage(file="repetir.png")
imagen_check = PhotoImage(file="check.png")
imagen_oceania = PhotoImage(file="oceania.png")
imagen_america = PhotoImage(file="america.png")
imagen_asia = PhotoImage(file="asia.png")
imagen_europa = PhotoImage(file="europa.png")
imagen_africa = PhotoImage(file="africa.png")

# Crear y configurar elementos de la GUI
bemvindo_label = tk.Label(janela, text="Bem-vindo ao\nGeoQuiz!", font=fonte_title)
bemvindo_label.pack(pady=60)
jogar_button = tk.Button(janela, image=imagen_jogar, command=lambda: mostrar_entrada_nome())
jogar_button.pack(pady=10)

nome_label = tk.Label(janela, text="\n\nQual é o seu nome?:", font=fonte_texto)
nome_entry = tk.Entry(janela, font=fonte_texto)
iniciar_button = tk.Button(janela, image=imagen_iniciar, command=lambda: mostrar_selecionar_continente())

continente_label = tk.Label(janela, text="Selecione o continente:", font=fonte_texto)
continente_botoes = [
    tk.Button(janela, image=imagen_europa, command=lambda: selecionar_continente("europa")),
    tk.Label(janela, text="Europa", font=fonte_texto),
    tk.Button(janela, image=imagen_america, command=lambda: selecionar_continente("americas")),
    tk.Label(janela, text="Americas", font=fonte_texto),
    tk.Button(janela, image=imagen_asia, command=lambda: selecionar_continente("asiaticas")),
    tk.Label(janela, text="Ásia", font=fonte_texto),
    tk.Button(janela, image=imagen_africa, command=lambda: selecionar_continente("africa")),
    tk.Label(janela, text="África", font=fonte_texto),
    tk.Button(janela, image=imagen_oceania, command=lambda: selecionar_continente("oceania")),
    tk.Label(janela, text="Oceania", font=fonte_texto),
    tk.Button(janela, text="Todos", font=fonte_texto, command=lambda: selecionar_continente("todos"))
]

pergunta_label = tk.Label(janela, text="", wraplength=500, font=fonte_texto)
pergunta_label.pack(pady=10)
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

def mostrar_selecionar_continente():
    global nome
    nome = nome_entry.get()
    if not nome.strip():
        result_label.config(text="Por favor, insira seu nome.")
        return

    nome_label.pack_forget()
    nome_entry.pack_forget()
    iniciar_button.pack_forget()

    continente_label.pack(pady=10)

    # Calcular el punto medio de la lista de botones
    midpoint = len(continente_botoes) // 2

    # Dividir la lista de botones en dos partes
    top_botoes = continente_botoes[:midpoint]
    bottom_botoes = continente_botoes[midpoint:]

    # Empaquetar los botones superiores
    for i in range(0, len(top_botoes), 2):
        top_botoes[i].pack(side=tk.LEFT, padx=5)
        if i + 1 < len(top_botoes):  # Verificar si el índice está dentro del rango
            top_botoes[i+1].pack(side=tk.LEFT, padx=5)

    # Empaquetar los botones inferiores
    for i in range(0, len(bottom_botoes), 2):
        bottom_botoes[i].pack(side=tk.LEFT, padx=5)
        if i + 1 < len(bottom_botoes):  # Verificar si el índice está dentro del rango
            bottom_botoes[i+1].pack(side=tk.LEFT, padx=5)

def selecionar_continente(continente):
    global continente_selecionado
    continente_selecionado = continente


    continente_label.pack_forget()
    for botao in continente_botoes:
        botao.grid_forget()

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
    obter_pais()

def obter_pais():
    global resultado, capital_correta, perguntas_restantes, paises_ja_perguntados

    if perguntas_restantes == 0:
        finalizar_jogo()
        return

    pergunta = ''
    if continente_selecionado == "todos":
        pergunta = 'SELECT pais, capital FROM (SELECT pais, capital FROM europa UNION SELECT pais, capital FROM americas UNION SELECT pais, capital FROM asiaticas UNION SELECT pais, capital FROM africa UNION SELECT pais, capital FROM oceania)'
    else:
        pergunta = f'SELECT pais, capital FROM {continente_selecionado}'

    while True:
        resultado = cur.execute(pergunta).fetchall()
        random.shuffle(resultado)
        pais, capital_correta = resultado[0]
        if pais not in paises_ja_perguntados:
            paises_ja_perguntados.append(pais)
            break

    mostrar_pergunta(pais)

def mostrar_pergunta(pais):
    global capital_correta

    pergunta_label.config(text=f"Restam {perguntas_restantes} de {nroPerguntas}º perguntas.\n\nQual é a capital de {pais}?")
    opcoes = obter_opcoes(capital_correta)

    for i, opcao in enumerate(opcoes):
        botoes_opcoes[i].config(text=opcao)

def verificar_resposta(index):
    global pontos_totais, perguntas_restantes

    resposta_ut = botoes_opcoes[index].cget('text')

    if resposta_ut == capital_correta:
        pontos_totais += 100
        result_label.config(text=f"Muito bom {nome}! Resposta correta!\nVocê ganhou 100 pontos.\nTotal de pontos: {pontos_totais}")
    else:
        result_label.config(text=f"Resposta incorreta.\nA resposta correta é: {capital_correta}.\nTotal de pontos: {pontos_totais}")

    perguntas_restantes -= 1
    if perguntas_restantes > 0:
        obter_pais()
    else:
        finalizar_jogo()

def obter_opcoes(capital_correta):
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
    global nome, nroPerguntas, pontos_totais, perguntas_restantes, paises_ja_perguntados, continente_selecionado

    nome = ""
    nroPerguntas = 0
    pontos_totais = 0
    perguntas_restantes = 0
    paises_ja_perguntados = []
    continente_selecionado = ""

    pergunta_label.config(text="")
    for botao in botoes_opcoes:
        botao.pack_forget()
    result_label.config(text="")

    bemvindo_label.pack(pady=20)
    jogar_button.pack(pady=20)
    botao_jogar_novamente.pack_forget()

# Iniciar el loop principal de la GUI
janela.mainloop()

# Cerrar la conexión con la base de datos
con.close()
