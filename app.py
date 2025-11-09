from flask import Flask, request, jsonify
import requests
import os
import re

app = Flask(__name__)
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

@app.route('/api/cik', methods=['GET'])
def get_cik():
    ticker = request.args.get('ticker', '').upper()
    if not FINNHUB_API_KEY:
        return jsonify({"error": "Missing Finnhub API key"}), 500

    # 1. Requête Finnhub
    url = f"https://finnhub.io/api/v1/stock/profile2?symbol={ticker}&token={FINNHUB_API_KEY}"
    try:
        resp = requests.get(url)
        data = resp.json()

        name = data.get("name", "non dispo")
        exchange = data.get("exchange", "non dispo")
        cik = data.get("cik")

        # 2. Fallback si cik manquant : scraping de la SEC
        if not cik:
            sec_url = f"https://www.sec.gov/cgi-bin/browse-edgar?CIK={ticker}&owner=exclude&action=getcompany"
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; GPTCustomBot/1.0)',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            sec_resp = requests.get(sec_url, headers=headers)
            if sec_resp.status_code == 200:
                match = re.search(r'CIK=(\d{10})', sec_resp.text)
                if match:
                    cik = match.group(1)

        return jsonify({
            "cik": cik or "non dispo",
            "name": name,
            "exchange": exchange
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
