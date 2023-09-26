import numpy as np


def compute_mandelbrot(width, height, x_center, y_center, x_width, max_iter=1000):
    """
    Compute the Mandelbrot set for a sector.

    Params:
    - width, height: dimensions of the output grid in px.
    - x_center, y_center: center point of the view in the complex plane in Re, Im.
    - x_width: width of the view in the complex plane in Re.
    - max_iter: the max iteration depth for divergence.

    Return: 2D array of iteration counts, shape (width, height).
    """
    y_height = x_width * height / width

    # Generate complex-valued 2D grid
    x = np.linspace(x_center - x_width/2, x_center + x_width/2, width)
    y = np.linspace(y_center - y_height/2, y_center + y_height/2, height)
    x, y = np.meshgrid(x, y)
    c = x + 1j*y

    # Mandelbrot iteration
    z = np.zeros_like(c)
    iteration = np.zeros_like(c, dtype=int)
    for i in range(max_iter):
        not_diverged = np.abs(z) <= 2
        iteration[not_diverged] = i
        z[not_diverged] = z[not_diverged]**2 + c[not_diverged]

    # Mask points that remained bounded
    iteration[iteration == max_iter-1] = 0

    return iteration

