import requests
import json
import sys

def get_holders():
    API_KEY = "BAI6RGS5M15MWYNU9PZ7N8M2JP9V4QR6W6"
    contrato = "0x9df5c1ad28fb08b47c07bd8e48f37b33fdebcd05"
    
    # URL da API V2 do Etherscan
    url = f"https://api.etherscan.io/v2/api?chainid=999&module=token&action=gettokenholders&contractaddress={contrato}&page=1&offset=50&apikey={API_KEY}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        print("Buscando dados na API do Etherscan...")
        response = requests.get(url, headers=headers)
        data = response.json()
        
        items = data.get('result', [])
        status = data.get('status', '1')
        
        # Se a API do Etherscan mandar um erro (ex: chave invalida, plano Pro, etc)
        if status == '0' or not isinstance(items, list):
            # Descobre qual foi a desculpa que o Etherscan deu
            motivo_erro = items if isinstance(items, str) else data.get('message', 'Erro desconhecido')
            print(f"ERRO REAL DO ETHERSCAN: {motivo_erro}")
            
            # Mostra o erro do Etherscan DIRETO NO SEU SITE!
            error_data = [{"rank": "!", "address": f"Aviso Etherscan: {motivo_erro}", "quantity": "0", "percentage": "0"}]
            with open('holders.json', 'w') as f:
                json.dump(error_data, f)
            sys.exit(0)

        holders_list = []
        for i, item in enumerate(items[:50], 1):
            quantidade_bruta = float(item.get('TokenHolderQuantity', 0))
            quantidade_real = quantidade_bruta / (10**18) 

            holders_list.append({
                "rank": i,
                "address": item.get('TokenHolderAddress', 'N/A'),
                "quantity": f"{quantidade_real:,.2f}",
                "percentage": "N/A"
            })
        
        with open('holders.json', 'w') as f:
            json.dump(holders_list, f, indent=4)
        print(f"Sucesso! {len(holders_list)} holders salvos.")

    except Exception as e:
        # Se der erro interno no Python
        error_data = [{"rank": "!", "address": f"Erro interno: {str(e)[:40]}", "quantity": "0", "percentage": "0"}]
        with open('holders.json', 'w') as f:
            json.dump(error_data, f)
        sys.exit(0)

if __name__ == "__main__":
    get_holders()
