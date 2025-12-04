# predict_module.py with effnet

import tensorflow as tf

def load_tflite(model_path):
    """Load a TFLite model and return interpreter + IO details."""
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter, input_details, output_details

def preprocess_image(image_bytes):
    """Preprocess the image exactly like your .h5 model pipeline."""
    img = tf.image.decode_image(image_bytes, channels=3)
    img = tf.image.resize(img, (224, 224))
    img = tf.keras.applications.efficientnet.preprocess_input(img)
    return tf.expand_dims(img, axis=0)  # shape: (1,224,224,3)


# def predict_h5(model, image_bytes):
#     """Predict using a Keras .h5 model."""
#     tensor = preprocess_image(image_bytes)
#     preds = model.predict(tensor)
#     return preds[0]   # return vector only


def predict_tflite(interpreter, input_details, output_details, image_bytes):
    """Run inference on a TFLite model."""
    tensor = preprocess_image(image_bytes)

    interpreter.set_tensor(input_details[0]["index"], tensor)
    interpreter.invoke()

    preds = interpreter.get_tensor(output_details[0]["index"])
    return preds[0]  
