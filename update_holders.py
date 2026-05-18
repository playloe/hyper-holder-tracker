import requests
import json
import sys

def get_holders():
    SCRAPER_KEY = "49b6f019e504a5ec3271bd87b55da0bd"
    url_alvo = "https://hyperevmscan.io/api/v2/tokens/0x9df5c1ad28fb08b47c07bd8e48f37b33fdebcd05/holders"
    
    # Mantemos o combo que furou o bloqueio (Antibot + Premium)
    url = f"http://api.scraperapi.com?api_key={SCRAPER_KEY}&url={url_alvo}&antibot=true&premium=true"
    
    try:
        print("Buscando dados via ScraperAPI...")
        response = requests.get(url, timeout=120)
        texto_resposta = response.text
        
        data = None
        
        # Tenta ler o JSON normalmente
        try:
            data = json.loads(texto_resposta)
        except json.JSONDecodeError:
            print("O ScraperAPI embrulhou os dados em HTML. Extraindo o recheio (JSON)...")
            # Se falhar, procura exatamente onde começam e terminam os dados (os símbolos { e })
            inicio = texto_resposta.find('{')
            fim = texto_resposta.rfind('}') + 1
            
            if inicio != -1 and fim != 0:
                json_puro = texto_resposta[inicio:fim]
                try:
                    data = json.loads(json_puro)
                except Exception as e:
                    raise ValueError(f"Falha ao limpar o HTML: {e}")
            else:
                # Se realmente não tiver dados, mostramos os primeiros caracteres da página para investigar
                raise ValueError(f"Página bloqueada: {texto_resposta[:60]}")

        # Daqui pra baixo é o código normal, pois já extraímos os dados limpos!
        items = data.get('items', [])
        
        if not items:
            raise ValueError("A API não retornou as carteiras (lista vazia).")

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
        print(f"Sucesso Absoluto! {len(holders_list)} holders salvos e limpos.")

    except Exception as e:
        print(f"Erro na execução: {e}")
        error_data = [{"rank": "!", "address": f"Erro de Extração: {str(e)[:60]}", "quantity": "0", "percentage": "0"}]
        with open('holders.json', 'w') as f:
            json.dump(error_data, f)
        sys.exit(0)

if __name__ == "__main__":
    get_holders()
