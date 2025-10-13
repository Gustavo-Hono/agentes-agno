from dotenv import load_dotenv
from agno.agent import Agent
load_dotenv()
from agno.models.google import Gemini
import os
from agents import calc_imc, calc_tdee



agent = Agent(model=Gemini(id="gemini-2.5-pro"),
              system_message="Você é um coach de saúde direto e seguro",
              tools=[calc_imc, calc_tdee])

resposta_completa = agent.run("como eu sei meu nivel de treinamento se é leve, moderado ou extremo ?")


print(resposta_completa.content) 




