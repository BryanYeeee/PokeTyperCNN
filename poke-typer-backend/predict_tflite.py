# predict_module.py with effnet

import tensorflow as tf
import threading

tflite_lock = threading.Lock()

def load_tflite(model_path):
    """Load a TFLite model and return interpreter + IO details."""
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter, input_details, output_details

# def predict_h5(model, image_bytes):
#     """Predict using a Keras .h5 model."""
#     tensor = preprocess_image(image_bytes)
#     preds = model.predict(tensor)
#     return preds[0]   # return vector only


def predict_tflite(interpreter, input_details, output_details, image_bytes, preprocess_image):
    """Run inference on a TFLite model."""
    tensor = preprocess_image(image_bytes)
    with tflite_lock:
        interpreter.set_tensor(input_details[0]["index"], tensor)
        interpreter.invoke()

        preds = interpreter.get_tensor(output_details[0]["index"])
    return preds[0]  
