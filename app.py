from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/api/cik', methods=['GET'])
def get_cik():
    ticker = request.args.get('ticker', '').upper()
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?CIK={ticker}&owner=exclude&action=getcompany&output=json"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        resp = requests.get(url, headers=headers)

        if resp.status_code != 200:
            return jsonify({"error": f"SEC responded with status {resp.status_code}"}), 502

        data = resp.json()

        for entry in data.values():
            if entry['ticker'] == ticker:
                return jsonify({"cik": str(entry['cik_str']).zfill(10)})
        return jsonify({"error": "Ticker not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
