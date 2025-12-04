from flask import Flask, request, jsonify
from flask_cors import CORS
# from tensorflow.keras.models import load_model
import os

from preprocess import *
from format_pred import format_prediction
from tflite_model_cache import load_tflite_interpreter, MODEL_FILES
from predict_tflite import load_tflite, predict_tflite

# import requests

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, resources={
    r"/*": {
        "origins": ["https://poketypercnn.pages.dev","http://localhost:3000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})



# modelA = load_model(os.path.join(BASE, "models/model_A.h5"))
# modelB = load_model(os.path.join(BASE, "models/model_B.h5"))
# modelC = load_model(os.path.join(BASE, "models/model_C.h5"))
# models (not tflite) = {
#     "A": [modelA, preprocess_effnet],
#     "B": [modelB, preprocess_effnet],
#     "C": [modelC,preprocess_effnet],
#     "D": [load_model(os.path.join(BASE, "models/model_D.keras")),preprocess_resnet],
#     "E": [load_model(os.path.join(BASE, "models/model_E.keras")),preprocess_resnet]
# }
# for key in models:
#     dummy = tf.zeros((1, 224, 224, 3))
#     _ = models[key][0](dummy)
    
@app.route("/predict/<model_name>", methods=["POST"])
def predict(model_name):
    # if model_name in ["D", "E"]:
    #     return jsonify({"error": f"Model D and E currently unavailable"}), 404

    if model_name not in MODEL_FILES:
        return jsonify({"error": f"Model '{model_name}' not found"}), 404

    # Expect an image file in the request
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    image_bytes = file.read()

    interpreter, input_details, output_details, preprocess = load_tflite_interpreter(
        model_name
    )
    preds = predict_tflite(interpreter, input_details, output_details, image_bytes, preprocess)

    return jsonify({"model": model_name, "prediction": format_prediction(preds.reshape(1, -1))})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
