from math import radians, pi, tan, sin, cos, atan, sqrt

from scipy.optimize import fsolve

from draw import drawPlot

theta = radians(120)
alpha = radians(1.5)


def get_depth(y):
    return 110 - (y - 2 * 1852) * tan(alpha)


def get_w(y, beta, str):
    D = get_depth(y)
    gamma = atan(tan(alpha) * sin(beta))
    W_left = D * sin(theta / 2) * cos(gamma) * (1 / cos(theta / 2 - gamma))
    W_right = D * sin(theta / 2) * cos(gamma) * (1 / cos(theta / 2 + gamma))
    if str == 'left':
        return W_left
    elif str == 'right':
        return W_right
    else:
        return W_left + W_right


def equation_first_line(y):
    return get_w(y, pi / 2, 'right') - y


def equation_parallel(next_y, y):
    last_left = get_w(y, pi / 2, 'left')
    next_right = get_w(next_y, pi / 2, 'right')
    eta = (last_left + next_right - (next_y - y)) / get_w(next_y, pi / 2, '')
    return eta - 0.1


def solve_first_line():
    return fsolve(lambda y: equation_first_line(y), 0)[0]

def solve_parallel(y):
    return fsolve(lambda next_y: equation_parallel(next_y, y), 0)[0]

k_values = []
b_values = []

# 找到和矩形的交点，没有返回 None
total_length = 0
first_y = solve_first_line()
print(first_y)
cur_y = first_y
k_values.append(0.0)
b_values.append(cur_y)


while cur_y <= 1852 * 4:
    total_length += 1852 * 2
    next_yy = solve_parallel(cur_y)
    cur_y = next_yy
    k_values.append(0.0)
    b_values.append(cur_y)
    print(cur_y)

drawPlot(k_values, b_values)
print(total_length)