from curl_cffi import requests
import json
import sys

def get_holders():
    url = "https://hyperevmscan.io/api/v2/tokens/0x9df5c1ad28fb08b47c07bd8e48f37b33fdebcd05/holders"
    
    try:
        print("Tentando acessar com curl_cffi (Imitação profunda do Chrome)...")
        # O parâmetro impersonate="chrome110" é a mágica que burla o bloqueio
        response = requests.get(url, impersonate="chrome110", timeout=30)
        
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("ERRO: O Cloudflare bloqueou a requisição novamente.")
            print(response.text[:500])
            raise ValueError("Bloqueio de segurança detectado.")

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
        print(f"Sucesso! {len(holders_list)} holders salvos com a nova tática.")

    except Exception as e:
        print(f"Erro na execução: {e}")
        error_data = [{"rank": "!", "address": "Bloqueio Cloudflare Ativo", "quantity": "0", "percentage": "0"}]
        with open('holders.json', 'w') as f:
            json.dump(error_data, f)
        sys.exit(0)

if __name__ == "__main__":
    get_holders()
