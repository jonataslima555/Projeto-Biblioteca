import requests
import models

def validator_cpf(cpf):
    url = "https://api.invertexto.com/v1/validator"
    headers = {"Authorization": f"Bearer {models.API_KEY}"}
    params = {"value": cpf}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        return data
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def format_result(data):
    if "valid" in data and data["valid"]:
        print("CPF válido")
        return True
    else:
        print("CPF inválido")
        return False
