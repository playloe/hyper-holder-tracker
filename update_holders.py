import requests
import json
import sys

def get_holders():
    SCRAPER_KEY = "49b6f019e504a5ec3271bd87b55da0bd"
    url_alvo = "https://hyperevmscan.io/api/v2/tokens/0x9df5c1ad28fb08b47c07bd8e48f37b33fdebcd05/holders"
    
    # O COMBO MÁXIMO: antibot=true (resolve o desafio do Cloudflare) + premium=true (IP Residencial)
    url = f"http://api.scraperapi.com?api_key={SCRAPER_KEY}&url={url_alvo}&antibot=true&premium=true"
    
    try:
        print("Buscando dados via ScraperAPI (Combo: Premium + AntiBot)...")
        # O desafio do Cloudflare pode levar uns 10 a 15 segundos para ser resolvido pelo ScraperAPI
        response = requests.get(url, timeout=120)
        
        try:
            data = response.json()
        except json.JSONDecodeError:
            texto_erro = response.text[:100].replace('\n', ' ')
            raise ValueError(f"Site bloqueou com HTML: {texto_erro}")
        
        items = data.get('items', [])
        
        if not items:
            raise ValueError("A lista de holders veio vazia. API original não tem dados.")

        holders_list = []
        for i, item in enumerate(items[:50], 1):
            quantidade = item.get('value', '0')
            try:
                quantidade_formatada = f"{float(quantidade):,.2f}"
            except:
                quantidade_formatada = quantidade

            percentual_bruto = item.get('value_percent', '0')
            try:
                percentual_formatado = f"{float(percentual_bruto):.2f}%"
            except:
                percentual_formatado = "0%"

            holders_list.append({
                "rank": i,
                "address": item.get('address', {}).get('hash', 'N/A'),
                "quantity": quantidade_formatada,
                "percentage": percentual_formatado
            })
        
        with open('holders.json', 'w') as f:
            json.dump(holders_list, f, indent=4)
        print(f"Sucesso! {len(holders_list)} holders salvos furando o Cloudflare.")

    except Exception as e:
        print(f"Erro na execução: {e}")
        error_data = [{"rank": "!", "address": f"Erro Final: {str(e)[:70]}", "quantity": "0", "percentage": "0"}]
        with open('holders.json', 'w') as f:
            json.dump(error_data, f)
        sys.exit(0)

if __name__ == "__main__":
    get_holders()
