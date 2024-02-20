import tkinter as tk
from tkinter import ttk, Text, messagebox
from tkcalendar import DateEntry
import pygame
from cronometro import CronogramaEstudos  # Importe a classe Cronometro
from database import criar_tabela, adicionar_evento, obter_tarefas_do_dia
from database import salvar_evento  # Corrija a importação

# Inicializar o Pygame
pygame.init()

# Variáveis globais
entry_titulo = None
entry_descricao = None
entry_prioridade = None
entry_notas = None
calendario_widget = None  # Variável global para o widget de calendário
cronometro = None  # Remova a instância de Cronometro

# Criação da tabela no banco de dados
criar_tabela()

#===============================
# Adicionar Eventos na Agenda
#===============================

def adicionar_evento():
    titulo = entry_titulo.get()
    descricao = entry_descricao.get()
    prioridade = entry_prioridade.get()
    notas = entry_notas.get("1.0", tk.END).strip()
    data = calendario_widget.get_date()

    if not titulo or not data:
        messagebox.showwarning("Campos Vazios", "Por favor, preencha pelo menos o título e a data.")
        return

    salvar_evento(titulo, descricao, data, prioridade, notas)  # Corrija a chamada da função

    entry_titulo.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_prioridade.delete(0, tk.END)
    entry_notas.delete("1.0", tk.END)

    messagebox.showinfo("Evento Adicionado", "O evento foi adicionado com sucesso.")

#===============================
#       Abrir Calendário
#===============================
def abrir_calendario(root):
    global calendario_widget

    def exibir_tarefas_do_dia(data_selecionada, janela_calendario):
        tarefas_do_dia = obter_tarefas_do_dia(data_selecionada)

        if not tarefas_do_dia:
            messagebox.showinfo("Nenhuma Atividade", "Nenhuma atividade agendada para esta data.")
        else:
            messagebox.showinfo("Tarefas do Dia", "\n".join(tarefas_do_dia))

        fechar_calendario(janela_calendario)

    def fechar_calendario(janela_calendario):
        janela_calendario.destroy()

    janela_calendario = tk.Toplevel(root)
    janela_calendario.title("Calendário")

    calendario_widget = DateEntry(janela_calendario, width=12, background='darkblue', foreground='white', borderwidth=2)
    calendario_widget.pack(padx=10, pady=5)

    btn_exibir_tarefas = ttk.Button(janela_calendario, text="Exibir Tarefas do Dia", command=lambda: exibir_tarefas_do_dia(calendario_widget.get_date(), janela_calendario))
    btn_exibir_tarefas.pack(pady=10)

    btn_fechar_calendario = ttk.Button(janela_calendario, text="Fechar Calendário", command=lambda: fechar_calendario(janela_calendario))
    btn_fechar_calendario.pack(pady=10)

#=========================
#       Cronometro
#=========================
def iniciar_cronometro():
    global cronometro

    # Verificar se uma música foi selecionada antes de iniciar o cronômetro
    if not pygame.mixer.music.get_busy():
        messagebox.showinfo("Escolha uma Música", "Por favor, escolha uma música antes de iniciar o cronômetro.")
        return

    btn_abrir_cronometro = ttk.Button(root, text="Abrir Cronômetro", command=criar_cronometro)
    btn_abrir_cronometro.grid(row=7, column=0, columnspan=2, pady=10)

    btn_iniciar_cronometro = ttk.Button(root, text="Iniciar Cronômetro", command=iniciar_cronometro)
    btn_iniciar_cronometro.grid(row=8, column=0, columnspan=2, pady=10)
    cronometro.iniciar_cronometro()

#==============================
#      Função Principal
#==============================

def main():
    global entry_titulo, entry_descricao, entry_prioridade, entry_notas, calendario_widget, cronometro

    # Interface gráfica principal
    root = tk.Tk()
    root.title("Agenda Pessoal - Joshebrk21")

    label_titulo = ttk.Label(root, text="Título:")
    label_titulo.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

    entry_titulo = ttk.Entry(root)
    entry_titulo.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

    label_descricao = ttk.Label(root, text="Descrição:")
    label_descricao.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

    entry_descricao = ttk.Entry(root)
    entry_descricao.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

    label_data = ttk.Label(root, text="Data:")
    label_data.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)

    calendario_widget = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
    calendario_widget.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

    label_prioridade = ttk.Label(root, text="Prioridade:")
    label_prioridade.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)

    entry_prioridade = ttk.Entry(root)
    entry_prioridade.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

    label_notas = ttk.Label(root, text="Notas:")
    label_notas.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)

    entry_notas = tk.Text(root, height=5, width=30)
    entry_notas.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

    btn_adicionar = ttk.Button(root, text="Adicionar Evento", command=adicionar_evento)
    btn_adicionar.grid(row=5, column=0, columnspan=2, pady=10)

    btn_abrir_calendario = ttk.Button(root, text="Abrir Calendário", command=lambda: abrir_calendario(root))
    btn_abrir_calendario.grid(row=6, column=0, columnspan=2, pady=10)

    # Lista para armazenar a referência ao cronômetro
    cronometro_ref = [None]

    # Função para criar instância de Cronometro
    def criar_cronometro():
        global cronometro
        cronometro_ref[0] = CronogramaEstudos(root)
        cronometro = cronometro_ref[0]

    btn_abrir_cronometro = ttk.Button(root, text="Abrir Cronômetro", command=criar_cronometro)
    btn_abrir_cronometro.grid(row=7, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
