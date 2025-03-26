# HW1: Problem 1

import numpy as np
import matplotlib.pyplot as plt


N = 19                  # filter length 
k = 9                   # (N-1)/2 = 9
W_p = 1                 # weighting function for passband
W_s = 0.6               # weighting function for stopband

# Normalized frequency for stop / transition / pass band
Sb_l = 0                # Lower bound of the stopband, 0 / 8000 = 0
Sb_h = 0.25             # Upper bound of the stopband, 2000 / 8000 = 0.25
TB_l = 0.25             # Lower bound of the transition band, 2000 / 8000 = 0.25
TB_h = 0.3              # Upper bound of the transition band, 2400 / 8000 = 0.3
Pb_l = 0.275            # Lower bound of the passband, 2200 / 8000 = 0.275

fs = 8000               # Sampling frequency in Hz

# Create a frequency vector from 0 to 0.5 with a step of 0.0001 (5001 points)
F_all = np.arange(0, 0.5, 0.0001)
# Initialize the weight vector W_all and the desired filter response vector Hd_all
W_all = np.zeros_like(F_all)
# Desired filter response H_d[F_m] for the 5001 points (0 in stopband, 1 in passband)
Hd_all = (F_all >= Pb_l).astype(float)  # Check if the frequency is in the passband

for i in range(len(F_all)):
    if F_all[i] <= Sb_h:        # if t is in the stopband
        W_all[i] = W_s          # set the corresponding weight to W_s (stopband weight)
    elif F_all[i] >= TB_h and F_all[i] >= Pb_l:
        W_all[i] = W_p          # set the corresponding weight to W_p (passband weight)
    else:
        W_all[i] = 0            # the error in transition band is ignored, so set to 0

# Initialization for step 2
E_1 = float('inf')       # set the previous error of the first iteration to infinity
E_0 = 1000               # set a large value for error of the current iteration
delta = 0.0001           # Convergence threshold

# Matrix initialization
A_ext = np.zeros((k+2, k+2))  # Matrix A_ext
S = np.zeros((k+2, 1))        # Vector S

# Randomly choose the initial values for k+2 = 11 extreme points in [0, 0.5]
F_ext = np.array([0.1, 0.13, 0.15, 0.17, 0.2, 0.23, 0.35, 0.37, 0.4, 0.43, 0.45])
Hd_ext = (F_ext >= Pb_l).astype(float)  # Vector H with k+2 elements
P = F_ext                               # Initialize the local maximal/minimal points by F_ext
W_ext = np.zeros_like(F_ext)            # Initialize the weight vector for the extreme points

for i in range(len(F_ext)):
    if F_ext[i] <= Sb_h:
        W_ext[i] = W_s
    elif F_ext[i] >= TB_h and F_ext[i] >= Pb_l:
        W_ext[i] = W_p
    else:
        W_ext[i] = 0

# Start iteration
while E_1 - E_0 > delta or E_1 - E_0 < 0:
    E_1 = E_0  # set the previous error to the current error
    
    # STEP 2
    for row in range(k+2):
        for col in range(k+2):
            if col == 0:
                A_ext[row, col] = 1
            elif col == k+1:
                A_ext[row, col] = (-1)**row / W_ext[row]
            else:
                A_ext[row, col] = np.cos(2 * np.pi * col * F_ext[row])

    S = np.linalg.solve(A_ext, Hd_ext)  # S = A_ext^{-1} H

    # STEP 3
    # R(F) = \sum_{n=0}^k s[n] cos(2 \pi n F)
    RF = np.matmul(S[:k+1], np.cos(2 * np.pi * np.outer(np.arange(k+1), F_all)))
    
    # err(F) = [R(F) - H_d(F)]W(F)
    err = (RF - Hd_all) * W_all

    # STEP 4
    count = 0
    err_ext = []
    location_ext = []
    for i in range(len(F_all)):
        if i == 0:
            if err[i] > err[i+1] and err[i] > 0:
                F_ext[count] = F_all[i]
                err_ext.append(abs(err[i]))
                location_ext.append(i)
                count += 1
            elif err[i] < err[i+1] and err[i] < 0:
                F_ext[count] = F_all[i]
                err_ext.append(abs(err[i]))
                location_ext.append(i)
                count += 1
        elif i == len(F_all) - 1:
            if err[i] > err[i-1] and err[i] > 0:
                F_ext[count] = F_all[i]
                err_ext.append(abs(err[i]))
                location_ext.append(i)
                count += 1
            elif err[i] < err[i-1] and err[i] < 0:
                F_ext[count] = F_all[i]
                err_ext.append(abs(err[i]))
                location_ext.append(i)
                count += 1
        else:
            if err[i] > err[i-1] and err[i] > err[i+1] and err[i] > 0:
                F_ext[count] = F_all[i]
                err_ext.append(abs(err[i]))
                location_ext.append(i)
                count += 1
            elif err[i] < err[i-1] and err[i] < err[i+1] and err[i] < 0:
                F_ext[count] = F_all[i]
                err_ext.append(abs(err[i]))
                location_ext.append(i)
                count += 1

    if count >= (k+2) + 2:
        err_ext.pop(0)
        F_ext = np.delete(F_ext, 0)
        location_ext.pop(0)
        err_ext.pop(-1)
        F_ext = np.delete(F_ext, -1)
        location_ext.pop(-1)
        if len(err_ext) > k+2:
            idx = np.argsort(err_ext)[::-1]
            F_ext = F_ext[idx]
            location_ext = np.array(location_ext)[idx]
            err_ext = np.array(err_ext)[idx][:k+2]
            F_ext = F_ext[:k+2]
            location_ext = location_ext[:k+2]
        else:
            idx = np.argsort(err_ext)[::-1]
            F_ext = F_ext[idx]
            location_ext = np.array(location_ext)[idx]
    elif count == (k+2) + 1:
        if err_ext[0] > err_ext[k+2-1]:
            err_ext.pop(-1)
            F_ext = np.delete(F_ext, -1)
            location_ext.pop(-1)
        else:
            err_ext.pop(0)
            F_ext = np.delete(F_ext, 0)
            location_ext.pop(0)
        idx = np.argsort(err_ext)[::-1]
        F_ext = F_ext[idx]
        location_ext = np.array(location_ext)[idx]
    else:
        idx = np.argsort(err_ext)[::-1]
        F_ext = F_ext[idx]
        location_ext = np.array(location_ext)[idx]

    # STEP 5
    E_0 = max(err_ext)
    if E_1 - E_0 > delta or E_1 - E_0 < 0:
        for i in range(len(F_ext)):
            if F_ext[i] <= Sb_h:
                W_ext[i] = W_s
            elif F_ext[i] >= TB_h and F_ext[i] >= Pb_l:
                W_ext[i] = W_p
            else:
                W_ext[i] = 0
        Hd_ext = (F_ext >= Pb_l).astype(float)
    else:
        break

# STEP 6
h = np.zeros((N, 1))
h[k, 0] = S[0]  # h[k] = s[0]
for n in range(1, k+1):
    h[k+n, 0] = S[n] / 2  # h[k+n] = s[n]/2
    h[k-n, 0] = S[n] / 2  # h[k-n] = s[n]/2

# Plot the results
plt.figure(1)
# Plot Frequency Response
plt.subplot(211)
plt.plot(F_all, RF, 'r', label='R(F)')
plt.plot(F_ext, Hd_ext, 'b', label='Hd_ext')
plt.title('Frequency Response $R(F)$')
plt.xlabel('Normalized Frequency')
plt.ylabel('$R(F)$')
plt.xlim([0, 0.5])
plt.legend()

# Plot Impulse Response
plt.subplot(212)
n = np.arange(N)
plt.stem(n, h, use_line_collection=True)
plt.title('Impulse Response $h[n]$')
plt.xlabel('n')
plt.ylabel('$h[n]$')

plt.tight_layout()
plt.show()
