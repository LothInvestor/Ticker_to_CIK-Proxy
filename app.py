from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

@app.route('/api/cik', methods=['GET'])
def get_cik():
    ticker = request.args.get('ticker', '').upper()
    if not FINNHUB_API_KEY:
        return jsonify({"error": "Missing Finnhub API key"}), 500

    url = f"https://finnhub.io/api/v1/stock/profile2?symbol={ticker}&token={FINNHUB_API_KEY}"

    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            return jsonify({"error": f"Finnhub error {resp.status_code}"}), 502

        data = resp.json()
        if 'name' in data:
            return jsonify({
                "cik": data.get("cik", "non dispo"),
                "name": data.get("name", "non dispo"),
                "exchange": data.get("exchange", "non dispo")
            })
        else:
            return jsonify({"error": "Ticker non reconnu"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
