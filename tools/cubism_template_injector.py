
# tools/cubism_template_injector.py

import shutil
import os

def replace_psd(template_dir, new_psd, output_dir):
    shutil.copytree(template_dir, output_dir, dirs_exist_ok=True)
    target_psd = os.path.join(output_dir, "model.psd")
    shutil.copy(new_psd, target_psd)
    print(f"Replaced PSD in {output_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--template_dir', type=str, default="./cubism_template")
    parser.add_argument('--new_psd', type=str, default="./live2d_model.psd")
    parser.add_argument('--output_dir', type=str, default="./cubism_model_output")
    args = parser.parse_args()

    replace_psd(args.template_dir, args.new_psd, args.output_dir)
