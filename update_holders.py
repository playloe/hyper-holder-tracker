import requests
import json
import sys

def get_holders():
    # Sua chave oficial gerada agora pouco
    API_KEY = "BAI6RGS5M15MWYNU9PZ7N8M2JP9V4QR6W6"
    
    # Endereço do contrato HF
    contrato = "0x9df5c1ad28fb08b47c07bd8e48f37b33fdebcd05"
    
    # URL da API V2 oficial focada na rede HyperEVM (chainid=999)
    url = f"https://api.etherscan.io/v2/api?chainid=999&module=token&action=gettokenholders&contractaddress={contrato}&page=1&offset=50&apikey={API_KEY}"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        print("Buscando dados via API Oficial do Etherscan (Porta da frente!)...")
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # A API oficial guarda a lista de holders dentro de 'result'
        items = data.get('result', [])
        
        # Verifica se deu algum erro na chave ou na leitura
        if not isinstance(items, list):
            print(f"ERRO da API: {items}")
            raise ValueError("Falha ao ler os dados da API.")

        holders_list = []
        for i, item in enumerate(items[:50], 1):
            # Formatação do valor (tira os 18 zeros que as blockchains usam no backend)
            quantidade_bruta = float(item.get('TokenHolderQuantity', 0))
            quantidade_real = quantidade_bruta / (10**18) 

            holders_list.append({
                "rank": i,
                "address": item.get('TokenHolderAddress', 'N/A'),
                "quantity": f"{quantidade_real:,.2f}", # Deixa o número bonito com 2 casas
                "percentage": "N/A" # A API oficial não envia a % pronta
            })
        
        with open('holders.json', 'w') as f:
            json.dump(holders_list, f, indent=4)
        print(f"Vitória! {len(holders_list)} holders salvos usando sua API Key oficial.")

    except Exception as e:
        print(f"Erro na execução: {e}")
        error_data = [{"rank": "!", "address": "Erro de Conexão na API", "quantity": "0", "percentage": "0"}]
        with open('holders.json', 'w') as f:
            json.dump(error_data, f)
        sys.exit(0)

if __name__ == "__main__":
    get_holders()
