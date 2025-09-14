import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from sklearn.model_selection import train_test_split



def get_data_generators(csv_dir, img_dir, img_size=(224,224)):
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

    # Prepare labels
    # labels = df[[c for c in df.columns if c.startswith("label_")]].values

    # # Create stratified splitter
    # msss = MultilabelStratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

    # for train_idx, val_idx in msss.split(df, labels):
    #     train_df = df.iloc[train_idx]
    #     val_df = df.iloc[val_idx]
    train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

    # Count type distribution in train/val
    # train_counts = train_df[[c for c in train_df.columns if c.startswith("label_")]].sum()
    # val_counts   = val_df[[c for c in val_df.columns if c.startswith("label_")]].sum()

    # print("Train counts:\n", train_counts)
    # print("\nVal counts:\n", val_counts)

    # # Normalize (percentage of dataset with each type)
    # train_pct = train_counts / len(train_df)
    # val_pct   = val_counts / len(val_df)

    # print("\nTrain distribution (%):\n", train_pct.round(3))
    # print("\nVal distribution (%):\n", val_pct.round(3))

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        zoom_range=[0.7,1],          # random zoom up to +-20%
        horizontal_flip=True,    # randomly flip horizontally
        rotation_range=20,       # small rotations
        brightness_range=[0.9, 1.3],
        fill_mode='nearest'      # fill gaps after shifts/rotations
    )

    val_datagen = ImageDataGenerator(rescale=1./255) 
    full_datagen = ImageDataGenerator(rescale=1./255)

    train_gen = train_datagen.flow_from_dataframe(
        train_df,
        x_col='img_path',
        y_col=label_cols,
        target_size=img_size,
        class_mode='raw',
        batch_size=16,
        shuffle=True
    )

    val_gen = val_datagen.flow_from_dataframe(
        val_df,
        x_col='img_path',
        y_col=label_cols,
        target_size=img_size,
        class_mode='raw',
        batch_size=16,
        shuffle=False
    )

    full_gen = full_datagen.flow_from_dataframe(
        dataframe=df,
        x_col='img_path',
        y_col=label_cols,
        target_size=img_size,
        class_mode='raw',
        batch_size=16,
        shuffle=False
    )

    
    # labels = df[[c for c in df.columns if c.startswith("label_")]].values
    # class_counts = labels.sum(axis=0)   # count positives for each type
    # total_samples = labels.shape[0]
    # num_classes = labels.shape[1]

    # class_weights = {}
    # for i in range(num_classes):
    #     if class_counts[i] > 0:
    #         class_weights[i] = total_samples / (num_classes * class_counts[i])
    #     else:
    #         class_weights[i] = 1.0

    return train_gen, val_gen, full_gen, df

if __name__ == '__main__':
    # train_gen, val_gen, full_gen,df = get_data_generators('./data/pokemon.csv', './data/pokemon-img/pokemon/pokemon/')

    # x_batch, y_batch = next(iter(train_gen))

    # print(x_batch.shape)  
    # print(y_batch.shape)  
    # print(y_batch[1])

    get_data_generators('./data/pokemon.csv', './data/pokemon-img/pokemon/pokemon/')