import numpy as np
from scipy.stats import entropy

# aim: Calculate entropy
lambda_val = 0.015
n_max = 5000

n = np.arange(n_max + 1)

# Calculate probabilities: P(x=n) = (1-e^(-λ))e^(-λn)
p = (1 - np.exp(-lambda_val)) * np.exp(-lambda_val * n)

# Calculate entropy (in nats by default)
H = entropy(p)
# Calculate entropy in bits (by dividing by ln(2))
H_bits = H / np.log(2)

print(f"Entropy (nats): {H:.6f}")
print(f"Entropy (bits): {H_bits:.6f}\n")

# aim: Calculate bounds to get the range of total coding length
N = 50000  # length(X)
k = 2      # binary coding

# Calculate the range of total coding length b
# For binary coding (k=2):
# ceil(N·entropy / ln k) \leq b \leq floor(N entropy / ln k + log_2 2 + 1)

# Lower bound: ceil(N entropy / ln k)
lower_bound = np.ceil(N * H_bits)

# Upper bound: floor(N·entropy / ln k + log_2 2 + 1)
upper_bound = np.floor(N * H_bits + np.log2(k) + 1)

print(f"Arithmetic Coding Length Bounds:")
print(f"Lower bound: {lower_bound:.0f}")
print(f"Upper bound: {upper_bound:.0f}")

