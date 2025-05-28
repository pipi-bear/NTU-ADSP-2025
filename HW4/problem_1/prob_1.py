import numpy as np
import cv2
from PIL import Image
import math
import os
import matplotlib.pyplot as plt

def C420(A):
    """
    Implement 4:2:0 image compression
    A: Input color image (H x W x 3 numpy array in RGB format)
    Returns: Tuple of (compressed image, reconstructed image)
    """
    
    # Normalize RGB values to [0, 1]
    A_norm = A.astype(float) / 255.0
    
    # RGB to YCbCr transform matrix
    # can be found in lecture note "ADSP_Write4.pdf", p.286
    transform = np.array([
        [0.299, 0.587, 0.114],
        [-0.169, -0.331, 0.500],
        [0.500, -0.419, -0.081]
    ])
    
    # Convert to YCbCr
    ycbcr = np.zeros_like(A_norm)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            ycbcr[i, j] = np.dot(transform, A_norm[i, j])
    
    # Add offset to Cb and Cr
    ycbcr[:,:,1:] += 0.5
    
    # Downsample Cb and Cr (4:2:0)
    # Take average of 2x2 blocks
    H, W = A.shape[:2]
    H_down = H // 2
    W_down = W // 2
    
    Cb_down = np.zeros((H_down, W_down))
    Cr_down = np.zeros((H_down, W_down))
    
    for i in range(H_down):
        for j in range(W_down):
            Cb_down[i,j] = np.mean(ycbcr[2*i:2*i+2, 2*j:2*j+2, 1])
            Cr_down[i,j] = np.mean(ycbcr[2*i:2*i+2, 2*j:2*j+2, 2])
    
    # Create compressed image (before interpolation)
    ycbcr_compressed = ycbcr.copy()
    for i in range(H_down):
        for j in range(W_down):
            ycbcr_compressed[2*i:2*i+2, 2*j:2*j+2, 1] = Cb_down[i,j]
            ycbcr_compressed[2*i:2*i+2, 2*j:2*j+2, 2] = Cr_down[i,j]
    
    # Convert compressed image back to RGB
    compressed = np.zeros_like(A_norm)
    for i in range(H):
        for j in range(W):
            compressed[i, j] = np.dot(np.linalg.inv(transform), ycbcr_compressed[i, j] - [0, 0.5, 0.5])
    
    # Reconstruct using interpolation
    Cb_up = cv2.resize(Cb_down, (W, H), interpolation=cv2.INTER_LINEAR)
    Cr_up = cv2.resize(Cr_down, (W, H), interpolation=cv2.INTER_LINEAR)
    
    # Combine channels
    ycbcr_reconstructed = np.dstack((ycbcr[:,:,0], Cb_up, Cr_up))
    
    # Subtract offset from Cb and Cr
    ycbcr_reconstructed[:,:,1:] -= 0.5
    
    # YCbCr to RGB conversion matrix
    inverse_transform = np.linalg.inv(transform)
    
    # Convert back to RGB
    reconstructed = np.zeros_like(A_norm)
    for i in range(H):
        for j in range(W):
            reconstructed[i, j] = np.dot(inverse_transform, ycbcr_reconstructed[i, j])
    
    # Clip values to [0, 1] and convert back to [0, 255]
    compressed = np.clip(compressed, 0, 1) * 255
    reconstructed = np.clip(reconstructed, 0, 1) * 255
    return compressed.astype(np.uint8), reconstructed.astype(np.uint8)

def calculate_psnr(A, B):
    """
    Calculate PSNR value between original image A and reconstructed image B
    The formula can be found in lecture note "ADSP_Write4.pdf", p.301
    """
    if len(A.shape) != 3 or len(B.shape) != 3:
        raise ValueError("Input images must be color images with 3 channels")
    
    M, N = A.shape[:2]  # image dimensions
    X_max = 255.0       # maximum possible pixel value
    
    # Calculate MSE across all color channels
    mse = np.sum((A.astype(float) - B.astype(float)) ** 2) / (3 * M * N)
    
    if mse == 0:
        return float('inf')
    
    # Calculate PSNR using the formula
    psnr = 10 * math.log10((X_max ** 2) / mse)
    return psnr

def create_comparison_image(compressed, reconstructed, psnr_value):
    """
    Create a comparison image with compressed and reconstructed images side by side
    """
    # Create figure and subplots
    plt.figure(figsize=(12, 6))
    
    # Plot compressed image
    plt.subplot(1, 2, 1)
    plt.imshow(compressed)
    plt.title('Compressed Image (4:2:0)')
    plt.axis('off')
    
    # Plot reconstructed image
    plt.subplot(1, 2, 2)
    plt.imshow(reconstructed)
    plt.title('Reconstructed Image')
    plt.axis('off')
    
    # Add PSNR value as text
    plt.suptitle(f'PSNR: {psnr_value:.2f}', fontsize=14, y=0.95)
    
    plt.tight_layout()
    plt.show()

def main():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define input and output image paths relative to script location
    # note: Modify the input image path here
    input_image = os.path.join(script_dir, 'jokebear3.jpg')
    
    # Create output filename by adding '_reconstructed' before the extension
    input_basename = os.path.splitext(os.path.basename(input_image))[0]  # get filename without extension
    input_ext = os.path.splitext(input_image)[1]  
    output_filename = f"{input_basename}_reconstructed{input_ext}"
    output_image = os.path.join(script_dir, output_filename)
    
    # Read the input image
    A = cv2.imread(input_image)
    if A is None:
        print(f"Error: Could not read input image at {input_image}")
        return
    
    # Convert BGR to RGB (cv2 reads in BGR format)
    A = cv2.cvtColor(A, cv2.COLOR_BGR2RGB)
    
    # Apply 4:2:0 compression and reconstruction
    compressed, reconstructed = C420(A)
    
    # Calculate PSNR between compressed and reconstructed
    psnr_value = calculate_psnr(compressed, reconstructed)
    print(f"PSNR value between the compressed and reconstructed image: {psnr_value:.2f}")
    
    # Save the reconstructed image
    reconstructed_rgb = Image.fromarray(reconstructed)
    reconstructed_rgb.save(output_image)
    print(f"Reconstructed image saved as: {output_image}")
    
    # Create comparison image
    create_comparison_image(compressed, reconstructed, psnr_value)

if __name__ == "__main__":
    main()
