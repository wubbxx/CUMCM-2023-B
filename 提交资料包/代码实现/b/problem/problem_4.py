from math import radians, pi, tan, sin, cos, atan

from scipy.optimize import fsolve

from b.problem.get_start_end import get_start_end
from b.simulate import preprocess, simulate
from draw import drawPlot

from b.problem.rotate import transform_line


def get_depth(y):
    return D0 - y * tan(alpha)


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
    return eta - precise


def solve_first_line():
    return fsolve(lambda y: equation_first_line(y), 0)[0]


def solve_parallel(y):
    return fsolve(lambda next_y: equation_parallel(next_y, y), y)[0]


theta = radians(120)

k_trans_tot = []
b_trans_tot = []
start_tot = []
end_tot = []
polygon_num = preprocess(get_polygon_num=True, get_polygon=False, polygon_index=0)

print(f'polygon_num is {polygon_num}')

for polygon_index in range(polygon_num + 1):

    unformat_lines = preprocess(get_polygon_num=False, get_polygon=True, polygon_index=polygon_index)
    lines = []
    for line in unformat_lines:
        A, B, C = line[0], line[1], line[2]
        lines.append((A, B, C))

    print(lines)
    OP, phi, L, R, alpha, depth = preprocess(get_polygon_num=False,
                                             get_polygon=False,
                                             polygon_index=polygon_index)

    print(f'OP, phi, L, R, alpha, depth: {OP, phi, L, R, alpha, depth}')
    print(f'lines: {lines}')
    alpha = radians(alpha)
    D0 = -depth  # 最深的
    max_y = L  # R

    precise = 0.10

    k_values = []
    b_values = []

    # 找到和矩形的交点，没有返回 None
    total_length = 0
    first_y = solve_first_line()
    print(first_y)
    cur_y = first_y
    k_values.append(0.0)
    b_values.append(cur_y)

    cnt = 0
    while cur_y <= max_y:
        total_length += 1852 * 2
        next_yy = solve_parallel(cur_y)
        cur_y = next_yy
        k_values.append(0.0)
        b_values.append(cur_y)
        print(cur_y)

    # drawPlot(k_values, b_values)
    print(total_length)

    k_temp_tot = []
    b_temp_tot = []
    start_temp_tot = []
    end_temp_tot = []

    for b_value in b_values:
        k_trans, b_trans = transform_line(b_value, OP[0], OP[1], radians(phi))
        k_temp_tot.append(k_trans)
        b_temp_tot.append(b_trans)

    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! there are {len(k_temp_tot)} lines !!!!!!!!!!!!!!!!")
    print(len(k_temp_tot))
    print(len(b_temp_tot))
    print(len(start_temp_tot))
    print(len(end_temp_tot))
    # for b_value in

    # 测试一下没问题
    # lines = [
    #     (-5.88, 0.44, 5.74),  # Line 1
    #     (-1.15, -6.44, 15.21),  # Line 2
    #     (3.34, -0.88, -23.67),  # Line 3
    #     (0.57, -3.16, 10.34)  # Line 4
    # ]
    # k = 0.18
    # b = 1.03
    #
    # ret = get_start_end(lines, k, b)
    # print(ret)
    flag1 = len(k_temp_tot) == 7
    flag2 = len(k_temp_tot) == 14
    flag3 = len(k_temp_tot) == 36

    # if not flag3: continue
    for i in range(len(k_temp_tot)):

        k, b = k_temp_tot[i], b_temp_tot[i]
        intersections = get_start_end(lines, k, b)
        # print(f'line is y = {k}x + {b}, and intersections are {intersections}')
        # print(intersections)
        if len(intersections) == 2:

            x1, x2 = intersections[0][0], intersections[1][0]
            if flag1 and i < 3:
                start_temp_tot.append(min(x1, x2)-1000)
                end_temp_tot.append(max(x1, x2)+1000)
            elif flag2 and i == 0:
                start_temp_tot.append(min(x1, x2) - 200)
                end_temp_tot.append(max(x1, x2) + 500)
            elif flag3 and i == 0:
                start_temp_tot.append(min(x1, x2) - 100)
                end_temp_tot.append(max(x1, x2) + 300)
            else:
                start_temp_tot.append(min(x1, x2))
                end_temp_tot.append(max(x1, x2))
        else:
            start_temp_tot.append(0)
            end_temp_tot.append(0)

    k_trans_tot += k_temp_tot
    b_trans_tot += b_temp_tot
    start_tot += start_temp_tot
    end_tot += end_temp_tot
    # break

print(len(k_trans_tot))
print(len(b_trans_tot))
print(len(start_tot))
print(len(end_tot))
length_tot = 0
for i in range(len(k_trans_tot)):
    length_tot += abs(start_tot[i] - end_tot[i]) * (k_trans_tot[i] ** 2 + 1) ** 0.5

print(f'lines_tot  is {len(k_trans_tot)} !!!!!!!!!!!!!!!!!!')
print(f'length_tot is {length_tot} !!!!!!!!!!!!!!!!!!!!!!!!')


import matplotlib.pyplot as plt
import numpy as np

vectors = []
for i in range(len(k_trans_tot)):
    vector = (k_trans_tot[i], b_trans_tot[i], start_tot[i], end_tot[i])
    vectors.append(vector)

# 向量列表，每个向量是一个四元组（k, b, start, end）
# vectors = [(1, 0, 0, 5), (2, 1, 0, 4), (-1, 3, 1, 6)]
plt.show()

for vector in vectors:
    k, b, start, end = vector
    y = np.linspace(start, end, 100)  # 在start和end之间生成100个点
    x = k * y + b  # 计算对应的y值
    print(f'y = {k}x + {b}, {start} <= x <= {end}')
    plt.plot(x, y, label=f'y = {k}x + {b}')  # 画线并添加标签
    # plt.show()
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('')
# plt.legend()
plt.ylim(0, plt.ylim()[1])
plt.xlim(0, plt.xlim()[1])
plt.grid(True)
plt.show()




simulate(k_trans_tot=k_trans_tot, b_trans_tot=b_trans_tot, start_tot=start_tot, end_tot=end_tot)
