from functions import *

x = read_data('data/xc.dat')

for i in range(1, 10):
    y_file = f'data/yc-{i}.dat'
    y = read_data(y_file)

    stats = calculate_statistics(y)
    derivative = calculate_derivative(x, y)
    integral = calculate_integral(x, y)

    out_file = f'out_yc-{i}.dat'
    write_results(out_file, y_file, stats, derivative, integral)