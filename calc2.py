import numpy as np

DOUBLE_BYTES_SIZE = 8
X_MIN, X_MAX = 0, 1
Y_MIN, Y_MAX = 0, 1


def get_x_and_y(data):
    data = data[DOUBLE_BYTES_SIZE * 2:]
    length = len(data)
    data = data[:length - length % DOUBLE_BYTES_SIZE]
    values = np.frombuffer(data, dtype=np.dtype(float))[:-1]

    half_length = len(values) // 2
    x, y = values[:half_length], values[half_length:]
    return normalize(x, y)


def normalize(x, y):
    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)
    xmax_minus_xmin = x_max - x_min
    ymax_minus_ymin = y_max - y_min

    return [(el - x_min) / xmax_minus_xmin for el in x],\
           [(el - y_min) / ymax_minus_ymin for el in y]


def dots_in_range(data, size, delta_x, delta_y):
    points = zip(*data)
    x_size, y_size = size
    x_min = x_size * delta_x
    x_max = x_min + x_size
    y_min = y_size * delta_y
    y_max = y_min + y_size

    def filter_func(point):
        x, y = point
        return x_min <= x < x_max and y_min <= y < y_max

    points_in_square = filter(filter_func, points)
    return len(list(points_in_square))