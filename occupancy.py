import sys
from math import ceil, floor

sharedSize = 65536
CUDA_version = 11.1


def occupancy(MyThreadCount, MyRegCount, MySharedMemory, computeCapability):
    def roundup(x, factor):
        return int(ceil(x / factor)) * factor

    def rounddown(x, factor):
        return int(floor(x / factor)) * factor

    if computeCapability == 6.1:
        limitThreadsPerWarp = 32
        limitWarpsPerMultiprocessor = 64
        limitBlocksPerMultiprocessor = 32
        limitThreadsPerMultiprocessor = 2048
        maxThreadsPerBlock = 1024
        limitTotalRegisters = 65536
        limitRegsPerBlock = 65536
        limitRegsPerThread = 255
        limitTotalSharedMemory = 65536
        limitSharedMemoryPerBlock = 49152
        myAllocationSize = 256
        myAllocationGranularity = 'warp'
        mySharedMemAllocationSize = 256
        myWarpAllocationGranularity = 4
        CUDASharedMemory = 0
    elif computeCapability == 8.6:
        limitThreadsPerWarp = 32
        limitWarpsPerMultiprocessor = 48
        limitBlocksPerMultiprocessor = 16
        limitThreadsPerMultiprocessor = 1536
        maxThreadsPerBlock = 1024
        limitTotalRegisters = 65536
        limitRegsPerBlock = 65536
        limitRegsPerThread = 255
        limitTotalSharedMemory = 65536
        limitSharedMemoryPerBlock = 65536
        myAllocationSize = 256
        myAllocationGranularity = "warp"
        mySharedMemAllocationSize = 128
        myWarpAllocationGranularity = 4
        CUDASharedMemory = 1024

    MyWarpsPerBlock = ceil(MyThreadCount / limitThreadsPerWarp)
    MyRegsPerBlock = MyRegsPerBlock = ceil(
        ceil(MyWarpsPerBlock, myWarpAllocationGranularity) * MyRegCount *
        limitThreadsPerWarp, myAllocationSize
    ) if myAllocationGranularity == 'block' else MyWarpsPerBlock
    MySharedMemPerBlock = roundup(MySharedMemory, mySharedMemAllocationSize)

    C42 = limitWarpsPerMultiprocessor
    C43 = limitRegsPerBlock if myAllocationGranularity == 'block' else rounddown(
        limitRegsPerBlock /
        roundup(MyRegCount * limitThreadsPerWarp, myAllocationSize),
        myWarpAllocationGranularity)
    C44 = limitSharedMemoryPerBlock

    limitBlocksDueToWarps = min(
        (limitBlocksPerMultiprocessor,
         rounddown(limitWarpsPerMultiprocessor / MyWarpsPerBlock, 1)))
    limitBlocksDueToRegs = 0 if MyRegCount > limitRegsPerThread else floor(
        C43 / MyRegsPerBlock) * floor(
            limitTotalRegisters / limitRegsPerBlock
        ) if MyRegCount > 0 else limitBlocksPerMultiprocessor
    limitBlocksDueToSMem = 7

    B21 = min(
        (limitBlocksDueToWarps, limitBlocksDueToRegs, limitBlocksDueToSMem))
    B20 = B21 * MyWarpsPerBlock
    B19 = B20 * limitThreadsPerWarp
    ans = B20 / limitWarpsPerMultiprocessor
    return ans


if __name__ == "__main__":
    computeCapability = float(sys.argv[1])
    print(
        occupancy(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]),
                  computeCapability))
