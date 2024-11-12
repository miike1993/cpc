import tkinter as tk
from tkinter import messagebox
import csv
import os

# Caminho da pasta Documentos do usuário
documents_path = os.path.expanduser("~/Documents")
csv_file_path = os.path.join(documents_path, "cadastro_criancas.csv")

# Função para verificar o login
def check_login():
    if username_entry.get() == "admin" and password_entry.get() == "admin":
        show_home()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

# Função para exibir a tela inicial
def show_home():
    login_frame.pack_forget()
    home_frame.pack()

# Função para exibir a tela de cadastro
def show_register():
    home_frame.pack_forget()
    register_frame.pack()

# Função para voltar para a tela inicial
def go_home():
    register_frame.pack_forget()
    home_frame.pack()

# Função para salvar dados da criança
def save_child_data():
    data = [search_entry.get()] + [entry.get() for entry in entries.values()]
    file_exists = os.path.isfile(csv_file_path)
    with open(csv_file_path, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Nome", "Idade", "Restrição Alimentar", "Medicamentos", "Responsável", "Contato do Responsável", "Veículo de Transporte"])
        writer.writerow(data)
    messagebox.showinfo("Sucesso", "Dados da criança cadastrados com sucesso.")
    clear_form()

# Função para limpar o formulário
def clear_form():
    search_entry.delete(0, tk.END)
    for entry in entries.values():
        entry.delete(0, tk.END)

# Função para carregar dados da criança no formulário
def load_child_data():
    search_name = search_entry.get()
    if not os.path.isfile(csv_file_path):
        messagebox.showerror("Erro", "Nenhum cadastro encontrado.")
        return
    
    with open(csv_file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Pula o cabeçalho
        for row in reader:
            if row[0] == search_name:
                for i, entry in enumerate(entries.values()):
                    entry.delete(0, tk.END)
                    entry.insert(0, row[i])
                return
        messagebox.showinfo("Não encontrado", "Cadastro não encontrado.")

# Configuração da janela principal
root = tk.Tk()
root.title("Sistema de Cadastro de Crianças")
root.geometry("600x400")

# Frame de Login
login_frame = tk.Frame(root)
tk.Label(login_frame, text="Usuário").pack()
username_entry = tk.Entry(login_frame)
username_entry.pack()

tk.Label(login_frame, text="Senha").pack()
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack()

login_button = tk.Button(login_frame, text="Entrar", command=check_login)
login_button.pack()
login_frame.pack()

# Frame Home
home_frame = tk.Frame(root)
tk.Label(home_frame, text="Bem-vindo ao Sistema de Cadastro de Crianças!").pack(pady=10)
register_button = tk.Button(home_frame, text="Cadastrar Criança", command=show_register)
register_button.pack()
home_frame.pack_forget()

# Frame de Cadastro
register_frame = tk.Frame(root)

# Campo de pesquisa
tk.Label(register_frame, text="Pesquisar Criança").grid(row=0, column=0, padx=10, pady=5, sticky="w")
search_entry = tk.Entry(register_frame, width=50)
search_entry.grid(row=0, column=1, padx=10, pady=5)
search_button = tk.Button(register_frame, text="Pesquisar", command=load_child_data)
search_button.grid(row=0, column=2, padx=10, pady=5)

# Campos de entrada
labels = ["Nome da Criança", "Idade", "Restrição Alimentar", "Medicamentos", "Responsável Autorizado", "Contato do Responsável", "Veículo de Transporte"]
entries = {}

for i, label_text in enumerate(labels):
    tk.Label(register_frame, text=label_text).grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
    entry = tk.Entry(register_frame, width=50)
    entry.grid(row=i+1, column=1, padx=10, pady=5)
    entries[label_text] = entry

# Botões de ação
save_button = tk.Button(register_frame, text="Salvar", command=save_child_data)
save_button.grid(row=len(labels) + 1, column=1, padx=10, pady=20, sticky="w")

cancel_button = tk.Button(register_frame, text="Cancelar", command=clear_form)
cancel_button.grid(row=len(labels) + 1, column=1, padx=10, pady=20, sticky="e")

edit_button = tk.Button(register_frame, text="Editar", command=load_child_data)
edit_button.grid(row=len(labels) + 2, column=1, padx=10, pady=5, sticky="w")

back_button = tk.Button(register_frame, text="Voltar", command=go_home)
back_button.grid(row=len(labels) + 2, column=1, padx=10, pady=5, sticky="e")

register_frame.pack_forget()

root.mainloop()
