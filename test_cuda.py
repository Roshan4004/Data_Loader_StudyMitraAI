import torch
import datetime

# Disable problematic backends (default config)
torch.backends.cudnn.enabled = True
torch.backends.cuda.enable_flash_sdp(False)
torch.backends.cuda.enable_math_sdp(True)
torch.backends.cuda.enable_mem_efficient_sdp(False)

if True:  # Force indentation block
    _orig_topk = torch.topk
    def _patched_topk(tensor, *args, **kwargs):
        device = tensor.device
        values, indices = _orig_topk(tensor.cpu(), *args, **kwargs)
        return values.to(device), indices.to(device)
    torch.topk = _patched_topk

from langchain_huggingface import HuggingFaceEmbeddings

def create_embedding(text):
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-large-en-v1.5",
        model_kwargs={
            "device": "cuda",
            # "trust_remote_code": False,
            # "dtype": "torch.float16"
        },
        encode_kwargs={"normalize_embeddings": True},
        show_progress=True
    )
    ok=embeddings.embed_query(text)
    print(ok)
    print(datetime.datetime.now())
    return ok

