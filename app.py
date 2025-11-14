from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok"})

@app.route("/sum", methods=["GET"])
def summation():
    a = request.args.get("a", None)
    b = request.args.get("b", None)
    try:
        a_f = float(a)
        b_f = float(b)
    except (TypeError, ValueError):
        return jsonify({"error": "a and b must be numbers"}), 400
    return jsonify({"sum": a_f + b_f})
    
if __name__ == "__main__":
    # Use 127.0.0.1 so tests using requests can hit it locally
    app.run(host="127.0.0.1", port=5000)
