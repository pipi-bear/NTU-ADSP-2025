"""
ADSP HW5 Problem 1

Author: Luo Chunchou
Student ID: R13922136
Date: 2025-06-11

This script is used to compute the FFT of two real sequences using a single complex FFT.
"""


import numpy as np
import matplotlib.pyplot as plt

def fftreal(f1, f2):
    """
    Compute FFT of two real sequences using a single complex FFT
    
    Args:
        f1: First real sequence
        f2: Second real sequence
        
    Returns:
        F1, F2: FFT results of the two sequences
    """
    N = len(f1)
    if N != len(f2):
        raise ValueError("Input length mismatch")

    # Combine the two real sequences into one complex sequence
    f3 = f1 + 1j * f2
    # Perform FFT on the combined complex sequence
    F3 = np.fft.fft(f3)
    
    # Extract the FFT results of the two sequences
    F1 = np.zeros(N, dtype=np.complex64)
    F2 = np.zeros(N, dtype=np.complex64)
    
    F1[0] = (F3[0] + np.conj(F3[0])) / 2
    F2[0] = (F3[0] - np.conj(F3[0])) / (2*1j)
    
    for m in range(1, N // 2):
        F1[m] = (F3[m] + np.conj(F3[N - m])) / 2
        F2[m] = (F3[m] - np.conj(F3[N - m])) / (2*1j)
        F1[N - m] = np.conj(F1[m])
        F2[N - m] = -np.conj(F2[m])
    
    if N % 2 == 0:
        F1[N // 2] = (F3[N // 2] + np.conj(F3[N // 2])) / 2
        F2[N // 2] = (F3[N // 2] - np.conj(F3[N // 2])) / (2*1j)
    
    return F1, F2

def create_comparison_plot(f, F1, F2):
    """
    Create a comparison plot of two FFT results
    
    Args:
        f: Frequency vector
        F1: FFT of signal x
        F2: FFT of signal y
    """
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(f, np.abs(F1))
    plt.title('Fx')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(f, np.abs(F2))
    plt.title('Fy')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

def main():
    Fs = 1000                   # Sampling frequency (Hz)
    T = 1 / Fs                  # Sampling period
    L = 1024                    # Length of the signal
    t = np.arange(L) * T        # Time vector
    f = Fs * np.arange(L) / L   # Frequency vector
    
    # Example: Two distinct frequency signals
    f1 = np.cos(2 * np.pi * 100 * t)  # 100 Hz cosine
    f2 = np.sin(2 * np.pi * 200 * t)  # 200 Hz sine
    
    # Compute and plot FFT
    F1, F2 = fftreal(f1, f2)
    create_comparison_plot(f, F1, F2)

if __name__ == "__main__":
    main()