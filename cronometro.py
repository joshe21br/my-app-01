import os
import tkinter as tk
from tkinter import filedialog, messagebox, font
from datetime import timedelta, datetime
import pygame

class CronogramaEstudos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cronômetro")
        self.geometry("300x200")

        # Configuração de fonte personalizada
        custom_font = font.Font(family="Helvetica", size=16)

        # Adicione a definição da variável cor_normal
        self.cor_normal = self.cget('bg')

        self.label_tempo = tk.Label(self, text="Tempo restante : 25:00", font=custom_font)
        self.label_tempo.grid(row=0, column=0, pady=10)

        # Inicialize as variáveis necessárias
        self.tempo_atual = timedelta(minutes=60)
        self.tempo_pausa = timedelta(minutes=5)
        self.tempo_alerta = timedelta(seconds=60)
        self.alerta_ativo = False

        self.label_tempo = tk.Label(self, text="Tempo restante : 25:00", font=custom_font)
        self.label_tempo.grid(row=0, column=0, pady=10)
         # Adicione esta linha para corrigir o problema com o widget de label
        self.label_tempo.update_idletasks()

        self.em_pausa = False  # Adicione esta linha para inicializar o atributo em_pausa

        self.botao_iniciar = tk.Button(self, text="Iniciar", command=self.iniciar_cronometro)
        self.botao_iniciar.grid(row=1, column=0, pady=5)

        self.botao_pausar = tk.Button(self, text="Pausar", state=tk.DISABLED, command=self.pausar_cronometro)
        self.botao_pausar.grid(row=2, column=0, pady=5)

        self.botao_config = tk.Button(self, text="Configurações", command=self.abrir_configuracoes)
        self.botao_config.grid(row=3, column=0, pady=5)

        self.botao_historico = tk.Button(self, text="Histórico", command=self.mostrar_historico)
        self.botao_historico.grid(row=4, column=0, pady=5)

        # Adicionando informações do desenvolvedor e da empresa
        self.label_info_desenvolvedor = tk.Label(self, text="Desenvolvedor: Joshebrk21")
        self.label_info_desenvolvedor.grid(row=5, column=0, pady=5)

        self.label_info_telefone = tk.Label(self, text="Telefone: 85992853916")
        self.label_info_telefone.grid(row=6, column=0, pady=5)

        self.label_info_email = tk.Label(self, text=" Email: josuesouzadasilva@gmail.com")
        self.label_info_email.grid(row=7, column=0, pady=5)

        self.label_info_empresa = tk.Label(self, text="Empresa: I-Tech")
        self.label_info_empresa.grid(row=8, column=0, pady=5)

        # Carregar configurações padrão
        self.carregar_configuracoes()



        # Criar ou carregar arquivo de histórico
        self.arquivo_historico = "historico.txt"
        if not os.path.exists(self.arquivo_historico):
            with open(self.arquivo_historico, "w") as f:
                f.write("Data,Tempo de Estudo\n")

        self.janela_config = None  # Adicione a variável janela_config aqui

    def iniciar_cronometro(self):
        if hasattr(self, 'musica_selecionada') and self.musica_selecionada:
            self.botao_iniciar.config(state=tk.DISABLED)
            self.botao_pausar.config(state=tk.NORMAL)
            pygame.mixer.music.play(-1)
            self.inicio_sessao = datetime.now()
            self.atualizar_cronometro()
        else:
            messagebox.showinfo("Escolha uma Música", "Por favor, escolha uma música antes de iniciar o cronômetro.")

    def pausar_cronometro(self):
        self.botao_iniciar.config(state=tk.NORMAL)
        self.botao_pausar.config(state=tk.DISABLED)
        pygame.mixer.music.stop()
        self.em_pausa = not self.em_pausa
        if not self.em_pausa:
            self.registrar_historico()

    def atualizar_cronometro(self):
        if self.janela_config and not self.janela_config.winfo_exists():
            # A janela de configurações não existe mais, encerrar a atualização
            return

        if not self.em_pausa:
            self.tempo_atual -= timedelta(seconds=1)

        if self.tempo_atual.total_seconds() <= 0:
            # Tempo esgotado, parar o cronômetro
            self.em_pausa = True
            self.tempo_atual = timedelta(seconds=0)

        self.label_tempo.config(text=self.formatar_tempo(self.tempo_atual))
        self.master.after(1000, self.atualizar_cronometro)

    def formatar_tempo(self, tempo):
        horas, minutos, segundos = str(tempo).split(":")
        return f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}"

    def piscar_tela(self):
        self.master.configure(bg='red')
        self.master.after(500, lambda: self.master.configure(bg=self.cor_normal))
        self.master.after(1000, lambda: self.master.configure(bg='red'))
        self.master.after(1500, lambda: self.master.configure(bg=self.cor_normal))

    def abrir_configuracoes(self):
        janela_config = tk.Toplevel(self.master)
        janela_config.title("Configurações")

        tk.Label(janela_config, text="Tempo de Estudo (minutos):").pack()
        self.entrada_tempo_estudo = tk.Entry(janela_config)
        self.entrada_tempo_estudo.insert(0, str(self.tempo_estudo.seconds // 60) if hasattr(self, 'tempo_estudo') else "")
        self.entrada_tempo_estudo.pack()

        tk.Label(janela_config, text="Tempo de Pausa (minutos):").pack()
        self.entrada_tempo_pausa = tk.Entry(janela_config)
        self.entrada_tempo_pausa.insert(0, str(self.tempo_pausa.seconds // 60) if hasattr(self, 'tempo_pausa') else "")
        self.entrada_tempo_pausa.pack()

        tk.Label(janela_config, text="Tempo de Alerta (segundos):").pack()
        self.entrada_tempo_alerta = tk.Entry(janela_config)
        self.entrada_tempo_alerta.insert(0, str(self.tempo_alerta.seconds) if hasattr(self, 'tempo_alerta') else "")
        self.entrada_tempo_alerta.pack()

        tk.Label(janela_config, text="Música de Fundo:").pack()
        self.botao_selecionar_musica = tk.Button(janela_config, text="Selecionar Música", command=self.selecionar_musica)
        self.botao_selecionar_musica.pack()

        tk.Button(janela_config, text="Salvar", command=self.salvar_configuracoes).pack()

    def selecionar_musica(self):
        arquivo_musica = filedialog.askopenfilename(filetypes=[("Arquivos MP3", "*.mp3")])
        if arquivo_musica:
            pygame.mixer.music.load(arquivo_musica)
            self.musica_selecionada = True

    def salvar_configuracoes(self):
        try:
            tempo_estudo = int(self.entrada_tempo_estudo.get())
            tempo_pausa = int(self.entrada_tempo_pausa.get())
            tempo_alerta = int(self.entrada_tempo_alerta.get())

            self.tempo_estudo = timedelta(minutes=tempo_estudo)
            self.tempo_pausa = timedelta(minutes=tempo_pausa)
            self.tempo_alerta = timedelta(seconds=tempo_alerta)

            # Salvar configurações em um arquivo ou banco de dados, se necessário

            # Fechar a janela de configurações
            if self.janela_config:
                self.janela_config.destroy()
            self.master.update_idletasks()
            self.master.update()
            self.master.focus_force()
            self.master.configure(bg=self.cor_normal)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

    def carregar_configuracoes(self):
        # Carregar configurações de um arquivo ou banco de dados, se necessário
        # Configurações padrão já foram definidas no início do programa
        pass

    def registrar_historico(self):
        fim_sessao = datetime.now()
        tempo_sessao = fim_sessao - self.inicio_sessao
        with open(self.arquivo_historico, "a") as f:
            f.write(f"{fim_sessao},{tempo_sessao}\n")

    def mostrar_historico(self):
        try:
            with open(self.arquivo_historico, "r") as f:
                historico = f.read()
            tk.messagebox.showinfo("Histórico de Estudos", historico)
        except FileNotFoundError:
            tk.messagebox.showinfo("Histórico de Estudos", "Nenhum histórico disponível.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CronogramaEstudos(root)
    root.mainloop()
