from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from preprocess import *
from format_pred import format_prediction

app = Flask(__name__)
CORS(app)


models = {
    "A": [load_model("models/model_A.h5"), preprocess_effnet],
    "B": [load_model("models/model_B.h5"), preprocess_effnet],
    "C": [load_model("models/model_C.h5"),preprocess_effnet],
    # "D": [load_model("models/resnet1.h5"),preprocess_resnet],
    # "E": [load_model("models/resnet2.h5"),preprocess_resnet]
}

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
    app.run(host="0.0.0.0", port=5000)
