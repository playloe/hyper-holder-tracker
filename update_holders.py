import requests
import json
import sys

def get_holders():
    # URL da API do HyperEVM Scan
    url = "https://hyperevmscan.io/api/v2/tokens/0x9df5c1ad28fb08b47c07bd8e48f37b33fdebcd05/holders"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    
    try:
        print(f"Conectando ao HyperScan...")
        response = requests.get(url, headers=headers, timeout=30)
        
        # Se der erro de servidor, isso avisa
        response.raise_for_status()
        
        # Tenta transformar em JSON
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("ERRO: O site não devolveu um JSON. Devolveu isso:")
            print(response.text[:500]) # Mostra os primeiros 500 caracteres do erro
            raise ValueError("Resposta do site não é um JSON válido.")

        holders_list = []
        items = data.get('items', [])
        
        for i, item in enumerate(items[:50], 1):
            holders_list.append({
                "rank": i,
                "address": item.get('address', {}).get('hash', 'N/A'),
                "quantity": item.get('value', '0'),
                "percentage": item.get('value_percent', '0')
            })
        
        with open('holders.json', 'w') as f:
            json.dump(holders_list, f, indent=4)
        print(f"Sucesso! {len(holders_list)} holders salvos.")

    except Exception as e:
        print(f"Erro crítico na execução: {e}")
        # Cria um arquivo de erro para o site não ficar em branco
        error_data = [{"rank": "!", "address": "Erro na API/Bloqueio", "quantity": "0", "percentage": "0"}]
        with open('holders.json', 'w') as f:
            json.dump(error_data, f)
        sys.exit(0) # Finaliza "com sucesso" para não travar o GitHub

if __name__ == "__main__":
    get_holders()
