import requests
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from urllib.parse import urljoin
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.applications.efficientnet import preprocess_input
import os

BASE_URL = "https://phoenixdex.alteredorigin.net"
POKEMON_INDEX = urljoin(BASE_URL, "/pokemon/")
POKEMON_IMG = urljoin(BASE_URL, "/images/pokemon/")

# MODEL_PATH = "models/basic/poke_type_(32x32,0.6auc).h5"
# MODEL_PATH = ""
# MODEL_PATH = "models\classifier2.h5"
# MODEL_PATH = "models/poke_type_v2.1(0.44acc).h5"
# MODEL_PATH = "models/poke_type_70acc-99auc_v1.h5"

TYPES = {'bug': 0, 'dark': 1, 'dragon': 2, 'electric': 3, 'fairy': 4, 'fighting': 5, 'fire': 6, 'flying': 7, 'ghost': 8, 'grass': 9, 'ground': 10, 'ice': 11, 'normal': 12, 'poison': 13, 'psychic': 14, 'rock': 15, 'steel': 16, 'water': 17}
TYPE_INDEX = ['bug','dark','dragon','electric','fairy','fighting','fire','flying','ghost','grass','ground','ice','normal','poison','psychic','rock','steel','water']

def load_and_prepare_image(img_path, target_size=(64,64)):
    # response = requests.get(img_path, stream=True)
    # response.raise_for_status()  # make sure download was successful
    # img = image.load_img(BytesIO(response.content), target_size=target_size)
    img = image.load_img(img_path, target_size=target_size)

    img_array = image.img_to_array(img)
    img_array = img_array.astype('float32') / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # plt.imshow(img_array[0])
    # plt.show()
    return img_array


def scrape_index_page(index_url=POKEMON_INDEX):
    resp = requests.get(index_url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    rows = []
    # seen = set()
    for poke in soup.find_all(class_="mini-poketable"):
        cur = {}
        cur['name'] = poke.strong.string
        cur['img'] = poke.find("img")["src"].split("/")[-1]
        type = poke.find_all(class_='type-icon')

        vector = np.zeros(len(TYPES), dtype=np.float32)
        vector[TYPES[type[0].string.lower()]] = 1
        cur['type1']=type[0].string.lower()
        if len(type) > 1:
            cur['type2']=type[1].string.lower()
            vector[TYPES[type[1].string.lower()]] = 1

        for i in range(len(TYPES)):
            cur[f'label_{i}'] = vector[i]

        rows.append(cur)
        
        # local_path = os.path.join('data\\fakemon-img', cur['img'])
        # if not os.path.exists(local_path):
        IMAGE_DIR = "C:/Users/halod/Documents/Projects/poke_classy/images/"
        response = requests.get(POKEMON_IMG+cur['img'], stream=True, timeout=15)
        response.raise_for_status()
        with open(IMAGE_DIR+cur['img'], "wb") as f:
            f.write(response.content)
        
        # img_array = load_and_prepare_image(cur['img'])
        # return
        # if len(rows) > 15:
        #     break
        
    df = pd.DataFrame(rows, columns=["name","type1","type2","img"]+[f'label_{i}' for i in range(len(TYPES))])
    df.to_csv("phoenixdex_pokemon.csv", index=False)
    return

if __name__ == "__main__":
    # scrape_index_page()
    
    df = pd.read_csv('data\phoenixdex_pokemon.csv')
    model = load_model('models\poke_efficnet_(224,0.69auc).h5')
    model2 = load_model('models\poke_efficnet_(224,0.70auc).h5')
    model3 = load_model('models\poke_efficnet(0.716auc).h5')

    from tensorflow.keras.preprocessing.image import ImageDataGenerator 
    label_cols = [f'label_{i}' for i in range(18)]
    df['img_fullpath'] = df['img'].apply(lambda fn: os.path.join('data\\fakemon-images-blackbg', fn))
    full_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input)
    full_gen = full_datagen.flow_from_dataframe(
        dataframe=df,
        x_col='img_fullpath',
        y_col=label_cols,
        target_size=(224,224),
        class_mode='raw',
        batch_size=16,
        shuffle=False
    )
    # print(df.head())
    # x, y = next(full_gen)
    # x, y = next(full_gen)
    # print(x.shape, y.shape)

    # plt.imshow(x[0].astype("uint8"))
    # plt.show()

    # x=1/0
    type_names = sorted(set(df['type1']).union(set(df['type2'].dropna())))
    from collections import Counter

    venn_counts = Counter()  # counts across dataset
    c = Counter()  # counts across dataset

    for i, (x, y) in enumerate(full_gen): 
        batch_indices = full_gen.index_array[16*i:16*i+16]
        probs1 = model.predict(x, verbose=0)
        probs2 = model2.predict(x, verbose=0)
        probs3 = model3.predict(x, verbose=0)

        for j, idx in enumerate(batch_indices):
            # probs1 = [probs1[k] + probs2[k] for k in range(len(probs1))]
            # pred1 = (probs1[j] > 100000).astype(int)
            # top_indices = probs1[j].argsort()[-2:][::-1]
            # pred1[top_indices] = 1
            # binarize predictions
            pred1 = (probs1[j] >= 0.5).astype(int)
            if pred1.sum() == 0:
                top_indices = probs1[j].argsort()[-2:][::-1]
                pred1[top_indices] = 1

            pred2 = (probs2[j] >= 0.5).astype(int)
            if pred2.sum() == 0:
                top_indices2 = probs2[j].argsort()[-2:][::-1]
                pred2[top_indices2] = 1

            pred3 = (probs3[j] >= 0.5).astype(int)
            if pred3.sum() == 0:
                top_indices3 = probs3[j].argsort()[-2:][::-1]
                pred3[top_indices3] = 1

            true = y[j].astype(int)
            

            set1 = {t for t, p in zip(type_names, pred1) if p == 1}
            set2 = {t for t, p in zip(type_names, pred2) if p == 1}
            set3 = {t for t, p in zip(type_names, pred3) if p == 1}
            true_set = {t for t, p in zip(type_names, true) if p == 1}

            # --- Venn counts ---
            c["model1_correct"] += len(set3 & true_set)
            c["model1_perfect"] += 1 if set3 == true_set else 0
            # venn_counts["model2_correct"] += len(set2 & true_set)
            # venn_counts["model2_perfect"] += 1 if set2 == true_set else 0
            # venn_counts["model1_only_correct"] += len((set1 & true_set) - set2)
            # venn_counts["model1_only_perfect"] += 1 if set2 == true_set and set1 != set2 else 0
            # venn_counts["model2_only_correct"] += len((set2 & true_set) - set1)
            # venn_counts["model2_only_perfect"] += 1 if set1 == true_set and set1 != set2 else 0
            # venn_counts["both_correct"]   += len((set1 & set2) & true_set)
            # venn_counts["both_perfect"]   += 1 if set2 == true_set and set1 == set2 else 0
            # venn_counts["none"]   += 1 if len((set1 & set2) & true_set) == 0 else 0
            only1 = (set1 - set2 - set3)
            only2 = (set2 - set1 - set3)
            only3 = (set3 - set1 - set2)
            both12 = (set1 & set2) - set3
            both13 = (set1 & set3) - set2
            both23 = (set2 & set3) - set1
            all123 = set1 & set2 & set3

            venn_counts['100'] += len(only1)
            venn_counts['010'] += len(only2)
            venn_counts['001'] += len(only3)
            venn_counts['110'] += len(both12)
            venn_counts['101'] += len(both13)
            venn_counts['011'] += len(both23)
            venn_counts['111'] += len(all123)

            # venn_counts["XXmodel1_only"] += len(set1 - set2)
            # venn_counts["XXmodel2_only"] += len(set2 - set1)
            # venn_counts["XX3&2"]        += len(set1 & set2)
            print(df.iloc[idx]['name']) 
            print(" Predicted types :", set1) 
            print(" Predicted types2:", set2) 
            print(" Predicted types3:", set3) 
            print(" Actual types :", true_set) 
            print("-" * 40)
        if i == 18:  # safety break
            break

    # print("Venn-style stats:")
    print(c)
    from matplotlib_venn import venn3
    import matplotlib.pyplot as plt
    venn3(subsets=venn_counts, set_labels=("Model 1", "Model 2", "Model 3"))
    plt.show()

    print(model.evaluate(full_gen,verbose=1))
    