import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from utils.data_prep import get_data_generators
# Load model
# model = load_model("models\classifier1.h5")

# Get data generators again (so you have val_gen to test on)
train_gen, val_gen, full_gen, df = get_data_generators(
    "./data/pokemon.csv",
    "./data/pokemon-img/pokemon/pokemon/", img_size=(32,32)
)

# loss, acc, auc = model.evaluate(full_gen, verbose=1)

# print(f"Validation Loss: {loss:.4f}")
# print(f"Validation Accuracy: {acc:.4f}")
# print(f"Validation AUC: {auc:.4f}")

def exact_match_accuracy(y_true, y_pred):
    y_pred_binary = tf.cast(y_pred > 0.5, tf.int32)
    y_true_binary = tf.cast(y_true, tf.int32)
    matches = tf.reduce_all(tf.equal(y_true_binary, y_pred_binary), axis=1)
    return tf.reduce_mean(tf.cast(matches, tf.float32))
model2 = load_model("models/poke_type_70acc-99auc_v1.h5",custom_objects={'exact_match_accuracy': exact_match_accuracy})
# loss, auc, bin,a,p,d = model2.evaluate(full_gen, verbose=1)
# print(f"Validation Loss: {loss:.4f}")
# print(f"Validation auc: {auc:.4f}")
# print(f"Validation binacc: {bin:.4f}")


type_names = sorted(set(df['type1']).union(set(df['type2'].dropna())))
tot = 0
total = 0
cor = 0
fullcor=0
for i, (x, y) in enumerate(full_gen): 
    batch_indices = full_gen.index_array[32*i:32*i+32]
    probs = model.predict(x, verbose=0)
    # print(df.iloc[idx]['name'])
    # break
    
    for j, idx in enumerate(batch_indices):
        pred_labels = (probs[j] >= 0.5).astype(int)
        if pred_labels.sum() == 0:
            top_indices = probs[j].argsort()[-1:][::-1] 
            pred_labels = np.zeros_like(pred_labels)
            pred_labels[top_indices] = 1
        true_labels = y[j].astype(int)

        pred_types = {t for t, p in zip(type_names, pred_labels) if p == 1}
        true_types = {t for t, p in zip(type_names, true_labels) if p == 1}

        print(df.iloc[idx]['name'], [f"{x:.2f}" for x in probs[j]])
        print("  Predicted types:", pred_types)
        print("  Actual types   :", true_types)
        print("-" * 40)
        tot = tot+len(true_types)
        total= total+1
        if pred_types == true_types:
            fullcor=fullcor+1
        cor=cor+len(pred_types.intersection(true_types))
    if i == 23:
        break
    # break
print("total",total)
print("total types",tot)
print("correct types", cor,cor/tot)
print("full correct", fullcor, fullcor/total)
    



