from dotenv import load_dotenv
from agno.agent import Agent
load_dotenv()
from agno.models.google import Gemini
import os
from agents import calc_imc, calc_tdee, get_user_info
from crud import select, delete, update, insert, select_by_name



agent = Agent(model=Gemini(id="gemini-2.5-pro"),
              system_message="Você é um coach de saúde confiável e inteligente. Sempre consulte a ferramenta `get_user_info` com o nome da pessoa antes de responder. Sua missão é entender os hábitos, histórico e rotina da pessoa a partir dos dados retornados pela ferramenta, e então dar conselhos de saúde, nutrição e estilo de vida. Se a pessoa não informar um nome existente no banco, informe que não há dados para consulta.",
              tools=[calc_imc, calc_tdee, get_user_info])

while True:
    print("____________________________________________________________________________________________________")
    ask = input("> ")
    if ask == 1:
        break
    resposta_completa = agent.run(ask)
    print(resposta_completa.content)
    





