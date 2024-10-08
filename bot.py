import requests
import json

# Carregar configurações do arquivo config.json
with open('config.json') as config_file:
    config = json.load(config_file)

# Atribuir variáveis a partir do JSON
URL_ENDPOINT = config['URL_ENDPOINT']
API_KEY = config['API_KEY']
MOEDA_VALOR = config['MOEDA_VALOR']
MOEDA_BUY = config['MOEDA_BUY']
WEBHOOK_URL = config['WEBHOOK_URL']
# Construa a URL completa
url = f"{URL_ENDPOINT}{API_KEY}/latest/{MOEDA_VALOR}"

# Envie a requisição GET
response = requests.get(url)

# Verifique o status da resposta
if response.status_code == 200:
    # Parseie o JSON da resposta
    data = response.json()

    # Extraia a taxa de câmbio desejada
    taxa_cambio = data['conversion_rates'].get(MOEDA_BUY)

    if taxa_cambio:
        print(f" {MOEDA_VALOR} para {MOEDA_BUY} é R${taxa_cambio}")
        data = {"content": f"{MOEDA_VALOR} para {MOEDA_BUY} é R${taxa_cambio}"}
        response = requests.post(WEBHOOK_URL, data=json.dumps(data), headers={"Content-Type": "application/json"})
        if response.status_code == 204:
            print("Mensagem enviada com sucesso!")
        else:
            print(f"Falha ao enviar mensagem. Status: {response.status_code}, Resposta: {response.text}")
    else:
        print(f"Informação sobre a moeda {MOEDA_BUY} não encontrada.")
else:
    print(f"Erro ao acessar a API: {response.status_code}")