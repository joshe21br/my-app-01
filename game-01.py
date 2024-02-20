#======================================
#           Jogo Da Velha
# Criador : Josué Souza da Silva
# Email : josuesouzadasilva@gmail.com
# Github : 
# Data : 18/02/2024
#======================================

import tkinter as tk
from tkinter import messagebox

class JogoDaVelha:
    def __init__(self):
        # Inicializa a janela principal do jogo
        self.janela = tk.Tk()
        self.janela.title("Jogo da Velha")

        # Inicializa as variáveis do jogo
        self.turno = "X"
        self.tabuleiro = [["" for _ in range(3)] for _ in range(3)]

        # Cria os botões para representar o tabuleiro
        self.botoes = [[tk.Button(self.janela, text="", width=10, height=3,
                                  command=lambda row=row, col=col: self.clique(row, col))
                        for col in range(3)] for row in range(3)]

        # Posiciona os botões na interface gráfica
        for row in range(3):
            for col in range(3):
                self.botoes[row][col].grid(row=row, column=col)

        # Adiciona uma barra de menu
        menu_bar = tk.Menu(self.janela)
        self.janela.config(menu=menu_bar)

        # Opções no menu
        jogo_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Jogo", menu=jogo_menu)
        jogo_menu.add_command(label="Novo Jogo", command=self.novo_jogo)
        jogo_menu.add_command(label="Encerrar Jogo", command=self.janela.quit)

    def clique(self, row, col):
        # Função chamada quando um botão é clicado
        if self.tabuleiro[row][col] == "" and not self.verificar_vencedor():
            # Atualiza o tabuleiro e a interface gráfica
            self.tabuleiro[row][col] = self.turno
            self.botoes[row][col].config(text=self.turno)

            # Verifica se há um vencedor ou empate
            if self.verificar_vencedor():
                messagebox.showinfo("Fim do Jogo", f"O jogador {self.turno} venceu!")
            elif all(self.tabuleiro[i][j] != "" for i in range(3) for j in range(3)):
                messagebox.showinfo("Fim do Jogo", "Empate!")
            else:
                # Troca o turno
                self.turno = "O" if self.turno == "X" else "X"

    def verificar_vencedor(self):
        # Verifica vitória nas linhas, colunas e diagonais
        for i in range(3):
            if self.tabuleiro[i][0] == self.tabuleiro[i][1] == self.tabuleiro[i][2] != "":
                return True  # Linhas
            if self.tabuleiro[0][i] == self.tabuleiro[1][i] == self.tabuleiro[2][i] != "":
                return True  # Colunas
        if self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] != "":
            return True  # Diagonal principal
        if self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] != "":
            return True  # Diagonal secundária
        return False

    def novo_jogo(self):
        # Limpa o tabuleiro e reinicia o jogo
        for row in range(3):
            for col in range(3):
                self.tabuleiro[row][col] = ""
                self.botoes[row][col].config(text="")
        self.turno = "X"
        messagebox.showinfo("Novo Jogo", "Um novo jogo foi iniciado!")

    def iniciar(self):
        # Inicia o loop principal da interface gráfica
        self.janela.mainloop()

# Instancia o jogo e inicia a interface gráfica
jogo = JogoDaVelha()
jogo.iniciar()

