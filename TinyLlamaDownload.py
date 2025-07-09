# download_model.py
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    local_dir="./tinyllama-model",
    local_dir_use_symlinks=False,
    token="your_huggingface_token_here" #Replace with your HuggingFace token if needed
)
