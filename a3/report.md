## Summary



I've finished all of problems. But I spent too much time tuning the hyper-parameters on problem 4 and the result of problem 4 sometimes is weird due to randomness. As I wrote on moodle (https://moodle.hku.hk/mod/forum/discuss.php?d=827845), I am not pretty sure that my code could converge the test dataset.

Problem1: 3h

Problem2: 2h

Problem3: 0.5h

Problem4: 2h

Tuning Problem4: 3h

report: 2h

total: 12.5h

## Problem 1

1. Find the start point position.
2. Do loop until go to exit position.
   1. Determine the intended direction based on the policy and determine the actual direction based on the probability distribution.
   2. Check the feasibility of actual direction. Update the info.
3. return result.

## Problem 2

1. do specified times of iterations 
   1. loop every points	
      1. Determine the intended direction based on the policy and determine the actual direction based on the probability distribution.
      2. Check the feasibility of actual direction.
      3. Compute the current value for current point based on the previous iteration value matrix.
2. After finishing every iterations, return res.

## Problem 3

1. do specified iterations 
   1. loop every points
      1. loop every direction (North, East, South, West)
         1. check the feasibility of all directions based on the probability distribution.
         2. Compute the value based on the previous iteration value matrix
      2. choose the policy corresponding to the max value.
2. After finishing every iterations, return res.

## Problem 4

1. do specified iterations

   1. determine the start place

   2. loop until the sample go to exit place

      1. determine the direction based on epsilon_greedy_with_decay function

         ```python
             def epsilon_greedy_with_decay(self, row, col):
                 if random.random() < EPSILON * (1 - self.current_iteration ** 1 / self.max_iterations ** 1):
                     return random.choices(population="NWES")[0]
                 else:
                     return self.find_max_direction(row, col)
         ```

         At the beginning of iterations, every sample have much higher probabilities to go randomly. After processing many samples, the sample try to find the direction regarding the max q value.

      2. Compute q value for current sample and current position.

      3. Based on TD-Learning equation, update Q(s,a)

2. After finishing the whole loop process, generate the policy based on the direction regarding max q-value.

**if  you want to check the q value convergence **, uncomment out code from line 121

### 1.prob convergence situation

| N 0.93 ||E 0.939 || S 0.92 ||W 0.928 ||N 0.943 ||E 0.953 ||S 0.943 ||W 0.932 ||N 0.957 ||E 0.966 || S 0.88 ||W 0.936 ||  0.99  |
|N 0.927 ||E 0.916 ||S 0.905 ||W 0.916 || #####  || N 0.75 ||E -0.672||S 0.663 ||W 0.874 || -1.01  |
|N 0.913 ||E 0.894 ||S 0.901 ||W 0.903 ||N 0.889 ||E 0.877 ||S 0.889 ||W 0.899 || N 0.84 ||E 0.731 ||S 0.856 ||W 0.886 ||N -0.682||E 0.521 ||S 0.719 ||W 0.652 |

### 2.prob convergence situation

|N 0.797 ||E 0.823 ||S 0.766 ||W 0.788 ||N 0.834 ||E 0.863 ||S 0.834 || W 0.8  ||N 0.875 || E 0.9  ||S 0.678 ||W 0.818 ||  0.97  |
|N 0.785 ||E 0.753 ||S 0.721 ||W 0.755 || #####  ||N 0.655 ||E -0.702||S 0.455 ||W 0.649 || -1.03  |
|N 0.743 ||E 0.687 ||S 0.709 ||W 0.717 ||N 0.676 ||E 0.646 ||S 0.676 ||W 0.704 ||N 0.617 ||E 0.448 ||S 0.616 ||W 0.668 ||N -0.756||E 0.268 ||S 0.427 ||W 0.431 |

### 3.prob convergence situation

|N -1.375||E -1.041||S -1.783||W -1.483||N -0.872||E -0.479||S -0.876||W -1.319||N -0.362||E 0.032 ||S -0.836||W -0.83 ||  0.6   |
|N -1.545||E -1.927||S -2.302||W -1.927|| #####  ||N -0.599||E -1.627||S -1.559||W -0.983||  -1.4  |
| N -2.0 ||E -2.113||S -2.363||W -2.343||N -2.077||E -1.695||S -2.081||W -2.341||N -1.193||E -1.908||S -1.704||W -1.937||N -1.804||E -2.035||S -2.021||W -1.671|

### 4.prob convergence situation

|N -10.767||E -9.157||S -12.76||W -11.284||N -8.265||E -6.263||S -8.331||W -10.525||N -5.719||E -3.728||S -7.195||W -7.939||  -1.0  |
|N -11.582||E -13.443||S -14.548||W -13.408|| #####  ||N -5.844||E -5.509||S -9.264||W -7.614||  -3.0  |
|N -13.6 ||E -12.77||S -14.586||W -14.714||N -12.435||E -10.475||S -12.435||W -14.347||N -8.096||E -7.978||S -10.007||W -11.781||N -5.795||E -7.557||S -8.011||W -9.275|





