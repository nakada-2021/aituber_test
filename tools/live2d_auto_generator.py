
# tools/live2d_auto_generator.py

import openai
import argparse
import os
from PIL import Image, ImageDraw

def query_llm(prompt):
    system_prompt = """
あなたはLive2D用立ち絵パーツをPillowで生成するアシスタントです。
以下の形式でコードを生成してください：

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
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"system","content":system_prompt},
                  {"role":"user","content":prompt}]
    )
    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt', type=str, required=True)
    parser.add_argument('--output_dir', type=str, default="./output")
    args = parser.parse_args()

    size = (512,512)
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    print("LLMに問い合わせ中...")
    generated_code = query_llm(args.prompt)
    print("生成されたコード：")
    print(generated_code)

    # 実行用の環境を制限
    exec_env = {"Image": Image, "ImageDraw": ImageDraw, "size": size, "output_dir": output_dir, "os": os}
    exec(generated_code, exec_env)
