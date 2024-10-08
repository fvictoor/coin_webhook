import os
import requests
import json

# Atribuir variáveis a partir das variáveis de ambiente
URL_ENDPOINT = os.getenv('URL_ENDPOINT')
API_KEY = os.getenv('API_KEY')
MOEDA_VALOR = os.getenv('MOEDA_VALOR', 'USD').split(',')  # Listas separadas por vírgula
MOEDA_BUY = os.getenv('MOEDA_BUY', 'BRL').split(',')      # Listas separadas por vírgula
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Função para enviar a taxa de câmbio para o WebHook
def send_to_webhook(moeda_valor, moeda_buy, taxa_cambio):
    message = {"content": f"**{moeda_valor}** para **{moeda_buy}** é ***R${taxa_cambio}***",
               "avatar_url": "https://www.pngarts.com/files/6/Money-Emoji-PNG-Photo.png"  # Opcional: URL de imagem para o avatar
               }
    response = requests.post(WEBHOOK_URL, data=json.dumps(message), headers={"Content-Type": "application/json"})
    if response.status_code == 204:
        print(f"Mensagem enviada com sucesso para {moeda_valor} para {moeda_buy}!")
    else:
        print(f"Falha ao enviar mensagem para {moeda_valor} para {moeda_buy}. Status: {response.status_code}, Resposta: {response.text}")

# Iterar sobre cada moeda valor e moeda buy
for valor in MOEDA_VALOR:
    for buy in MOEDA_BUY:
        # Construa a URL completa
        url = f"{URL_ENDPOINT}{API_KEY}/latest/{valor}"

        # Envie a requisição GET
        response = requests.get(url)

        # Verifique o status da resposta
        if response.status_code == 200:
            # Parseie o JSON da resposta
            data = response.json()

            # Extraia a taxa de câmbio desejada
            taxa_cambio = data['conversion_rates'].get(buy)

            if taxa_cambio:
                print(f"{valor} para {buy} é R${taxa_cambio}")
                send_to_webhook(valor, buy, taxa_cambio)
            else:
                print(f"Informação sobre a moeda {buy} não encontrada.")
        else:
            print(f"Erro ao acessar a API para {valor}: {response.status_code}")
