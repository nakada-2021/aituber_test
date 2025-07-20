
# tools/auto_psd_generator.py

from psd_tools import PSDImage, Group, Layer
from PIL import Image
import os

def create_psd(output_dir, save_path):
    layers = []
    parts = ["body", "face", "hair"]
    for part in parts:
        img_path = os.path.join(output_dir, f"{part}.png")
        if os.path.exists(img_path):
            img = Image.open(img_path).convert("RGBA")
            layer = Layer.from_PIL(img, name=part)
            layers.append(layer)

    group = Group(name="Character", layers=layers)
    psd = PSDImage(size=img.size, layers=[group])
    psd.save(save_path)
    print(f"PSD saved to {save_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, default="./output")
    parser.add_argument('--save_path', type=str, default="./live2d_model.psd")
    args = parser.parse_args()

    create_psd(args.input_dir, args.save_path)
