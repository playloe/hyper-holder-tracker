import requests
import json
import sys

def get_holders():
    # URL oficial da API para holders do token HF
    url = "https://hyperevmscan.io/api/v2/tokens/0x9df5c1ad28fb08b47c07bd8e48f37b33fdebcd05/holders"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        print(f"Conectando ao HyperScan...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        holders_list = []
        items = data.get('items', [])
        
        if not items:
            print("API retornou lista vazia.")
            # Cria um arquivo vazio para não dar erro no Git
            with open('holders.json', 'w') as f:
                json.dump([], f)
            return

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
        print(f"Erro crítico: {e}")
        # Garante que o arquivo exista para o GitHub Actions não travar
        if not hasattr(sys, 'holders_created'):
            with open('holders.json', 'w') as f:
                json.dump([{"rank": 0, "address": "Erro na API", "quantity": "0", "percentage": "0"}], f)
        sys.exit(1)

if __name__ == "__main__":
    get_holders()
