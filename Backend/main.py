from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def serve_home():
    return jsonify({
        'response': "Connected to backend.",
    })


@app.route("/sampleResponse", methods=["POST"])
def serve_sampleResponse():
    data = request.json
    message = data['message']
    print("Message received: " + message)
    return jsonify({
        'response': f"Successfully received {message}.",
    })


if __name__ == "__main__":
    app.run(host='192.168.0.24', port=8888)
