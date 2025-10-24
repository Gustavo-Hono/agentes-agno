import json
from db import connect, close

# SELECTS

def get_all_interactions_by_user(user_id: int, session_id: str):
    conexao = connect()
    cursor = conexao.cursor()
    cmd = """
        SELECT id, session_id, role, content, created_at
        FROM messages
        WHERE user_id = %s AND session_id = %s
        ORDER BY created_at DESC
        LIMIT 6
    """
    cursor.execute(cmd, (user_id, session_id))
    rows = cursor.fetchall()
    close(conexao, cursor)
    pares = []
    for i in range(len(rows) - 1):
        atual = rows[i]
        proximo = rows[i + 1]

        if atual[2] == 'user' and proximo[2] == 'assistant' and atual[1] == proximo[1]:
            pares.append({
                "message_id": proximo[0],
                "session_id": atual[1],
                "question": atual[3],
                "answer": proximo[3],
                "created_at": proximo[4]
            })
    print("Resultado dos pares:")
    print(pares)
    return pares



def get_user_conversation(user_id: int, session_id:str, before_id:int):
    conexao = connect()
    cursor = conexao.cursor()
    cmd = """
    SELECT role, content 
    FROM messages 
    WHERE user_id = %s AND session_id =%s
    """
    if before_id:
        cmd += " AND id <= %s"
        cursor.execute(cmd + " ORDER BY created_at ASC", (user_id, session_id, before_id))
    else:
        cursor.execute(cmd + " ORDER BY created_at ASC", (user_id, session_id))

    historico = cursor.fetchall()
    print("Chamando o user conversation")
    print(historico)
    close(conexao, cursor)
    return historico


def select():
    cmd = "SELECT * FROM users LIMIT 1"
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute(cmd)
    users = cursor.fetchone()
    close(conexao, cursor)
    for linha in users:
        print(linha)
    return users

def select_by_id(id:int):
    conexao = connect()
    cursor = conexao.cursor()
    cmd = "SELECT * FROM users WHERE id=%s"
    value = (id,)
    cursor.execute(cmd, value)
    user = cursor.fetchone()
    close(conexao, cursor)
    if user:
        print(user)
        name = user[1]
        return name
    else:
        print("Usuário não encontrado.")
        return None
        
def select_by_name(name: str):
    conexao = connect()
    cursor = conexao.cursor()
    name = name.capitalize()
    print("Chamado")
    cmd = "SELECT * FROM users WHERE name = %s"
    values = (name,)
    cursor.execute(cmd, values)
    users = cursor.fetchone()
    close(conexao, cursor)
    return users

# INSERTS
def insert(name: str, idade: int):
    try:
        conexao = connect()
        cursor = conexao.cursor()
        cmd_insert = "INSERT INTO users(name, idade) VALUES(%s, %s)"
        values = (name, idade)
        cursor.execute(cmd_insert, values)
        conexao.commit()
        print("Deu certo")
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao inserir: {e}")



def hallutination_checks(message_id: int, user_id: int, question: str, answer: str, veredict: dict, justification: str):
    try:
        conexao = connect()
        cursor = conexao.cursor()
        cmd = """
        INSERT INTO hallucination_checks(message_id, user_id, question, answer, veredict, justification)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (message_id, user_id, question, answer, json.dumps(veredict), justification)
        cursor.execute(cmd, values)
        conexao.commit()
        print("Salvo com sucesso no banco.")
    except Exception as e:
        print("Erro ao salvar verificação de alucinação:", e)
        conexao.rollback()
    finally:
        close(conexao, cursor)



# Delete

def delete(idade: int):
    try:
        conexao = connect()
        cursor = conexao.cursor()
        cmd = "DELETE FROM users WHERE idade = %s"
        values = (idade,)
        cursor.execute(cmd, values)
        conexao.commit()
        print("Deletado com sucesso")
        close(conexao, cursor)
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao deletar: {e}")
        close(conexao, cursor)

# Update

def update(name: str, idade: int, name_target: str):
    try:
        conexao = connect()
        cursor = conexao.cursor()
        cmd = "UPDATE users SET name = %s, idade = %s WHERE name = %s RETURNING *"
        values = (name, idade, name_target)
        cursor.execute(cmd, values)
        updated = cursor.fetchall()
        conexao.commit()
        if updated:
            print("Atualizado:", updated)
        else:
            print("Nenhuma linha correspondente ao WHERE")
            close(conexao, cursor)
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao atualizar: {e}")
        close(conexao, cursor)

