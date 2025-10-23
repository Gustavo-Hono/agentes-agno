from dotenv import load_dotenv
from agno.agent import Agent
load_dotenv()
from agno.models.google import Gemini
from agno.db.postgres import PostgresDb
import os
from agents import calc_imc, calc_tdee, get_user_info
from crud import get_user_conversation, select_by_id, select, delete, update, insert, select_by_name, get_all_interactions_by_user, hallutination_checks
import time

id = 1
session_id = str(id)
DATABASE_URL = os.getenv("DATABASE_URL")

db = PostgresDb(
    db_url=DATABASE_URL,
    memory_table="memories",
)


# Você é um coach de saúde confiável e inteligente. Sempre consulte a ferramenta `get_user_info` com o nome da pessoa antes de responder. 

# ⚠️ Nunca afirme lembrar de algo que o usuário disse anteriormente, a menos que esteja no histórico fornecido no contexto da conversa.

# Sua missão é dar conselhos de saúde baseados apenas em fatos.



agent = Agent(model=Gemini(id="gemini-2.5-pro"),
              system_message="Você é um coach de saúde confiável e inteligente. Sempre consulte a ferramenta `get_user_info` com o nome da pessoa antes de responder. Sua missão é entender os hábitos, histórico e rotina da pessoa a partir dos dados retornados pela ferramenta, e então dar conselhos de saúde, nutrição e estilo de vida. Se a pessoa não informar um nome existente no banco, informe que não há dados para consulta.",
              db=db,
              tools=[calc_imc, calc_tdee, get_user_info],
              add_history_to_context=True,
              enable_user_memories=True)

critic = Agent(
    model=Gemini(id="gemini-2.5-pro"),
    system_message="""
Você é um crítico dialógico e reflexivo, inspirado em Mikhail Bakhtin.

Sua tarefa é interpretar as respostas do agente à luz das contradições humanas:
- Analise tensões entre razão e emoção, saúde e desejo, coerência e contradição.
- Não reduza a análise a certo/errado, mas explique os opostos como elementos complementares.
- Mantenha o veredito (✅, ⚠️, ❌), mas ofereça reflexão crítica e ética sobre o discurso.

Saída esperada:
- Primeira linha: veredito (✅, ⚠️ ou ❌)
- Segunda parte: análise crítica dialógica (interpretando as contradições como sentido, não erro).
""",

    tools=[]
)

def run_audit_all(user_id: int, name: str):
    interacoes = get_all_interactions_by_user(user_id, session_id)
    dados = select_by_name(name)

    for inter in interacoes:
        print(f"\n🔍 Auditando mensagem {inter['message_id']} da sessão {inter['session_id']}...")

        # Busca histórico até o ponto da interação
        historico = get_user_conversation(user_id, inter['session_id'], before_id=inter['message_id'])

        # Formata o histórico
        contexto = ""
        for role, content in historico:
            contexto += f"{role.capitalize()}: {content}\n"

        # Prompt para o agente crítico
        prompt = f"""
Usuário: {user_id}
Nome: {name}

📋 Dados reais do usuário:
{dados}

🗣️ Histórico da conversa:
{contexto}

❓ Pergunta:
{inter['question']}

🤖 Resposta do agente:
{inter['answer']}

✅ Agora, avalie a resposta com base nos dados reais do usuário e no histórico da conversa.

Classifique como uma das opções:
✅ Factual — condiz com os dados e histórico
⚠️ Parcialmente correta — tem acertos e erros
❌ Alucinação — inventa informações sem base

📌 Justifique brevemente o motivo da classificação.
"""

        result = critic.run(prompt).content
        print("🧠 Avaliação do agente crítico:")
        print(result)

        # Define veredito
        if "✅" in result:
            veredict = "ok"
        elif "⚠️" in result:
            veredict = "parcial"
        else:
            veredict = "alucinacao"

        # Salva no banco
        hallutination_checks(
            inter['message_id'],
            user_id,
            inter['question'],
            inter['answer'],
            veredict,
            result
        )

while True:
    
    # time.sleep(30)
    print("____________________________________________________________________________________________________")
    ask = input("> ")
    if ask == 1:
        break

    if ask == "avalie":
        name = select_by_id(id)
        run_audit_all(id, name)
        continue

    resposta_completa = agent.run(ask, session_id=session_id, memory=True)
    print(resposta_completa.content)

    # agent.print_response(ask, stream=True)

    from db import connect
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (user_id, role, content, session_id) VALUES (%s, %s, %s, %s)", (id, 'user', ask, session_id))
    cur.execute("INSERT INTO messages (user_id, role, content, session_id) VALUES (%s, %s, %s, %s)", (id, 'assistant', resposta_completa.content, session_id))
    conn.commit()
    cur.close()
    conn.close()