import numpy as np
import math
from scipy.optimize import minimize_scalar

# N is the number of points in the DFT, and muls is the number of real multiplications
# This is part of the given table, which can be found in lecture note "ADSP_Write5.pdf", p.377-379
Pvalues_N = [
    {'N': 63, 'muls': 256}, {'N': 64, 'muls': 204}, {'N': 66, 'muls': 284},
    {'N': 70, 'muls': 300}, {'N': 72, 'muls': 164}, {'N': 80, 'muls': 260},
    {'N': 81, 'muls': 480}, {'N': 84, 'muls': 248}, {'N': 88, 'muls': 364},
    {'N': 90, 'muls': 340}, {'N': 96, 'muls': 280}, {'N': 104, 'muls': 468},
    {'N': 108, 'muls': 456}, {'N': 112, 'muls': 396}, {'N': 120, 'muls': 380},
    {'N': 128, 'muls': 560}, {'N': 144, 'muls': 436}, {'N': 160, 'muls': 680},
    {'N': 168, 'muls': 580}, {'N': 180, 'muls': 680}, {'N': 192, 'muls': 752},
    {'N': 204, 'muls': 976}, {'N': 216, 'muls': 1020}, {'N': 224, 'muls': 1016},
    {'N': 240, 'muls': 940}, {'N': 252, 'muls': 1024}, {'N': 256, 'muls': 1308},
    {'N': 288, 'muls': 1160}, {'N': 312, 'muls': 1608}, {'N': 336, 'muls': 1412},
    {'N': 360, 'muls': 1540}, {'N': 420, 'muls': 2080}, {'N': 480, 'muls': 2360},
    {'N': 504, 'muls': 2300}, {'N': 512, 'muls': 3180}, {'N': 560, 'muls': 3100},
    {'N': 672, 'muls': 3496}, {'N': 720, 'muls': 3620}, {'N': 784, 'muls': 4412},
    {'N': 840, 'muls': 4580}
]

def calculate_step1_func(L, N, M):
    """
    Calculate the function in step one: (N / L) 3 (L + M - 1)[log_2 ( L + M - 1) + 1]
    """
    if L <= 0:
        return float('inf')
    return (N / L) * 3 * (L + M - 1) * (np.log2(L + M - 1) + 1)

def find_L0(N, M):
    """
    Step 1: Find L0 that minimizes the function in step one
    note that we return the rounded value in order to get the integer value of L0
    """
    result = minimize_scalar(
        lambda L: calculate_step1_func(L, N, M),
        bounds=(1, N),
        method='bounded'
    )
    
    L0 = int(round(result.x))
    return L0

def calculate_real_multiplications(L, P, N):
    """
    Calculate the number of real multiplications using the formula:
    2S x [(3P / 2) log_2(P)] + 3SP, where S approx N / L
    The formula can be found in lecture note "ADSP_12.pdf", p.444
    """
    S = math.ceil(N / L)
    return 2 * S * ((3 * P / 2) * np.log2(P)) + 3 * S * P

def find_nearest_P_values(P0, Pvalues_N, num_neighbors = 4):
    """
    Find the nearest P values from the table around P0
    """
    # Get all N values from the table
    N_values = [entry['N'] for entry in Pvalues_N]
    
    # Find the nearest indices
    N_array = np.array(N_values)
    idx = np.searchsorted(N_array, P0)
    
    # Get range of indices around the insertion point
    start_idx = max(0, idx - num_neighbors)
    end_idx = min(len(N_values), idx + num_neighbors + 1)
    
    return N_values[start_idx:end_idx]

def main():
    # Given parameters
    N = 1500  # length(x[n])
    M = 250  # length(h[n])
    
    # Step 1: Find L0
    L0 = find_L0(N, M)
    print(f"\nStep 1:")
    print(f"L0 = {L0}")
    
    # Step 2: Estimate P0 and find nearest values from the table
    P0 = L0 + M - 1
    P_values = find_nearest_P_values(P0, Pvalues_N)
    print(f"\nStep 2:")
    print(f"P0 = L0 + M - 1 = {P0}")
    print(f"Testing P values from table: {P_values}")
    
    # Step 3: Calculate L, S, and number of real multiplications for each P
    print(f"\nStep 3:")
    print("P\tL\tS\tReal Multiplications\tTable Multiplications")
    print("-" * 70)
    
    min_muls = float('inf')
    optimal_P = None
    optimal_L = None
    optimal_S = None
    
    results = []
    for P in P_values:
        # L must be less than or equal to P-M+1
        L = min(L0, P - M + 1)
        S = math.ceil(N / L)
        muls = calculate_real_multiplications(L, P, N)
        
        # Find the corresponding table value
        table_muls = next((entry['muls'] for entry in Pvalues_N if entry['N'] == P), None)
        
        results.append((P, L, S, muls, table_muls))
        print(f"{P}\t{L}\t{S}\t{muls:.0f}\t\t{table_muls if table_muls else 'N/A'}")
        
        if muls < min_muls:
            min_muls = muls
            optimal_P = P
            optimal_L = L
            optimal_S = S
    
    print(f"\nOptimal values:")
    print(f"P = {optimal_P}")
    print(f"L = {optimal_L}")
    print(f"S = {optimal_S}")
    print(f"Calculated number of real multiplications = {min_muls:.0f}")
    
    # Find the corresponding table value for optimal P
    optimal_table_muls = next((entry['muls'] for entry in Pvalues_N if entry['N'] == optimal_P), None)
    if optimal_table_muls:
        print(f"Table value for N={optimal_P}: {optimal_table_muls}")

if __name__ == "__main__":
    main() 