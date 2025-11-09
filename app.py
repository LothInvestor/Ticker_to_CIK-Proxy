from flask import Flask, request, jsonify
import requests

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
