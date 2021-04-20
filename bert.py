import sys
import torch
import pyprof
import torch.cuda.profiler as profiler
from transformers import AutoTokenizer, AutoModel

def main():
    gpu_id = int(sys.argv[1])
    device = f"cuda:{gpu_id}"
    batch_size = int(sys.argv[2])
   
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModel.from_pretrained("bert-base-uncased").to(device)
   
    sentences = ["Hello world!"] * batch_size
    inputs = tokenizer(sentences, return_tensors="pt").to(device)

    pyprof.init()
    outputs = model(**inputs)
    print(outputs)

if __name__ == "__main__":
    main()

