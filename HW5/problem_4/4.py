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
    {'N': 840, 'muls': 4580}, {'N': 1008, 'muls': 5356}, {'N': 1024, 'muls': 7436},
    {'N': 1152, 'muls': 7088}, {'N': 1260, 'muls': 7640}, {'N': 1344, 'muls': 8252},
    {'N': 1440, 'muls': 8680}, {'N': 1680, 'muls': 10420}, {'N': 2016, 'muls': 12728},
    {'N': 2048, 'muls': 16836}, {'N': 2304, 'muls': 15868}, {'N': 2520, 'muls': 16540},
    {'N': 2688, 'muls': 19108}, {'N': 2880, 'muls': 20060}, {'N': 3369, 'muls': 24200},
    {'N': 3920, 'muls': 29900}, {'N': 4032, 'muls': 29488}, {'N': 4096, 'muls': 37516},
    {'N': 4368, 'muls': 35828}, {'N': 4608, 'muls': 36812}, {'N': 5040, 'muls': 36860}
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

def calculate_real_multiplications(L, P, N, M, S, Pvalues_N):
    """
    Calculate the number of real multiplications using different formulas based on approach:
    
    Non-sectioned: 2 × MUL_P + 3P, where P ≥ N + M - 1
    Sectioned: S × (2 × MUL_P + 3P), where P ≥ L + M - 1
    
    MUL_P is taken from the lookup table if available, otherwise approximated as (3P/2)log₂P
    """
    # Get MUL_P from the lookup table if available
    table_entry = next((entry for entry in Pvalues_N if entry['N'] == P), None)
    if table_entry:
        MUL_P = table_entry['muls']
    else:
        # If not in table, use the approximation formula
        MUL_P = (3 * P / 2) * np.log2(P)
    
    # Calculate both approaches
    # Non-sectioned approach
    if P >= N + M - 1:
        nonsectioned_muls = 2 * MUL_P + 3 * P
    else:
        nonsectioned_muls = float('inf')  # Invalid P for non-sectioned
        
    # Sectioned approach
    if P >= L + M - 1:
        sectioned_muls = S * (2 * MUL_P + 3 * P)
    else:
        sectioned_muls = float('inf')  # Invalid P for sectioned
        
    return nonsectioned_muls, sectioned_muls

def calculate_optimal_approaches(N, M):
    """
    Calculate optimal results for all three approaches: direct, non-sectioned, and sectioned
    """
    # Direct computation
    direct_muls = calculate_direct_multiplications(N, M)
    
    # Find L0 for sectioned convolution
    L0 = find_L0(N, M)
    
    # Non-sectioned convolution: find optimal P ≥ N + M - 1
    min_P_nonsectioned = N + M - 1
    P_values_nonsectioned = [entry['N'] for entry in Pvalues_N if entry['N'] >= min_P_nonsectioned]
    
    min_muls_nonsectioned = float('inf')
    optimal_nonsectioned = None
    
    for P in P_values_nonsectioned:
        table_entry = next((entry for entry in Pvalues_N if entry['N'] == P), None)
        if table_entry:
            MUL_P = table_entry['muls']
            muls = 2 * MUL_P + 3 * P
            if muls < min_muls_nonsectioned:
                min_muls_nonsectioned = muls
                optimal_nonsectioned = {
                    'method': 'Non-sectioned convolution',
                    'P': P,
                    'MUL_P': MUL_P,
                    'muls': muls
                }
    
    # Sectioned convolution: find optimal P ≥ L + M - 1
    min_P_sectioned = L0 + M - 1
    P_values_sectioned = [entry['N'] for entry in Pvalues_N if entry['N'] >= min_P_sectioned]
    
    min_muls_sectioned = float('inf')
    optimal_sectioned = None
    
    for P in P_values_sectioned:
        table_entry = next((entry for entry in Pvalues_N if entry['N'] == P), None)
        if table_entry:
            MUL_P = table_entry['muls']
            L = min(L0, P - M + 1)
            S = math.ceil(N / L)
            muls = S * (2 * MUL_P + 3 * P)
            if muls < min_muls_sectioned:
                min_muls_sectioned = muls
                optimal_sectioned = {
                    'method': 'Sectioned convolution',
                    'P': P,
                    'MUL_P': MUL_P,
                    'muls': muls,
                    'L': L,
                    'S': S
                }
    
    return {
        'direct': {'method': 'Direct computation', 'muls': direct_muls},
        'nonsectioned': optimal_nonsectioned,
        'sectioned': optimal_sectioned,
        'L0': L0,
        'min_P_nonsectioned': min_P_nonsectioned,
        'min_P_sectioned': min_P_sectioned
    }

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

def calculate_direct_multiplications(N, M):
    """
    Calculate the number of real multiplications for direct computation:
    3N × M, where N = length(x[n]), M = length(h[n])
    """
    return 3 * N * M

def main():
    # Given parameters
    N = 1500  # length(x[n])
    M = 2  # length(h[n])
    
    print(f"Given: N = {N}, M = {M}")
    
    # Calculate optimal approaches
    results = calculate_optimal_approaches(N, M)
    
    print(f"\nStep 1:")
    print(f"L0 = {results['L0']}")
    
    print(f"\nStep 2:")
    print(f"Requirements:")
    print(f"- Non-sectioned convolution: P >= N + M - 1 = {results['min_P_nonsectioned']}")
    print(f"- Sectioned convolution: P >= L0 + M - 1 = {results['min_P_sectioned']}")
    
    # Find P values for testing and show detailed calculations
    P0 = results['L0'] + M - 1
    P_values = find_nearest_P_values(P0, Pvalues_N)
    print(f"\nTesting P values from table: {P_values}")
    
    # Step 3a: Show detailed calculations for non-sectioned convolution
    print(f"\nStep 3a: Non-sectioned convolution calculations")
    # Get P values for non-sectioned (P >= N + M - 1)
    P_values_nonsectioned = [entry['N'] for entry in Pvalues_N if entry['N'] >= results['min_P_nonsectioned']]
    
    if P_values_nonsectioned:
        print("P\tMUL_P\tFormula (2×MUL_P + 3×P)\tReal Multiplications")
        print("-" * 70)
        
        for P in P_values_nonsectioned[:10]:  # Show first 10 valid P values
            table_entry = next((entry for entry in Pvalues_N if entry['N'] == P), None)
            if table_entry:
                MUL_P = table_entry['muls']
                muls = 2 * MUL_P + 3 * P
                print(f"{P}\t{MUL_P}\t2×{MUL_P} + 3×{P}\t\t{muls}")
    else:
        print("No valid P values found in table for non-sectioned convolution requirement.")
    
    # Step 3b: Show detailed calculations for sectioned convolution
    print(f"\nStep 3b: Sectioned convolution calculations")
    # Get P values for sectioned (P >= L0 + M - 1)
    P_values_sectioned = [entry['N'] for entry in Pvalues_N if entry['N'] >= results['min_P_sectioned']]
    
    if P_values_sectioned:
        print("P\tL\tS\tMUL_P\tFormula (S×(2×MUL_P + 3×P))\tReal Multiplications")
        print("-" * 80)
        
        for P in P_values_sectioned[:10]:  # Show first 10 valid P values
            table_entry = next((entry for entry in Pvalues_N if entry['N'] == P), None)
            if table_entry:
                # L must be less than or equal to P-M+1
                L = min(results['L0'], P - M + 1)
                S = math.ceil(N / L)
                MUL_P = table_entry['muls']
                sectioned_muls = S * (2 * MUL_P + 3 * P)
                formula_str = f"{S}×(2×{MUL_P} + 3×{P})"
                print(f"{P}\t{L}\t{S}\t{MUL_P}\t{formula_str}\t\t\t{sectioned_muls:.0f}")
    else:
        print("No valid P values found in table for sectioned convolution requirement.")
    
    # Print results for all three approaches
    print(f"\nDirect computation approach:")
    print(f"Number of real multiplications = {results['direct']['muls']:.0f}")
    
    print(f"\nOptimal values for non-sectioned approach:")
    if results['nonsectioned']:
        print(f"P = {results['nonsectioned']['P']}")
        print(f"Table value for P={results['nonsectioned']['P']}: {results['nonsectioned']['MUL_P']}")
        print(f"Formula: 2 × {results['nonsectioned']['MUL_P']} + 3 × {results['nonsectioned']['P']} = {results['nonsectioned']['muls']}")
        print(f"Number of real multiplications = {results['nonsectioned']['muls']:.0f}")
    else:
        print("No valid P values found in table for non-sectioned convolution")
        print("P = None")
        print("L = None")
        print("S = None")
        print("Number of real multiplications = inf")
    
    print(f"\nOptimal values for sectioned approach:")
    if results['sectioned']:
        print(f"P = {results['sectioned']['P']}")
        print(f"L = {results['sectioned']['L']}")
        print(f"S = {results['sectioned']['S']}")
        print(f"Table value for P={results['sectioned']['P']}: {results['sectioned']['MUL_P']}")
        print(f"Formula: {results['sectioned']['S']} × (2 × {results['sectioned']['MUL_P']} + 3 × {results['sectioned']['P']}) = {results['sectioned']['muls']}")
        print(f"Number of real multiplications = {results['sectioned']['muls']:.0f}")
    else:
        print("No valid P values found in table for sectioned convolution")
        print("P = None")
        print("L = None") 
        print("S = None")
        print("Number of real multiplications = inf")
    
    # Compare all three approaches
    print(f"\nComparison of approaches:")
    approaches = []
    
    # Add direct approach
    approaches.append(("Direct", results['direct']['muls']))
    
    # Add non-sectioned approach
    if results['nonsectioned']:
        approaches.append(("Non-sectioned", results['nonsectioned']['muls']))
    else:
        approaches.append(("Non-sectioned", float('inf')))
    
    # Add sectioned approach
    if results['sectioned']:
        approaches.append(("Sectioned", results['sectioned']['muls']))
    else:
        approaches.append(("Sectioned", float('inf')))
    
    best_approach = min(approaches, key=lambda x: x[1])
    print(f"{best_approach[0]} approach is best with {best_approach[1]:.0f} multiplications")
    print("\nMultiplications required for each approach:")
    for approach, muls in sorted(approaches, key=lambda x: x[1]):
        if muls == float('inf'):
            print(f"{approach}: inf")
        else:
            print(f"{approach}: {muls:.0f}")

if __name__ == "__main__":
    main() 