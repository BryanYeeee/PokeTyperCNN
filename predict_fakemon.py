import requests
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from urllib.parse import urljoin
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

BASE_URL = "https://phoenixdex.alteredorigin.net"
POKEMON_INDEX = urljoin(BASE_URL, "/pokemon/")
POKEMON_IMG = urljoin(BASE_URL, "/images/pokemon/")

MODEL_PATH = "models/poke_type_v2.0_0.5acc.h5"
# MODEL_PATH = "models\classifier2.h5"
# MODEL_PATH = "models/poke_type_v2.1(0.44acc).h5"
# MODEL_PATH = "models/poke_type_70acc-99auc_v1.h5"

TYPES = {'bug': 0, 'dark': 1, 'dragon': 2, 'electric': 3, 'fairy': 4, 'fighting': 5, 'fire': 6, 'flying': 7, 'ghost': 8, 'grass': 9, 'ground': 10, 'ice': 11, 'normal': 12, 'poison': 13, 'psychic': 14, 'rock': 15, 'steel': 16, 'water': 17}
TYPE_INDEX = ['bug','dark','dragon','electric','fairy','fighting','fire','flying','ghost','grass','ground','ice','normal','poison','psychic','rock','steel','water']

def load_and_prepare_image(img_path, target_size=(32,32)):
    response = requests.get(POKEMON_IMG+img_path, stream=True)
    response.raise_for_status()  # make sure download was successful
    img = image.load_img(BytesIO(response.content), target_size=target_size)

    img_array = image.img_to_array(img)
    img_array = img_array.astype('float32') / 255.0
    img_array = np.expand_dims(img_array, axis=0)

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
        # if len(rows) > 15:
        #     break
        
    df = pd.DataFrame(rows, columns=["name","type1","type2","img"]+[f'label_{i}' for i in range(len(TYPES))])
    
    model = load_model(MODEL_PATH)
    # print('asd')
    # print(df.iloc[0, 3])
    # print(img_array)
    tot = 0
    total = 0
    cor = 0
    fullcor=0
    for i in range(len(df)):
        img_array = load_and_prepare_image(df.iloc[i, 3])
        predictions = model.predict(img_array, verbose=0)
        print(df.iloc[i,0])
        pred_labels = (predictions[0] >= 0.5).astype(int)
        if pred_labels.sum() == 0:
            top_indices = predictions[0].argsort()[-2:][::-1] 
            pred_labels = np.zeros_like(pred_labels)
            pred_labels[top_indices] = 1
        pred_types = {TYPE_INDEX[j] for j, val in enumerate(pred_labels) if val == 1}
        actual_types = {t for t in [df.iloc[i,1],df.iloc[i,2]] if pd.notna(t)}
        print('PRED:',pred_types)
        print('ACTL:',actual_types)
        tot = tot+len(actual_types)
        total= total+1
        if pred_types == actual_types:
            fullcor=fullcor+1
        cor=cor+len(pred_types.intersection(actual_types))
    print("total",total)
    print("total types",tot)
    print("correct types", cor,cor/tot)
    print("full correct", fullcor, fullcor/total)
    # print(df.iloc[0])
    return df

if __name__ == "__main__":
    scrape_index_page()
    # df = scrape_index_page()
    # print(f"Found {len(df)} Pokémon entries.")
    # # show first 30 entries
    # print(df.head(30))
    # optionally save to CSV
    # df.to_csv("phoenixdex_pokemon.csv", index=False)
    # print("Saved to phoenixdex_pokemon.csv")
