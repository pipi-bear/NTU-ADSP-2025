import numpy as np
from scipy.stats import entropy

# Parameters
lambda_val = 0.015
n_max = 5000

# aim: Calculate entropy
# Generate n values from 0 to 5000
n = np.arange(n_max + 1)

# Calculate probabilities: P(x=n) = (1-e^(-lambda))e^(-lambda * n)
p = (1 - np.exp(-lambda_val)) * np.exp(-lambda_val * n)

# Calculate entropy (in nats by default)
H = entropy(p)
# Calculate entropy in bits (by dividing by ln(2))
H_bits = H / np.log(2)
print(f"Entropy (nats): {H:.6f}")
print(f"Entropy (bits): {H_bits:.6f}\n")

# aim: Calculate the bounds to get the range of total coding length
N = 50000

# Lower bound: ceil(50000 × 7.501602 / ln2)
lower_bound = np.ceil(N * H_bits)

# Upper bound: floor(50000 × 7.501602 / ln2 + 50000)
upper_bound = np.floor(N * H_bits + N)

print(f"\nBounds calculation:\n")
print(f"Lower bound: {lower_bound:.0f}")
print(f"Upper bound: {upper_bound:.0f}")
