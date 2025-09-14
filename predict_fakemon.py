import requests
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from urllib.parse import urljoin
import numpy as np
import matplotlib.pyplot as plt
# from io import BytesIO
import os

BASE_URL = "https://phoenixdex.alteredorigin.net"
POKEMON_INDEX = urljoin(BASE_URL, "/pokemon/")
POKEMON_IMG = urljoin(BASE_URL, "/images/pokemon/")

MODEL_PATH = "models\poke_type_(64x64,0.6auc).h5"
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
    # df.to_csv("phoenixdex_pokemon.csv", index=False)
    return

if __name__ == "__main__":
    # scrape_index_page()
    
    df = pd.read_csv('data\phoenixdex_pokemon.csv')
    model = load_model(MODEL_PATH)

    from tensorflow.keras.preprocessing.image import ImageDataGenerator 
    label_cols = [f'label_{i}' for i in range(18)]
    df['img_fullpath'] = df['img'].apply(lambda fn: os.path.join('data\\fakemon-images', fn))
    full_datagen = ImageDataGenerator(rescale=1./255)
    full_gen = full_datagen.flow_from_dataframe(
        dataframe=df,
        x_col='img_fullpath',
        y_col=label_cols,
        target_size=(64,64),
        class_mode='raw',
        batch_size=16,
        shuffle=False
    )
    # print(model.evaluate(full_gen,verbose=1))
    # # print(df.head())
    # x, y = next(full_gen)
    # print(x.shape, y.shape)

    # plt.imshow(x[0])
    # plt.show()
    # x=1/0
    type_names = sorted(set(df['type1']).union(set(df['type2'].dropna())))
    tot = 0
    total = 0
    cor = 0
    fullcor=0
    for i, (x, y) in enumerate(full_gen): 
        batch_indices = full_gen.index_array[16*i:16*i+16]
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

            print(df.iloc[idx]['name'])
            print("  Predicted types:", pred_types)
            print("  Actual types   :", true_types)
            print("-" * 40)
            tot = tot+len(true_types)
            total= total+1
            if pred_types == true_types:
                fullcor=fullcor+1
            cor=cor+len(pred_types.intersection(true_types))
        if i == 18:
            break
        # break
    print("total",total)
    print("total types",tot)
    print("correct types", cor,cor/tot)
    print("full correct", fullcor, fullcor/total)
    