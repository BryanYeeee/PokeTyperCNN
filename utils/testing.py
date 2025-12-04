import tensorflow as tf

models = ["A"]  # whichever you have

for m in models:
    keras_path = f"poke-typer-backend/models/model_{m}.h5"
    tflite_path = f"poke-typer-backend/models/model_{m}.tflite"

    model = tf.keras.models.load_model(keras_path)

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]  # reduces RAM
    tflite_model = converter.convert()

    with open(tflite_path, "wb") as f:
        f.write(tflite_model)

    print(f"Converted {keras_path} → {tflite_path}")
