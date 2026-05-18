import requests
import json
import sys

def get_holders():
    # 1. Sua chave do ScraperAPI atualizada:
    SCRAPER_KEY = "49b6f019e504a5ec3271bd87b55da0bd"
    
    # A URL original do HyperScan (que sabíamos que tinha os dados perfeitos)
    url_alvo = "https://hyperevmscan.io/api/v2/tokens/0x9df5c1ad28fb08b47c07bd8e48f37b33fdebcd05/holders"
    
    # A URL mágica que usa o ScraperAPI para mascarar nosso robô e furar o Cloudflare
    url = f"http://api.scraperapi.com?api_key={SCRAPER_KEY}&url={url_alvo}"
    
    try:
        print("Buscando dados via ScraperAPI (Invisível para o Cloudflare)...")
        # Aumentamos o timeout porque o disfarce demora uns segundinhos a mais
        response = requests.get(url, timeout=60)
        
        try:
            data = response.json()
        except:
            print("Erro ao tentar ler o formato JSON.")
            raise ValueError("O ScraperAPI não conseguiu ler os dados corretos.")
        
        items = data.get('items', [])
        
        if not items:
            raise ValueError("A lista de holders veio vazia.")

        holders_list = []
        for i, item in enumerate(items[:50], 1):
            # O valor na API original já vem certo, só formatamos pra ficar com vírgulas
            quantidade = item.get('value', '0')
            try:
                quantidade_formatada = f"{float(quantidade):,.2f}"
            except:
                quantidade_formatada = quantidade

            # A porcentagem de cada baleia (ex: "45.1234"), arredondamos para 2 casas
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
        print(f"Vitória Absoluta! {len(holders_list)} holders salvos furando o bloqueio.")

    except Exception as e:
        print(f"Erro na execução: {e}")
        error_data = [{"rank": "!", "address": f"Erro no Scraper: {str(e)[:40]}", "quantity": "0", "percentage": "0"}]
        with open('holders.json', 'w') as f:
            json.dump(error_data, f)
        sys.exit(0)

if __name__ == "__main__":
    get_holders()
