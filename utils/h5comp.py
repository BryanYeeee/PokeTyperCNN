import h5py
from tensorflow import keras

# 1. Load your Keras model
model = keras.models.load_model("models/resnet50/resnet50,0.72auc.keras")  # or "model.h5"

# 2. Save compressed manually using h5py
with h5py.File("comp_resnet50,0.72auc.keras", "w") as f:
    for layer in model.layers:
        weights = layer.get_weights()
        if weights:  # skip layers without weights
            grp = f.create_group(layer.name)
            for i, w in enumerate(weights):
                # compress using gzip (can also try 'lzf')
                grp.create_dataset(f"weight_{i}", data=w, compression="gzip", compression_opts=9)
