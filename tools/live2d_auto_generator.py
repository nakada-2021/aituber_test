
# tools/live2d_auto_generator.py

import argparse
import os
from PIL import Image, ImageDraw

def generate_dummy_parts(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    size = (512, 512)
    
    # 髪
    hair = Image.new("RGBA", size, (255, 0, 0, 128))
    ImageDraw.Draw(hair).ellipse((50, 50, 460, 300), fill=(255,0,0,200))
    hair.save(os.path.join(output_dir, "hair.png"))
    
    # 顔
    face = Image.new("RGBA", size, (255, 220, 200, 128))
    ImageDraw.Draw(face).ellipse((100, 100, 400, 400), fill=(255,220,200,200))
    face.save(os.path.join(output_dir, "face.png"))
    
    # 体
    body = Image.new("RGBA", size, (100, 100, 255, 128))
    ImageDraw.Draw(body).rectangle((150, 300, 350, 500), fill=(100,100,255,200))
    body.save(os.path.join(output_dir, "body.png"))
    
    print(f"パーツを{output_dir}に保存しました")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt', type=str, required=True)
    parser.add_argument('--output_dir', type=str, default="./output")
    args = parser.parse_args()
    
    print(f"プロンプト: {args.prompt} に基づいてLive2Dパーツを生成します（デモ版）")
    generate_dummy_parts(args.output_dir)
