
# tools/live2d_auto_generator.py

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt', type=str, required=True)
    args = parser.parse_args()
    print(f"生成開始：{args.prompt}")
    print("パーツ分け完了（ダミー出力）")

if __name__ == "__main__":
    main()
