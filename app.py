from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/api/cik', methods=['GET'])
def get_cik():
    ticker = request.args.get('ticker', '').upper()
    url = "https://www.sec.gov/files/company_tickers.json"
    try:
        data = requests.get(url).json()
        for entry in data.values():
            if entry['ticker'] == ticker:
                return jsonify({"cik": str(entry['cik_str']).zfill(10)})
        return jsonify({"error": "Ticker not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#  Lancement Render : écoute sur le port dynamique fourni par Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render définit PORT dans l'environnement
    app.run(host='0.0.0.0', port=port)
