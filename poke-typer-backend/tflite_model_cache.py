# tflite_model_cache.py
import os
import tensorflow as tf

BASE = os.path.dirname(os.path.abspath(__file__))

from preprocess import preprocess_effnet, preprocess_resnet


MODEL_FILES = {
    "A": ("model_A.tflite", preprocess_effnet),
    "B": ("model_B.tflite", preprocess_effnet),
    "C": ("model_C.tflite", preprocess_effnet),
    "D": ("model_D.tflite", preprocess_resnet),
    "E": ("model_E.tflite", preprocess_resnet),
}

current_name = None
current_interpreter = None
current_input_details = None
current_output_details = None
current_preprocess = None


def load_tflite_interpreter(model_name):
    global current_name, current_interpreter, current_input_details, current_output_details, current_preprocess

    # cache
    if model_name == current_name:
        return (
            current_interpreter,
            current_input_details,
            current_output_details,
            current_preprocess,
        )

    # load  new model
    fname, preprocess = MODEL_FILES[model_name]
    path = os.path.join(BASE, "models", fname)

    interpreter = tf.lite.Interpreter(model_path=path)
    interpreter.allocate_tensors()

    current_name = model_name
    current_interpreter = interpreter
    current_input_details = interpreter.get_input_details()
    current_output_details = interpreter.get_output_details()
    current_preprocess = preprocess

    return (
        current_interpreter,
        current_input_details,
        current_output_details,
        current_preprocess,
    )
