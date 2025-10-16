from crud import select, select_by_name
from db import close

def calc_imc(altura: float, peso: float) -> dict:
    '''
    Just use this tool if you are asked to calculate imc from a person
    Parâmetros:
      - peso: kg
      - altura: metros
    Retorna um dict com o IMC e a classificação.
    '''
    imc = peso / altura**2

    if imc < 18.5: cls = "Abaixo do peso"
    elif imc < 25: cls = "Peso normal"
    elif imc < 30: cls = "Sobrepeso"
    else: cls = "Obesidade"

    return {"imc": round(imc,2), "classificacao": cls}

def calc_tdee(peso: float, altura: float, idade: int, sexo: str, nivel: str) -> dict:
    """Use it to calculate the Total Daily Energy Expenditure

    Args:
        peso (float): peso > 0
        altura (float): Altura em centímetros (cm), Altura > 0
        idade (int): Idade deve ser acima de 0
        sexo (str): "M" para masculino, "F" para feminino.
        nivel (str): Nível de atividade: "sed", "leve", "mod", "intenso" ou "extremo".


    Returns:
        - bmr (int): Taxa metabólica basal estimada (kcal/dia).
        - tdee (int): Gasto energético total estimado (kcal/dia).
    """

    sexo_available = {"M", "F"}
    fat = {"sed": 1.2, "leve": 1.375, "mod": 1.55, "intenso": 1.725, "extremo": 1.9}

    if peso <= 0 or altura <= 0 or idade <= 0 or sexo not in sexo_available or nivel not in fat:
        raise ValueError("Está Faltando parametros corretos")


    bmr = (10*peso) + (6.25*altura) - (5*idade) + (5 if sexo=="M" else -161)

    tdee = 0

    for i, t in fat.items():
        if i == nivel:
            tdee = t * bmr
    
    return {"bmr": bmr, 'tdee': tdee}


def get_user_info(name: str) -> str:
    """
    Use it for identify the persona and in base of queries, you do a recomendation for the person of what should the person do different for body changes to get healther pay attention if the patient uses some type of medicine to remind them
    """
    
    print(f"📡 Tool get_user_info chamada para: {name}")
    user = select_by_name(name)

    
    if user:
        id_, name, idade, sexo, peso, altura, nivel_atividade, habits = user
        return (
            f"{name}, {idade} anos, sexo {sexo}, {peso}kg, {altura}cm, "
            f"nível de atividade {nivel_atividade}. Hábitos: {habits}"
        )

    return "Usuário não encontrado."
