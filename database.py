import sqlite3
from datetime import datetime

def conectar_banco():
    # Função para conectar ao banco de dados
    conexao = sqlite3.connect('agenda.db')
    return conexao

def criar_tabela():
    # Criação da tabela se ela não existir
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            data TEXT NOT NULL,
            prioridade INTEGER,
            notas TEXT
        )
    ''')

    conn.commit()
    conn.close()

def adicionar_evento(titulo, descricao, data, prioridade, notas):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO eventos (titulo, descricao, data, prioridade, notas)
        VALUES (?, ?, ?, ?, ?)
    ''', (titulo, descricao, data, prioridade, notas))

    conn.commit()
    conn.close()

def salvar_evento(titulo, descricao, data, prioridade, notas):
    # Função para salvar o evento no banco de dados
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Inserir os dados na tabela eventos
    cursor.execute('''
        INSERT INTO eventos (titulo, descricao, data, prioridade, notas)
        VALUES (?, ?, ?, ?, ?)
    ''', (titulo, descricao, data, prioridade, notas))

    conexao.commit()
    conexao.close()

def obter_tarefas_do_dia(data):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT titulo FROM eventos WHERE data = ?
    ''', (data,))

    tarefas_do_dia = [row[0] for row in cursor.fetchall()]   

    conn.close()

    return tarefas_do_dia
