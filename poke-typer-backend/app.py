from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from preprocess import *
from format_pred import format_prediction
import os
import requests

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, resources={r"/*": {"origins": [
            "https://poketypercnn.pages.dev",
            "http://localhost:3000"
        ]}})


BASE = os.path.dirname(os.path.abspath(__file__))

files = {
    "https://dl.dropboxusercontent.com/scl/fi/8a1nulx8wif5fkwyzxo8kqgxpb/model_D.keras?rlkey=9ho830wy7ckemco3lz9kqgxpb&st=b9uvvh8i&dl=0": "models/model_D.keras",
    "https://dl.dropboxusercontent.com/scl/fi/qi5zkvi16fns6yykc9shx/model_E.keras?rlkey=iwpdd1glsgw4djpt6yfsk64be&st=saa3bjdu&dl=0": "models/model_E.keras"
}

def download_file(url, path):
    print(f"Downloading {path}...")
    r = requests.get(url, stream=True)
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Saved {path}")

for url, path in files.items():
    download_file(url, path)
# if os.getenv("RENDER") == "1":
#     for url, path in files.items():
#         download_file(url, path)

models = {
    "A": [load_model(os.path.join(BASE, "models/model_A.h5")), preprocess_effnet],
    "B": [load_model(os.path.join(BASE, "models/model_B.h5")), preprocess_effnet],
    "C": [load_model(os.path.join(BASE, "models/model_C.h5")),preprocess_effnet],
    "D": [load_model(os.path.join(BASE, "models/model_D.keras")),preprocess_resnet],
    "E": [load_model(os.path.join(BASE, "models/model_E.keras")),preprocess_resnet]
}

for key in models:
    dummy = tf.zeros((1, 224, 224, 3))
    _ = models[key][0](dummy)
    
@app.route("/predict/<model_name>", methods=["POST"])
def predict(model_name):
    if model_name not in models:
        return jsonify({"error": f"Model '{model_name}' not found"}), 404

    # Expect an image file in the request
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    image_bytes = file.read()
    model, preprocess_fn = models[model_name]

    input_tensor = preprocess_fn(image_bytes)
    preds = model.predict(input_tensor)

    return jsonify({"model": model_name, "prediction": format_prediction(preds)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
