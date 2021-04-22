from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/send", methods=["POST"])
def send():
    f = request.files["file0"]
    f.save(f.filename)

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
