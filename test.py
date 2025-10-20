test = {"idade": 14, "osl": 13}

print(test.items())


import json

pessoa = {"nome": "Gustavo", "idade": 18}
json_str = json.dumps(pessoa)   # dict → JSON string
print(type(json_str))                 # {"nome": "Gustavo", "idade": 18}
print(13225555555555555)
print(json_str.nome)

obj = json.loads(json_str)      # JSON string → dict
print(obj["nome"])              # Gustavo
