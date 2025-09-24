"""
The archive contains six files tracesN.bin. These files contain six datasets of power traces measured during PRESENT encryption. The following holds:

    Every file tracesN.bin contains 1,000 power traces. Each power trace consists of 4,200 samples. Every file therefore contains 4,200 x 1,000 power samples.
    Every power sample is a signed 16bit integer (int16_t, signed short). Every file is therefore 2 x 4,200 x 1,000 = 8,400,000 bytes.
    All the data are saved in a "binary format", little-endian (i.e., what you would expect while working on a classic PC (Intel, AMD)).
    In every file, first, there are 4,200 samples measured during the first encryption. After that, there are 4,200 samples measured during the second encryption. And so on.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def plot_single_trace(src: np.ndarray):
    """ Task 1 """
    plt.plot(src, marker='o', markersize=2, linestyle='None')
    plt.title('Single Power Trace')
    plt.xlabel('Sample Index')
    plt.ylabel('Power Sample Value')
    plt.grid()
    plt.show()
    plt.clf()

def plot_n_traces(src: np.ndarray, n: int):
    """ Task 2 """
    for i in range(n):
        plt.plot(src[i,:], marker='o', markersize=2, linestyle='None')
    plt.title(f'{n} Power Traces')
    plt.xlabel('Sample Index')
    plt.ylabel('Power Sample Value')
    plt.legend([f'Trace {i+1}' for i in range(n)])
    plt.grid()
    plt.show()
    plt.clf()

def plot_histograms(src: np.ndarray):
    """
    Task 3
    ... first thing we should do, when we examine a random variable, is to plot a histogram.
    In any dataset, randomly select three sampling points. At these points, plot the histograms of consumption (three in total), each based on all 1,000 samples, and try to guess what statistical distribution you see. Does it make sense to calculate e.g. the mean or variance for such a distribution?
    ------------------------------------------------------------------------------------------------------------------ 
    Task answer:
    We see the normal distribution, therefore it makes sense to calcualte the mean and variance.
    """
    rand_var01 = src[:, 2]
    rand_var02 = src[:, 42]
    rand_var03 = src[:, 468]
    # plot as subplots
    plt.subplot(3, 1, 1)
    plt.hist(rand_var01, bins=50, edgecolor='black')
    plt.title('Histogram of Power Samples at Index 2')
    plt.xlabel('Power Sample Value')
    plt.ylabel('Frequency')
    plt.grid()
    plt.subplot(3, 1, 2)
    plt.hist(rand_var02, bins=50, edgecolor='black')
    plt.title('Histogram of Power Samples at Index 42')
    plt.xlabel('Power Sample Value')
    plt.ylabel('Frequency')
    plt.grid()
    plt.subplot(3, 1, 3)
    plt.hist(rand_var03, bins=50, edgecolor='black')
    plt.title('Histogram of Power Samples at Index 468')
    plt.xlabel('Power Sample Value')
    plt.ylabel('Frequency')
    plt.grid()
    plt.tight_layout()
    plt.show()
    plt.clf()

def calc_stats(src: np.ndarray):
    """
    Task 4
    The following holds for the six available datasets:

        Each dataset contains power traces measured during PRESENT encryption on an FPGA.
        Consumption within each individual dataset was measured during either
            encryption of randomly selected plaintexts, or
            encryption of a fixed constant plaintext.

    These datasets are easily distinguishable using the most basic statistical tools.

    Your task is to decide which datasets were measured when encrypting random data, and which datasets were measured when encrypting the fixed constant data. Try to justify your claims with proper statistical reasoning.
    --------------------------------------------------------------------------------------------------------------------------------
    My questions:
    1. The whole dataset has been rolled to be random/fixed or there was a roll between random/fixed before each encryption within dataset.
    -> The whole dataset has been rolled to be random/fixed
    
    2. Is there a difference between calculating means, variances for each encryption and then averaging them
    in comparison to calculating means, variances of the whole dataset?
    -> mean of means is a mean, so no. mean of vars is different than var of the whole dataset though
    --------------------------------------------------------------------------------------------------------------------------------
    Task answer:
    1. First try calculating variances, means
    -> 1, 2, 4 are from the random data set: each have variances of random variables of roughly 9'000'000 
    -> 3, 5, 6 are from the constant data set: each have lower variances of random variables at around 8'000'000
    Furthermore the means (positive, negative) also correspond to these two groupings.
    """
    # Random variable:= one column across all encryptions, that is, one point in time across all encryptions
    print(f'Mean: {src.mean()}') # Mean of means of each random variable respectively, is the same as a mean of everything

    vars = []
    for i in range(src.shape[1]):
        vars.append(np.var(src[:,i]))
    print(f'Var: {np.mean(vars)}') # Mean of variances of each random variable respectively

def main():
    for file in Path('ni-hsc-lab-01-data').glob('traces*.bin'):
        print(file)
        data = np.fromfile(file, dtype=np.int16)
        data = data.reshape((1000, 4200))
        calc_stats(data)
        print('-'*40)

    # plot_single_trace(data[0])
    # plot_n_traces(data, 5)
    # plot_histograms(data)

if __name__ == '__main__':
    main()
