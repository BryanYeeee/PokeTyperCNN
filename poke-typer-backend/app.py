from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from preprocess import *
from format_pred import format_prediction
import os

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, resources={r"/*": {"origins": [
            "https://poketypercnn.pages.dev",
            "http://localhost:3000"
        ]}})



models = {
    "A": [load_model("models/model_A.h5"), preprocess_effnet],
    "B": [load_model("models/model_B.h5"), preprocess_effnet],
    "C": [load_model("models/model_C.h5"),preprocess_effnet],
    "D": [load_model("models/model_D.keras"),preprocess_resnet],
    "E": [load_model("models/model_E.keras"),preprocess_resnet]
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
