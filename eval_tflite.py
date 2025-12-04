#!/usr/bin/env python3
"""
Evaluate a TFLite model and compute ONLY multi-class macro AUC.
"""

import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.metrics import roc_auc_score
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE, "data", "phoenixdex_pokemon.csv")
IMAGE_DIR = os.path.join(BASE, "data", "fakemon-images-blackbg")
TFLITE_MODEL_PATH = os.path.join(BASE, "poke-typer-backend", "models", "model_E.tflite")

NUM_CLASSES = 18
label_cols = [f"label_{i}" for i in range(NUM_CLASSES)]

def load_tflite_interpreter(path):
    print(f"[INFO] Loading TFLite model:\n{path}")
    interpreter = tf.lite.Interpreter(model_path=path)
    interpreter.allocate_tensors()
    return (
        interpreter,
        interpreter.get_input_details(),
        interpreter.get_output_details()
    )

def prepare_input(batch_x, input_detail):
    dtype = input_detail["dtype"]
    scale, zero_point = input_detail.get("quantization", (0.0, 0))

    x = np.ascontiguousarray(batch_x)

    if dtype == np.float32:
        return x.astype(np.float32)

    elif dtype in (np.uint8, np.int8):
        if scale == 0:
            raise ValueError("Invalid quantization scale for quantized model.")
        x_f = x.astype(np.float32)
        q = np.round(x_f / scale + zero_point).astype(dtype)
        if dtype == np.uint8:
            q = np.clip(q, 0, 255)
        else:
            q = np.clip(q, -128, 127)
        return q

    raise NotImplementedError(f"Unsupported dtype: {dtype}")

def evaluate_auc(interpreter, input_details, output_details, generator):
    input_index = input_details[0]["index"]
    output_index = output_details[0]["index"]

    y_true_all = []
    y_pred_all = []

    generator.reset()
    steps = len(generator)

    print(f"[INFO] Running {steps} batches…")

    for step in range(steps):
        x_batch, y_batch = next(generator)

        x_prepared = prepare_input(x_batch, input_details[0])

        try:
            interpreter.set_tensor(input_index, x_prepared)
            interpreter.invoke()
            preds = interpreter.get_tensor(output_index)
        except:
            preds = []
            for i in range(x_batch.shape[0]):
                x_i = prepare_input(x_batch[i:i+1], input_details[0])
                interpreter.set_tensor(input_index, x_i)
                interpreter.invoke()
                preds.append(interpreter.get_tensor(output_index)[0])
            preds = np.stack(preds, axis=0)

        y_true_all.append(y_batch)
        y_pred_all.append(preds)

        if (step + 1) % 20 == 0:
            print(f"[PROGRESS] {step+1}/{steps} batches")

    y_true_all = np.concatenate(y_true_all, axis=0)
    y_pred_all = np.concatenate(y_pred_all, axis=0)

    y_prob = tf.nn.softmax(y_pred_all, axis=1).numpy()

    print("[INFO] Computing macro AUC…")
    y_true_idx = np.argmax(y_true_all, axis=1)

    auc = roc_auc_score(
        y_true_idx,
        y_prob,
        multi_class="ovr",
        average="macro"
    )
    return auc


if __name__ == "__main__":
    print("[INFO] Loading CSV…")

    df = pd.read_csv(CSV_PATH)
    df["img_fullpath"] = df["img"].apply(lambda x: os.path.join(IMAGE_DIR, x))

    generator = ImageDataGenerator(
        preprocessing_function=preprocess_input
    ).flow_from_dataframe(
        dataframe=df,
        x_col="img_fullpath",
        y_col=label_cols,
        target_size=(224, 224),
        class_mode="raw",
        batch_size=16,
        shuffle=False
    )

    interpreter, input_details, output_details = load_tflite_interpreter(TFLITE_MODEL_PATH)

    auc = evaluate_auc(interpreter, input_details, output_details, generator)
    print(f"\n==============================")
    print(f"  FINAL MACRO AUC = {auc:.4f}")
    print(f"==============================\n")
