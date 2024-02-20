import tkinter as tk
from tkcalendar import Calendar

def visualizar_calendario():
    root = tk.Tk()
    root.title("Calendário")

    cal = Calendar(root, selectmode="day", year=2022, month=1, day=1)
    cal.pack(pady=20)

    def ao_clicar_na_data():
        data_selecionada = cal.selection_get()
        print(f"Data selecionada: {data_selecionada}")

    btn_selecionar_data = tk.Button(root, text="Selecionar Data", command=ao_clicar_na_data)
    btn_selecionar_data.pack(pady=10)

    root.mainloop()

# Se você quiser que a função seja executada quando o arquivo é executado diretamente
if __name__ == "__main__":
    visualizar_calendario()
