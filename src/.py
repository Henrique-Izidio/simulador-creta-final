import json

class JsonDecoder:
    def decode(filePath: str):
        try:
            with open(filePath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            print("Dados lidos com sucesso!")
            print(f"Tipo do objeto em Python: {type(data)}")
            print(data)

        except FileNotFoundError:
            print(f"Erro: O arquivo '{filePath}' não foi encontrado.")
        except json.JSONDecodeError:
            print(f"Erro: O arquivo '{filePath}' não está formatado corretamente como JSON.")