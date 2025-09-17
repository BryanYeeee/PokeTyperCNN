from PIL import Image
import os

def flatten_to_black(input_path, output_path):
    """Flatten transparent PNGs to RGB with black background."""
    img = Image.open(input_path)
    if img.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", img.size, (0, 0, 0))  # black background
        bg.paste(img, mask=img.split()[-1])         # alpha mask
        bg.save(output_path, "PNG")
    else:
        img.convert("RGB").save(output_path, "PNG")


def preprocess_fakemon_images(fake_df, input_dir="./data/fakemon-images",
                              output_dir="./data/fakemon-images-blackbg"):
    """Ensure all fakemon images have black backgrounds."""
    os.makedirs(output_dir, exist_ok=True)
    new_paths = []
    for fn in fake_df["img"]:
        in_path = os.path.join(input_dir, fn)
        out_path = os.path.join(output_dir, fn)
        if not os.path.exists(out_path):  # only process once
            flatten_to_black(in_path, out_path)
        new_paths.append(out_path)
    fake_df["img_fullpath"] = new_paths
    return fake_df

import pandas as pd

fake_df = pd.read_csv('./data/phoenixdex_pokemon.csv')
fake_df = preprocess_fakemon_images(fake_df,
                                    input_dir="./data/fakemon-images",
                                    output_dir="./data/fakemon-images-blackbg")
