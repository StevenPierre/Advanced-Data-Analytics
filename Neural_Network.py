Problem 15: The Forward Pass of a Neural Network
Version 1.2

Neural networks are a set of algorithms for pattern recognition. They are loosely inspired by the human brain, and have proven especially useful in data clustering and classification tasks.

In this problem, you will use your knowledge of Python and Numpy to speed-up a common computational kernel that arises in neural networks.

Example: a "fully connected layer" for images. Suppose the data we are analyzing consists of  N
  two-dimensional images of size  H×W
  pixels each. In a neural network, a typical substep is the evaluation of a "fully connected (FC) layer," which takes the images as input and produces a vector of outputs, with one vector per image.

Mathematically, here is a simplified example of what a typical FC layer calculation might look like. Let  x[k,i,j]
  denote the value (e.g., intensity) of the pixel at location  (i,j)
  of the  k
 -th input image. Since there are  N
  images, take the values of  k
  to be in the range of 0 to  N−1
 , respectively. And since each image is  H×W
 , take  0≤i≤H−1
  and  0≤j≤W−1
 . Next, let  out[k,l]
  denote an output value in the  l
 -th element of a vector associated with image  k
 , where  0≤l≤M−1
 , for some given value of  M
 . Lastly, suppose the specific formula for transforming the input images into this collection of output vectors is given by the formula,

out[k,l]=b[l]+∑i=0H−1∑j=0W−1(x[k,i,j]×w[l,i,j])
 
where  w[l,i,j]
  are "weights" and  b[l]
  are "biases." The process of "training" the neural network from sample data determines these weight and bias parameters, but for this problem, just assume that they are given.

If it's helpful, here is a picture of what this formula is doing for each  (k,l)
  pair: <img src = "fully_connected.png" width = "600">

The baseline implementation. In the code cells below, we define a Python function, FC_naive(x, w, b), that implements the FC layer calculation from above using a straightforward, albeit somewhat naive, method. Your goal is to make this baseline run faster.

To start, first run the next three code cells to estimate the time of the baseline implementation.

import numpy as np
import time

def rel_error(x, y):
    return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))
def FC_naive(x, w, b):
    """
    Inputs:
    - x: A numpy array of images of shape (N, H, W)
    - w: A numpy array of weights of shape (M, H, W)
    - b: A numpy vector of biases of size M

    Returns: 
    - out: a numpy array of shape (N, M)
    """
    N, H, W = x.shape
    M, _, _ = w.shape
    out = np.zeros((N,M))
    for ni in range(N):
        for mi in range(M):
                out[ni,mi] = b[mi]
                for d1 in range(H):
                    for d2 in range(W):
                        out[ni,mi] += x[ni, d1, d2] * w[mi, d1, d2] 
    return out
num_inputs = 50
input_shape = (128, 256)
output_dim = 10

x = np.random.rand(num_inputs, *input_shape)
w = np.random.rand(output_dim, *input_shape)
b = np.random.rand(output_dim)
start_time = time.time ()
out = FC_naive(x, w, b)
elapsed_time = time.time () - start_time
print ("==> Took %g seconds." % elapsed_time)
==> Took 13.1844 seconds.
Exercise 1 (5 points). Let's start by seeing if we can make FC_naive() function faster by rewriting the two innermost loops, i.e., the d1 and d2 loops:

for d1 in range(H):
    for d2 in range(W):
        out[ni, mi] += x[ni, d1, d2] * w[mi, d1, d2]
For this exercise, complete the function two_inner_loops(x_i, w_l, b_j), below, so that it implements the same computation as these two d1 and d2 loops, but is much faster. It should return out[ni, mi]. The input x_i is the i-th image, w_l is the l-th weight matrix, and b_l is the l-th component of the bias vector.

The test code will check your results and benchmark a complete FC layer using the function FC_two_loops(), defined below. You'll see that it calls your two_inner_loops() routine to implement the two innermost loops.

To get credit on this exercise, the resulting execution time of FC_two_loops() must be at least 100 times faster than FC_naive() on the problem sizes being tested below when running on the Vocareum platform. There is no partial credit for smaller speedups. Having said that, a little bit of basic Numpy should go a long way.

def two_inner_loops(x_i, w_l, b_l):
    """
    Inputs:
    - x_i: A numpy array of images of shape (H, W)
    - w_l: A numpy array of weights of shape (H, W)
    - b_l: A float (single number)

    Returns: 
    - out: A float (single number)
    """
    ### BEGIN SOLUTION
    return np.sum(np.multiply(x_i, w_l)) + b_l
    ### END SOLUTION
# Test cell: 'FC_two_loops_1' (5 points)

def FC_two_loops(x, w, b):
    """
    Inputs:
    - x: A numpy array of images of shape (N, H, W)
    - w: A numpy array of weights of shape (M, H, W)
    - b: A numpy vector of biases of size M

    Returns: 
    - out: a numpy array of shape (N, M)
    """
    N, H, W = x.shape
    M, _, _ = w.shape
    out = np.zeros((N,M))
    for ni in range(N):
           for mi in range(M):
                out[ni, mi] = two_inner_loops(x[ni,  :, :], w[mi,  :, :], b[mi])
    return out

num_inputs = 50
input_shape = (128, 256)
output_dim = 10

x = np.random.rand(num_inputs, *input_shape)
w = np.random.rand(output_dim, *input_shape)
b = np.random.rand(output_dim)

print("Checking the correctness of your implementation...")
out_fast = FC_two_loops(x, w, b)
out_naive = FC_naive(x, w, b)
error = rel_error(out_naive, out_fast)
print("==> Output error:", error)
assert error < 1e-12, "The value of your output is incorrect or not accurate enough"
print("==> This level of error is acceptable.")

print("\nBenchmarking your code...")
T_fast = %timeit -o FC_two_loops(x, w, b)
#start_time = time.time ()
#for i in range(5):
#    out_fast = FC_two_loops(x, w, b)
#elapsed_time_fast = (time.time () - start_time)/5
elapsed_time_fast = np.average(T_fast.all_runs) / T_fast.loops
print ("==> Took %g seconds." % elapsed_time_fast)

print("\nBenchmarking the naive code...")
T_naive = %timeit -o FC_naive(x, w, b)
#start_time = time.time ()
#for i in range(5):
#    out_naive = FC_naive(x, w, b)
#elapsed_time_naive = (time.time () - start_time)/5
elapsed_time_naive = np.average(T_naive.all_runs) / T_naive.loops
print ("==> Took %g seconds." % elapsed_time_naive)

speed_up = elapsed_time_naive/elapsed_time_fast
print("Speed-up:", speed_up)
assert speed_up >= 100, "The speed-up of your method is less than 100"

print("\n(Passed!)")
Checking the correctness of your implementation...
==> Output error: 6.40287404638248e-15
==> This level of error is acceptable.

Benchmarking your code...
18.4 ms ± 298 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
==> Took 0.0183686 seconds.

Benchmarking the naive code...
12 s ± 82.4 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
==> Took 12.0312 seconds.
Speed-up: 654.9841477884501

(Passed!)
Question 2 (5 points). Now, completely rewrite the FC_naive() function by at least 2,000 times.

This improvement can be attained with basic Numpy operations that you've learned (i.e., no "new" functions) and no explicit loops.

def FC_no_loop(x, w, b):
    """
    Inputs:
    - x: A numpy array of images of shape (N, H, W)
    - w: A numpy array of weights of shape (M, H, W)
    - b: A numpy vector of biases of size M

    Returns: 
    - out: a numpy array of shape (N, M)
    """
    N, H, W = x.shape
    M, _, _ = w.shape
    out = np.zeros((N,M))
    ### BEGIN SOLUTION
    x = np.reshape(x, (N, H*W))
    w = np.reshape(w, (M, H*W))
    out = x @ w.T + b
    # The following one-line solution, which Googling might give you, will work,
    # but it's likely it won't be fast enough in its current implementation.
#    out = np.einsum("nhw,mhw->nm", x, w) + b
    ### END SOLUTION
    return out
# Test cell: 'FC_no_loop' (5 points)
num_inputs = 50
input_shape = (128, 256)
output_dim = 10

x = np.random.rand(num_inputs, *input_shape)
w = np.random.rand(output_dim, *input_shape)
b = np.random.rand(output_dim)

print("Checking the correctness of your implementation...")
out_fast = FC_no_loop(x, w, b)
out_naive = FC_naive(x, w, b)
error = rel_error(out_naive, out_fast)
print("==> Output error:", error)
assert error < 1e-12, "The value of your output is incorrect or not accurate enough"
print("==> This level of error is acceptable.")

print("\nBenchmarking your code...")
T_fast = %timeit -o FC_no_loop(x, w, b)
elapsed_time_fast = np.average(T_fast.all_runs) / T_fast.loops
print ("==> Took %g seconds." % elapsed_time_fast)

print("\nBenchmarking the naive code...")
T_naive = %timeit -o FC_naive(x, w, b)
elapsed_time_naive = np.average(T_naive.all_runs) / T_naive.loops
print ("==> Took %g seconds." % elapsed_time_naive)

speed_up = elapsed_time_naive/elapsed_time_fast
print("Speed-up:", speed_up)
assert speed_up >= 2000, "The speed-up of your method is less than 2000"

print("\n(Passed!)")
Checking the correctness of your implementation...
==> Output error: 7.191896084646408e-15
==> This level of error is acceptable.

Benchmarking your code...
1.62 ms ± 4.03 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
==> Took 0.00162191 seconds.

Benchmarking the naive code...
12 s ± 147 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
==> Took 12.0018 seconds.
Speed-up: 7399.788227204887

(Passed!)
Fin! You've reached the end of this problem. Don't forget to restart the kernel and run the entire notebook from top-to-bottom to make sure you did everything correctly. If that is working, try submitting this problem. (Recall that you must submit and pass the autograder to get credit for your work!)
