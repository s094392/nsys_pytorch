import torch
from time import time
import torch.cuda.profiler as profiler
import pyprof

#import torch.autograd.profiler as profiler
#import torchprof
import sys
import torch.nn as nn

gpu_id = int(sys.argv[1])
device = f"cuda:{gpu_id}"

def measure(N):
    pyprof.init()
    w, h, c, n, k, s, r, pad_w, pad_h, wstride, hstride = (56, 56, 64, 32, 128, 3, 3, 1, 1, 2, 2)
    conv = nn.Conv2d(c, k, (s, r), (wstride, hstride), (pad_w, pad_h)).to(device)
    inputs = torch.randn(n, c, w, h).to(device)
    conv(inputs)

measure(100)

