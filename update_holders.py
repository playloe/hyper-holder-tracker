import cloudscraper
import json
import sys

def get_holders():
    url = "https://hyperevmscan.io/api/v2/tokens/0x9df5c1ad28fb08b47c07bd8e48f37b33fdebcd05/holders"
    
    # Criamos um "scraper" que finge ser o Google Chrome no Windows
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    })
    
    try:
        print("A tentar aceder ao HyperScan com disfarce de navegador...")
        response = scraper.get(url, timeout=30)
        response.raise_for_status()
        
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("ERRO: O site bloqueou o acesso novamente.")
            print(response.text[:500])
            raise ValueError("Bloqueio de anti-bot detetado.")

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
        print(f"Sucesso! {len(holders_list)} holders guardados.")

    except Exception as e:
        print(f"Erro na execução: {e}")
        error_data = [{"rank": "!", "address": "O HyperScan bloqueou a leitura", "quantity": "0", "percentage": "0"}]
        with open('holders.json', 'w') as f:
            json.dump(error_data, f)
        sys.exit(0)

if __name__ == "__main__":
    get_holders()
