
#!/bin/bash

# Mistral-7B-Instruct-v0.2 Q2_K（約2.8GB）の自動ダウンロード

REPO_ID=TheBloke/Mistral-7B-Instruct-v0.2-GGUF
FILENAME=mistral-7b-instruct-v0.2.Q2_K.gguf
LOCAL_DIR=./models

mkdir -p $LOCAL_DIR

huggingface-cli download $REPO_ID $FILENAME --local-dir $LOCAL_DIR

echo "ダウンロード完了: $LOCAL_DIR/$FILENAME"
