from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/status')
def status():
    return {"status": "ok"}

@app.route('/sum')
def sum_numbers():
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
        return {"result": a + b}
    except ValueError:
        return {"error": "Invalid numbers"}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)