import numpy as np

def white_noise(
    n = 10,
    var = 10,
    seed = False 
):
    """
    Generate white noise.

    args:
        n: Number of time points.
        var: The variance.
        seed: Seed for reproducible experiments. Default is false.
    
    """
    time = np.arange(n)

    if seed is False:
        values = np.random.randn(n)*var
    else:
        np.random.seed(seed)
        values = np.random.randn(n)*var

    return time, values
