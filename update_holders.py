import requests
import json

def get_holders():
    # API da HyperEVM Scan para o token HF
    url = "https://hyperevmscan.io/api/v2/tokens/0x9df5c1ad28fb08b47c07bd8e48f37b33fdebcd05/holders"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        holders_list = []
        # Pegamos os top 50
        for i, item in enumerate(data.get('items', [])[:50], 1):
            holders_list.append({
                "rank": i,
                "address": item.get('address', {}).get('hash'),
                "quantity": item.get('value'),
                "percentage": item.get('value_percent')
            })
        
        with open('holders.json', 'w') as f:
            json.dump(holders_list, f, indent=4)
        print("Sucesso! Dados salvos em holders.json")
    except Exception as e:
        print(f"Erro ao coletar dados: {e}")

if __name__ == "__main__":
    get_holders()
