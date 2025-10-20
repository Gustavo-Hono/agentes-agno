from db import connect, close

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
        
def hallutination_checks(user_id:int, question:str, answer:str, veredict:str):
    try:
        conexao = connect()
        cursor = conexao.cursor()
        cmd = "INSERT INTO hallucination_checks(user_id, question, answer, veredict) VALUES (%s, %s, %s, %s)"
        values = (user_id, question, answer, veredict)
        cursor.execute(cmd, values)
        conexao.commit()
        print("Insert funcionou")
        close(conexao, cursor)
    except Exception as e:
        print("Deu errado, \n {e}", e)
        conexao.rollback()
        close(conexao, cursor)

def select():
    cmd = "SELECT * FROM users"
    conexao = connect()
    cursor = conexao.cursor()
    cursor.execute(cmd)
    users = cursor.fetchall()
    close(conexao, cursor)
    for linha in users:
        print(linha)
    return users
        
def select_by_name(name: str):
    conexao = connect()
    cursor = conexao.cursor()
    name = name.capitalize()
    print("Chamado")
    cmd = "SELECT * FROM users WHERE name = %s"
    values = (name,)
    cursor.execute(cmd, values)
    users = cursor.fetchone()
    print(users)
    close(conexao, cursor)
    return users

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


