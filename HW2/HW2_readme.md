# Contents of the Directory 

The directory HW2 contains:
- HW spec: `ADSP_HW2.pdf`
- HW spec (with little notes): `ADSP_HW2_write.pdf`
- solution for ADSP_HW2: `ADSP_HW2_sol.pdf`, `ADSP_HW2_sol.tex`
> You can choose if you need the pdf veresion or the latex code (the equations can be copied)
- problem 1 code: `HW2_prob1.py`
- problem 1 code result images: `prob1_iamges`

## Problem 1

For problem 1, we are asked to hand in the code and put the resulting images in the solution pdf (`ADSP_HW2_sol.pdf`). 

### images 

You can find the images that I attached in `ADSP_HW2_sol.pdf` by checking the subdirectory `prob1_images`.  

Note that there's two images:
- `required_plot.png`: the plot used in HW
- `plot_with_additional_info.png`: additional info that I printed to check if anything is wrong 

### Code

As mentioned above, some plotting parts are not required by the HW spec, if you do not need the additional plot, make sure you did not mistakenly copied from line 47 to 71:

```python
# Plotting additional information to check the result (r_1[n], r[n], h[n])

"""
<some plotting content>
"""

plt.tight_layout()
```

# Note

Some of the solutions in `ADSP_HW2_sol` mentioned that I've used the contents from ppt, like you may see "from ppt p.***".

The ppt resources can be found in the subdirectory `Lecture_notes`, you can download them if needed :)

# Score

I got $10.44$ out of $12$ in this assignment. The scores for each problem and the mistakes given by the TA are shown below:

(1) 16
圖形有誤，講義p. 115有關transition band的部分，係將原本Hd的值乘上大於0小於1的值，例如講義所寫的乘上0.7與0.2，而因為transition band的位置是在訊號邊緣附近，因此有可能會出現一邊要用F，另一邊要用(F-1)，因此在line 18-26的迴圈中，應先將值算出後再做transition band
(2) 20
(3) 5
(4) 10
(5) 10
(6) 16
(a) (z-2)沒有約分
(b)
H(z) = (2z³ - 2z² - 3z - 2) / (z² - 0.7z + 1)
= 2[z - (-1+j)/2][z - (-1-j)/2](z - 2) / (z - 0.2)(z - 0.5)
依照講義 p. 186 - 188 的作法
Ĥ(z) = log (H(z)) 
= log 2 + log [z - (-1+j)/2] + log [z - (-1-j)/2] + log (z - 2) - log(z - 0.2) - log(z - 0.5)
= log 2 + log [1 - (-1+j)/2 z⁻¹] + log [1 - (-1-j)/2 z⁻¹] + log [-2(1 - ½ z)] - log(1 - 0.2 z⁻¹) - log(1 - 0.5 z⁻¹) 
= log (-4) + [-(-1-j)/2]ⁿ/n]z⁻ⁿ + [-[(-1+j)/2]ⁿ/n]z⁻ⁿ + (½)⁻ⁿ/n zⁿ  - (-0.2ⁿ/n)z⁻ⁿ - (-0.5ⁿ/n)z⁻ⁿ
log(-4), n = 0
(7) 10
(Bonus) +1