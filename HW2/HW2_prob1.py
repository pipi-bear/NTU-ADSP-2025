import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt

"""
Check lecture ppt ADSP_Write2 p.106-113 for the implementation details
- The steps are based on p.108
"""

k = input("Enter the value of k: ")
k = int(k)

# Step: 1. Sampling H_d(\frac{m}{N})
# the interval of h[n] is n \in [0, N-1]
# N is the number of points of the filter
N = 2*k + 1
H_d = np.zeros(N, dtype=complex)
for m in range(N):
    F = m / N                   # F: normalized frequency
    if m == k or m == (k+1):    # set transition band
        H_d[m] = 0.6            # set arbitrary value
    else:
        if F <= 0.5:
            H_d[m] = 1j * 2 * np.pi * F
        else:
            H_d[m] = 1j * 2 * np.pi * (F - 1)


# Step: 2. Get r_1[n]
# r_1[n] = \frac{1}{N} \sum_{m=0}^{N-1} H_d(\frac{m}{N}) e^{j \frac{2\pi}{\frac{m}{N}} n}
# i.e. r_1[n] = inverse discrete fourier transform of H_d(\frac{m}{N})
r_1 = np.fft.ifft(H_d)

# Step: 3. Get r[n]
# explain: we use fftshift to shift r_1[n] from [0, N-1] to [-k, k]
r = np.fft.fftshift(r_1)

# Step: 4. Get h[n]
# h[n] = r[n - k]
# The shifting of r[n] by k is done in the plot function
h = r

# Frequency Response R(F)
F_values = np.linspace(0, 1, 1000)
R = np.array([np.sum(r * np.exp(-1j * 2 * np.pi * F * np.arange(-k, k + 1))) for F in F_values])

# Plotting additional information to check the result (r_1[n], r[n], h[n])
plt.figure(figsize=(10, 10))

# Plot r_1[n]
plt.subplot(3, 1, 1)
plt.stem(np.arange(0, 2*k+1), r_1, linefmt='g-', markerfmt='go', basefmt=' ')
plt.title("$r_1[n]$")
plt.axhline(0, color='black', linewidth=0.8)  
plt.xlim([-N, N])  

# Plot r[n]
plt.subplot(3, 1, 2)
plt.stem(np.arange(-k, k+1), r, linefmt='b-', markerfmt='bo', basefmt=' ')
plt.title("$r[n]$")
plt.axhline(0, color='black', linewidth=0.8)  
plt.xlim([-N, N])  

# Plot h[n]
plt.subplot(3, 1, 3)
plt.stem(np.arange(0, 2*k+1), h, linefmt='r-', markerfmt='ro', basefmt=' ')
plt.title("$h[n]$")
plt.axhline(0, color='black', linewidth=0.8)  
plt.xlim([-N, N])  

plt.tight_layout()


# Plotting HW required plots

# (i) Impulse response (imaginary part of r[n])
plt.figure(figsize=(10, 10))
plt.subplot(2, 1, 1)
plt.stem(np.arange(-k, k+1), r, linefmt='b-', markerfmt='bo', basefmt=' ')
plt.title("Impulse response")
plt.xlabel("n")
plt.ylabel("$r[n]$")
plt.axhline(0, color='black', linewidth=0.8)  
plt.axvline(x=-k, color='gray', linestyle=':', alpha=0.6)
plt.axvline(x=k, color='gray', linestyle=':', alpha=0.6)
plt.text(-k, plt.ylim()[1], f'n = {-k}', horizontalalignment='right', verticalalignment='bottom')
plt.text(k, plt.ylim()[1], f'n = {k}', horizontalalignment='left', verticalalignment='bottom')
plt.xlim([-N, N])

# (ii) Frequency response (imaginary part of R(F))
plt.subplot(2, 1, 2)
plt.plot(F_values, np.imag(R), 'r', label='$Im(R(F))$')
plt.plot(np.arange(N) / N, np.imag(H_d), 'go', label='$Im(H_d(F))$')
plt.title("Frequency Response")
plt.xlabel("F (Normalized Frequency)")
plt.ylabel("Imaginary part of $R(F)$")
plt.legend()
plt.xlim([0, 1])

plt.tight_layout()
plt.show()

