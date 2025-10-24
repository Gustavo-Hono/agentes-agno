from dotenv import load_dotenv
from agno.agent import Agent
import json
load_dotenv()
from agno.models.google import Gemini
from agno.db.postgres import PostgresDb
import os
from tools import calc_imc, calc_tdee, get_user_info
from crud import get_user_conversation, select_by_id, select, delete, update, insert, select_by_name, get_all_interactions_by_user, hallutination_checks
import time

id = 7
session_id = str(id)
DATABASE_URL = os.getenv("DATABASE_URL")

db = PostgresDb(
    db_url=DATABASE_URL,
    memory_table="memories",
)





agent_saude = Agent(model=Gemini(id="gemini-2.0-flash-lite"),
              system_message="Você é um coach de saúde confiável e inteligente. Sempre consulte a ferramenta `get_user_info` com o nome da pessoa antes de responder.  ⚠️ Nunca afirme lembrar de algo que o usuário disse anteriormente, a menos que esteja no histórico fornecido no contexto da conversa. Sua missão é dar conselhos de saúde baseados apenas em fatos. ",
              db=db,
              tools=[calc_imc, calc_tdee, get_user_info],
              add_history_to_context=True,
              enable_user_memories=True)

critic = Agent(
    model=Gemini(id="gemini-2.0-flash-lite"),
    system_message="""
Você é um **agente crítico dialógico e ético**, inspirado em **Mikhail Bakhtin** e na visão integral do ser humano.

Sua missão é **avaliar as respostas do agente de saúde**, não como um juiz, mas como um **intérprete das vozes e contradições humanas**.

---

### 🧩 Diretrizes de linguagem dialógica paradoxal
- Trate **os opostos como complementares**: disciplina × prazer, controle × liberdade, biológico × espiritual.
- Evite simplificar: reconheça que **a verdade emerge do diálogo entre forças em tensão**.
- O erro pode revelar uma necessidade legítima; a coerência pode ocultar rigidez.
- Analise o discurso como uma **polifonia**: cada frase traz ecos de valores, crenças e contextos.

---

### 🧭 Contextos que você deve sempre considerar
Avalie como a resposta do agente se articula com a jornada integral do sujeito humano, incluindo:

1. **Biológico:** corpo, metabolismo, neurotransmissores, sono, alimentação, atividade física.
2. **Mental e psicológico-emocional:** estresse, ansiedade, regulação emocional, hábitos de pensamento.
3. **Social, espiritual e ambiental:** qualidade dos vínculos sociais; influência de ambientes não saudáveis (bebidas, drogas, excesso de games, redes sociais, pornografia, festas excessivas) versus práticas que fortalecem o sentido (oração, leitura meditativa, espiritualidade, frequência a missas ou comunidades).

Procure mostrar **como escolhas diárias constroem ou corroem a harmonia entre esses níveis**.

---

### 🧮 Saída estruturada
Sempre devolva a resposta **em JSON** com o seguinte formato:

{
  "status": "ok" | "parcial" | "alucinacao",
  "score": número entre 0 e 1,
  "critic_agent": "Gemini 2.5",
  "criteria": {
    "coerencia": número entre 0 e 1,
    "factualidade": número entre 0 e 1,
    "dialogicidade": número entre 0 e 1
  },
  "justificativas": {
  "coerencia": "explique aqui como chegou a essa nota",
  "factualidade": "explique aqui como chegou a essa nota",
  "dialogicidade": "explique aqui como chegou a essa nota"
},

  "reflexao": "análise crítica e dialógica sobre a resposta, explicando as tensões entre corpo, mente, emoção, sociedade e espiritualidade sem julgamentos morais."
}

Regras:
- A `score` deve ser a média dos três critérios.
- `status` = "ok" se a resposta for coerente e integral; "parcial" se for incompleta; "alucinacao" se distorcer dados ou ignorar o humano.
- O campo `reflexao` deve trazer uma leitura filosófica e empática, considerando **a jornada de vida** e **as contradições como sentido**, não como falha.
- Evite sermões: fale como um **professor que provoca reflexão**.

""",

    tools=[]
)

def run_audit_all(user_id: int, name: str):
    interacoes = get_all_interactions_by_user(user_id, session_id)
    dados = select_by_name(name)

    for inter in interacoes:
        print(f"\n🔍 Auditando mensagem {inter['message_id']} da sessão {inter['session_id']}...")

        # Histórico até o ponto da interação
        historico = get_user_conversation(user_id, inter['session_id'], before_id=inter['message_id'])
        contexto = "".join([f"{r.capitalize()}: {c}\n" for r, c in historico])

        # Prompt de auditoria
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

Avalie conforme suas instruções e devolva o JSON.
"""

        # Executa o crítico
        result = critic.run(prompt).content.strip()
        print("🧠 Saída bruta do crítico:")
        print(result)

        # Tenta interpretar o JSON retornado
        try:
            clean_result = result.strip()
            if clean_result.startswith("```"):
                clean_result = clean_result.strip("`")
                clean_result = clean_result.replace("json\n", "").replace("json", "")
            clean_result = clean_result.replace("```", "").strip()

            veredict_data = json.loads(clean_result)

            # Remove \n dentro da reflexão
            reflexao = veredict_data.get("reflexao", "")
            if isinstance(reflexao, str):
                reflexao = reflexao.replace("\\n", " ").replace("\n", " ").strip()
                veredict_data["reflexao"] = reflexao

            # ✅ Exibe resultado formatado e sinal visual
            status = veredict_data.get("status", "").lower()
            if status == "ok":
                simbolo = "✅"
            elif status == "parcial":
                simbolo = "⚠️"
            elif status == "alucinacao":
                simbolo = "❌"
            else:
                simbolo = "❓"

            criteria = veredict_data.get("criteria", {})
            print(f"\n{simbolo} Veredito: {status.upper()} — Score: {veredict_data.get('score', 0)}")
            print(f"   • Coerência: {criteria.get('coerencia', 0)}")
            print(f"   • Factualidade: {criteria.get('factualidade', 0)}")
            print(f"   • Dialogicidade: {criteria.get('dialogicidade', 0)}")
            print(f"\n🪞 Reflexão: {veredict_data.get('reflexao', '')}\n")

            # Exibe justificativas (se existirem)
            just = veredict_data.get("justificativas", {})
            if just:
                print("   🧩 Por quê:")
                print(f"     - Coerência: {just.get('coerencia', '')}")
                print(f"     - Factualidade: {just.get('factualidade', '')}")
                print(f"     - Dialogicidade: {just.get('dialogicidade', '')}")


        except json.JSONDecodeError:
            print("⚠️ O agente crítico não retornou JSON válido — salvando como texto.")
            veredict_data = {
                "status": "erro",
                "score": 0.0,
                "critic_agent": "Gemini 2.5",
                "criteria": {"coerencia": 0.0, "factualidade": 0.0, "dialogicidade": 0.0},
                "reflexao": result
            }


        hallutination_checks(
            message_id=inter['message_id'],
            user_id=user_id,
            question=inter['question'],
            answer=inter['answer'],
            veredict=veredict_data,
            justification=veredict_data.get("reflexao", "")
        )



def run_audit_full_session(user_id: int, name: str):
    print(f"\n🔎 Avaliando coerência geral da sessão do usuário {user_id} ({name})...")

    # Busca histórico completo da sessão
    historico = get_user_conversation(user_id, session_id=session_id, before_id=None)

    # Monta o contexto como diálogo completo
    contexto = ""
    for role, content in historico:
        contexto += f"{role.capitalize()}: {content}\n"

    # Dados reais do usuário
    dados = select_by_name(name)

    # Prompt único para avaliação global
    prompt = f"""
Usuário: {user_id}
Nome: {name}

📋 Dados reais do usuário:
{dados}

🗣️ Conversa completa:
{contexto}

✅ Avalie a coerência global do agente de saúde ao longo de toda a conversa.
- Identifique contradições, exageros, ou conselhos sem base factual.
- Considere o equilíbrio entre razão e emoção, biologia e espiritualidade.
- Aponte se houve alguma alucinação ou discurso incoerente.

Saída esperada:
JSON com os campos:
{{
  "status": "ok" | "parcial" | "alucinacao",
  "score": número entre 0 e 1,
  "critic_agent": "Gemini 2.5",
  "criteria": {{
    "coerencia": número entre 0 e 1,
    "factualidade": número entre 0 e 1,
    "dialogicidade": número entre 0 e 1
  }},
  "reflexao": "Síntese interpretativa sobre o discurso integral do agente."
}}
"""

    result = critic.run(prompt).content

    # --- LIMPEZA E PARSE JSON ---
    try:
        clean_result = result.strip()
        if clean_result.startswith("```"):
            clean_result = clean_result.strip("`").replace("json", "").replace("```", "")
        clean_result = clean_result.strip()
        veredict_data = json.loads(clean_result)
    except Exception:
        print("⚠️ Resultado inválido, salvando texto bruto.")
        veredict_data = {"status": "erro", "reflexao": result}

    # --- EXIBIÇÃO ---
    simbolo = {
        "ok": "✅",
        "parcial": "⚠️",
        "alucinacao": "❌"
    }.get(veredict_data.get("status", ""), "❓")

    print(f"\n{simbolo} Veredito global: {veredict_data.get('status', '').upper()} — Score: {veredict_data.get('score', 0)}")
    print(json.dumps(veredict_data, indent=2, ensure_ascii=False))

    hallutination_checks(
        message_id=None,
        user_id=user_id,
        question="Avaliação global da sessão",
        answer=contexto,
        veredict=veredict_data,
        justification=veredict_data.get("reflexao", "")
    )





while True:
    
    # time.sleep(30)
    print("____________________________________________________________________________________________________")
    ask = input("> ")
    if ask == 1:
        break

    elif ask.lower() == "avalie":
        name = select_by_id(id)
        run_audit_all(id, name)
        continue

    elif ask == "avalie_tudo":
        name = select_by_id(id)
        run_audit_full_session(id, name)
        continue


    resposta_completa = agent_saude.run(ask, session_id=session_id, memory=True)
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