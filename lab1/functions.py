import numpy as np


def read_data(filename, method='np.loadtxt'):
    if method == 'open':
        with open(filename, 'r') as f:
            data = [float(line.strip()) for line in f]
        return data
    elif method == 'np.loadtxt':
        return np.loadtxt(filename)
    else:
        raise ValueError("Method must be 'open' or 'np.loadtxt'")


def calculate_statistics(y):
    y_array = np.array(y)
    return {
        'mean': np.mean(y_array),
        'max': np.max(y_array),
        'min': np.min(y_array)
    }


def calculate_derivative(x, y):
    return np.gradient(y, x)


def calculate_integral(x, y):
    x = np.asarray(x)
    y = np.asarray(y)
    dx = x[1:] - x[:-1]
    return np.sum(y[:-1] * dx)


def write_results(filename, original_name, stats, derivative, integral):
    with open(filename, 'w') as f:
        f.write(f"Source file: {original_name}\n")
        f.write("Statistics:\n")
        f.write(f"Mean: {stats['mean']:.6f}\n")
        f.write(f"Max: {stats['max']:.6f}\n")
        f.write(f"Min: {stats['min']:.6f}\n")
        f.write("Derivative:\n")
        f.write(' '.join(f"{val:.6f}" for val in derivative) + '\n')
        f.write(f"Integral: {integral:.6f}\n")