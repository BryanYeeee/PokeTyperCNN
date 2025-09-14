import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from sklearn.model_selection import train_test_split

def get_data_generators(csv_dir, img_dir):
    df = pd.read_csv(csv_dir)
    df = df.drop(df.index[721:801])
    df = df[['name','type1','type2', 'pokedex_number']]
    all_types = sorted(set(df['type1']).union(set(df['type2']) - {np.nan}))
    type_to_idx = {t: i for i, t in enumerate(all_types)}
    print(type_to_idx)

    def encode_types(row):
        vector = np.zeros(len(all_types), dtype=np.float32)
        vector[type_to_idx[row['type1']]] = 1
        if pd.notna(row['type2']):
            vector[type_to_idx[row['type2']]] = 1
        return vector
    labels = np.stack(df.apply(encode_types, axis=1).values)
    for i in range(labels.shape[1]):
        df[f'label_{i}'] = labels[:, i]
    label_cols = [f'label_{i}' for i in range(labels.shape[1])]

    df['img_path'] = df['pokedex_number'].apply(lambda x: f"{img_dir}{x}.png")
    df = df.drop('pokedex_number', axis=1)

    df.loc[646, 'img_path'] = img_dir + '647-ordinary.png'
    df.loc[644, 'img_path'] = img_dir + '645-incarnate.png'
    df.loc[641, 'img_path'] = img_dir + '642-incarnate.png'
    df.loc[640, 'img_path'] = img_dir + '641-incarnate.png'
    df.loc[585, 'img_path'] = img_dir + '586-autumn.png'
    df.loc[584, 'img_path'] = img_dir + '585-autumn.png'
    df.loc[554, 'img_path'] = img_dir + '555-standard.png'
    df.loc[549, 'img_path'] = img_dir + '550-blue-striped.png'
    df.loc[492, 'img_path'] = img_dir + '493-normal.png'
    df.loc[491, 'img_path'] = img_dir + '492-land.png'
    df.loc[486, 'img_path'] = img_dir + '487-origin.png'
    df.loc[422, 'img_path'] = img_dir + '423-east.png'
    df.loc[421, 'img_path'] = img_dir + '422-east.png'
    df.loc[420, 'img_path'] = img_dir + '421-overcast.png'
    df.loc[412, 'img_path'] = img_dir + '413-plant.png'
    df.loc[411, 'img_path'] = img_dir + '412-plant.png'
    df.loc[385, 'img_path'] = img_dir + '386-normal.png'

    # import os
    # missing_files = df.loc[~df['img_path'].apply(os.path.exists), 'img_path']
    # print("Invalid image files found:", len(missing_files))
    # print(missing_files.tolist())
    # print(df.columns)

    train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        zoom_range=0,          # random zoom up to +-20%
        horizontal_flip=True,    # randomly flip horizontally
        vertical_flip=True,
        rotation_range=30,       # small rotations
        brightness_range=[0.7, 1.3],
        fill_mode='nearest'      # fill gaps after shifts/rotations
    )

    val_datagen = ImageDataGenerator(rescale=1./255) 
    full_datagen = ImageDataGenerator(rescale=1./255)

    train_gen = train_datagen.flow_from_dataframe(
        train_df,
        x_col='img_path',
        y_col=label_cols,
        target_size=(128, 128),
        class_mode='raw',
        batch_size=32,
        shuffle=True
    )

    val_gen = val_datagen.flow_from_dataframe(
        val_df,
        x_col='img_path',
        y_col=label_cols,
        target_size=(128, 128),
        class_mode='raw',
        batch_size=32,
        shuffle=False
    )

    full_gen = full_datagen.flow_from_dataframe(
        dataframe=df,
        x_col='img_path',
        y_col=label_cols,
        target_size=(128, 128),
        class_mode='raw',
        batch_size=32,
        shuffle=False
    )

    return train_gen, val_gen, full_gen, df

# train_gen, val_gen, full_gen,df = get_data_generators('./data/pokemon.csv', './data/pokemon-img/pokemon/pokemon/')

# x_batch, y_batch = next(iter(train_gen))

# print(x_batch.shape)  
# print(y_batch.shape)  
# print(y_batch[1])

# get_data_generators('./data/pokemon.csv', './data/pokemon-img/pokemon/pokemon/')