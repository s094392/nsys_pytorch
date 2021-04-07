import sys
import torch
import pyprof
import torch.cuda.profiler as profiler
from torchvision.models import resnet18


def main():
    pyprof.init()
    gpu_id = int(sys.argv[1])
    device = f"cuda:{gpu_id}"
    batch_size = int(sys.argv[2])

    model = resnet18().to(device)
    inputs = torch.randn(batch_size, 3, 224, 224).to(device)
    model(inputs)

if __name__ == "__main__":
    main()

