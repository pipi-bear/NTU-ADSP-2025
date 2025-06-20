# Contents of the Directory 

The directory HW5 contains:
- HW spec: `ADSP_HW5.pdf`
- solution for ADSP_HW5: `ADSP_HW5_sol.pdf`, `ADSP_HW5_sol.tex`
> You can choose if you need the pdf veresion or the latex code (the equations can be copied)
> $\rightarrow$ The images that I attached in the HW solution are under: `HW5/HW5_img`

## Code for problem 1, 4, 7

In this HW, I wrote some code to solve problem 1, 4, 7. These code can be found at:

- code for prblem 1: `HW5/problem_1/problem_1.py`
- code for prblem 4: `HW5/problem_4/4.py`
- code for prblem 7: `HW5/problem_7.ipynb`

:warning: However, be aware that I got points deducted in some of the subproblems in 4 and 7, check the last section "Grade and Feedback" in this README for more details.


# Grade and feedback

## Grade

9.48 / 12

## Feedback

Solution feedback:

---

3.Only one multiplication operation is required for each output. -4
4.
(b) Sectioned convolution, using 360 or 240-point DFT, the number of real multiplications is 20800. -3
(c) Sectioned convolution, using 48-point DFT, the number of real multiplications is 12792. -3
(d) Sectioned convolution, using 4-point DFT, the number of real multiplications is 6000. -3
6.(b) 30 additions. -3
7.(a) -2
7.(c) -3, It is improper to use the Haar transform for CDMA, since many rows of the Haar transform has only 2 or 4 nonzero entries, which makes the Haar transform not robust to error. 

bonus+1

---

### Error in problem 4

From the feedback, I found that the problem is that I did not check the $P$ values under the lower bound I set, which is:

$$P \geq L_0 + M - 1$$

Maybe there is something wrong regarding to this part, if you want to write your homework based on my code, maybe you could check what the correct lower bound should be.
> I did not have enough time to finish watching all lecture videos for the last few weeks of the semester, and too lazy to rewatch them after the semester ends :joy:, so I'm not sure about the correct definition.