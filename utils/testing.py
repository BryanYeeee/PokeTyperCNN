import tensorflow as tf

models = ["D"]  # whichever you have

for m in models:
    keras_path = f"models/resnet50/resnet50_D.keras"
    tflite_path = f"poke-typer-backend/models/model_{m}2.tflite"

    print(f"Loading {keras_path}...")
    model = tf.keras.models.load_model(keras_path)

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16] 

    print("Converting...")
    tflite_model = converter.convert()

    with open(tflite_path, "wb") as f:
        f.write(tflite_model)

    print(f"Converted {keras_path} → {tflite_path}")
