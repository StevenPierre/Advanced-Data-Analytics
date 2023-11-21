def rep_str (a, n):
    """Returns a string consisting of an input string repeated a given number of times."""
    assert type(a) is str and n >= 1
    return a * n
import re
# Set up an input problem
n = 3
s_n = rep_str ('a', n) # Input string
pattern = '^a{%d}$' % n # Pattern to match it exactly

# Test it
print ("Matching input '{}' against pattern '{}'...".format (s_n, pattern))
assert re.match (pattern, s_n) is not None

# Benchmark it & report time, normalized to 'n'
timing = %timeit -q -o re.match (pattern, s_n)
t_avg = sum (timing.all_runs) / len (timing.all_runs) / timing.loops / n * 1e9
print ("Average time per match per `n`: {:.1f} ns".format (t_avg))

# Use this code cell (and others, if you wish) to set up an experiment
# to test whether matching simple patterns behaves at worst linearly
# in the length of the input.

def setup_problem (n):
    s_n = rep_str('a', n)
    p = "^a{%d}$" % n
    print ("\n[n={}] Matching pattern '{}'...".format(n, p))
    assert re.match(p, s_n) is not None
    return (p, s_n)

N = [1000, 10000, 100000, 1000000]
T = []
for n in N:
    p, s_n = setup_problem (n)
    timing = %timeit -q -o re.match(p, s_n)
    T.append(sum(timing.all_runs) / len(timing.all_runs) / timing.loops / n * 1e9)
    print ("==> Average time per match per `n`: {:.1f} ns".format(T[-1]))

def setup_inputs(n):
    """Sets up the 'complex pattern example' above."""
    s_n = rep_str('a', n)
    p_n = "^(a?){%d}(a{%d})$" % (n, n)
    print ("[n={}] Matching pattern '{}' against input '{}'...".format(n, p_n, s_n))
    assert re.match(p_n, s_n) is not None
    return (p_n, s_n)

n = 3
p_n, s_n = setup_inputs(n)
timing = %timeit -q -o re.match(p_n, s_n)
t_n = sum(timing.all_runs) / len(timing.all_runs) / timing.loops / n * 1e9
print ("==> Time per run per `n`: {} ns".format(t_n))

# Use this code cell (and others, if you wish) to set up an experiment
# to test whether matching simple patterns behaves at worst linearly
# in the length of the input.

N = [3, 6, 9, 12, 15, 18]
T = []
for n in N:
    p_n, s_n = setup_inputs (n)
    timing = %timeit -q -o re.match (p_n, s_n)
    t_n = sum (timing.all_runs) / len (timing.all_runs) / timing.loops / n * 1e9
    print ("Time per run per `n`: {} ns".format (t_n))
    T.append (t_n)
