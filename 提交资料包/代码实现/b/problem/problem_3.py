from math import radians, pi, tan, sin, cos, atan, sqrt

from scipy.optimize import fsolve

from draw import drawPlot

theta = radians(120)
alpha = radians(1.5)


def get_depth(y):
    return 110 - (y - 2 * 1852) * tan(alpha)


# 获得给定 y 值的 覆盖范围
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


# y1 是截距大的直线上的y， y2 是小的， beta 是当前的航线方向
# 输入要保证 y1 > y2
def cal_eta(y1, y2, beta):
    if y1 < y2:
        print("fffffffffffffffffffffffffffffffffffffffffffffffffffff")
    line_k = tan(beta - pi / 2)
    L = (line_k * line_k + 1) ** 0.5 * abs(y1 - y2)
    gamma = atan(tan(alpha) * sin(beta))

    W1_right = get_depth(y1) * sin(theta / 2) * cos(gamma) * (1 / cos(theta / 2 + gamma))
    W2_left = get_depth(y2) * sin(theta / 2) * cos(gamma) * (1 / cos(theta / 2 - gamma))

    W1 = get_depth(y1) * sin(theta / 2) * cos(gamma) * (1 / cos(theta / 2 + gamma) + 1 / cos(theta / 2 - gamma))

    eta = (W1_right + W2_left - L) / W1
    return eta


# 找到和矩形的交点，没有返回 None
def find_intersections(k, b):
    x_max = 1852 * 2
    y_max = 1852 * 4

    # 初始化交点列表
    intersections = set()

    # 与 x 轴的交点 (y = 0)
    x_intersect_x_axis = -b / k
    if 0 <= x_intersect_x_axis <= x_max:
        intersections.add((x_intersect_x_axis, 0))

    # 与 y 轴的交点 (x = 0)
    y_intersect_y_axis = b
    if 0 <= y_intersect_y_axis <= y_max:
        intersections.add((0, y_intersect_y_axis))

    # 与 x = x_max 的交点
    y_intersect_x_max = k * x_max + b
    if 0 <= y_intersect_x_max <= y_max:
        intersections.add((x_max, y_intersect_x_max))

    # 与 y = y_max 的交点
    x_intersect_y_max = (y_max - b) / k
    if 0 <= x_intersect_y_max <= x_max:
        intersections.add((x_intersect_y_max, y_max))

    if len(intersections) >= 2:
        return list(intersections)[:2]
    elif len(intersections) == 1:
        return list(intersections)
    else:
        return None


# b_prime 是新的截距
# 找到原先直线上的两个点到新直线上的交点，做垂线段，以便于计算重复率
def find_perpendicular_intersections(k, b, b_prime, leftPoint, rightPoint):
    x1, y1 = leftPoint
    x2, y2 = rightPoint

    # 计算垂线的截距
    c1 = y1 + x1 / k
    c2 = y2 + x2 / k

    # 计算交点的 x 坐标
    x3 = (c1 - b_prime) / (k + 1 / k)
    x4 = (c2 - b_prime) / (k + 1 / k)

    # 计算交点的 y 坐标
    y3 = k * x3 + b_prime
    y4 = k * x4 + b_prime

    return (x3, y3), (x4, y4)


# 测试函数
k = 2  # 斜率
b = 0  # 截距
b_prime = 2  # 新的截距
leftPoint = (1, 2)  # 左点
rightPoint = (3, 6)  # 右点

print(find_perpendicular_intersections(k, b, b_prime, leftPoint, rightPoint))


# 找到第一条直线
def equation_first_line(b, k, beta):
    y = (3704 * k + b) / (k * k + 1)
    d = abs(3704 * k + b) / ((k * k + 1) ** 0.5)
    return get_w(y, beta, 'right') - d


from sko.DE import DE
import numpy as np


# 目标函数
def obj_func(p):
    new_b = p[0]
    new_leftPoint, new_rightPoint = find_perpendicular_intersections(cur_k, cur_b, new_b, leftPoint, rightPoint)
    eta_left = cal_eta(new_leftPoint[1], leftPoint[1], beta)
    eta_right = cal_eta(new_rightPoint[1], rightPoint[1], beta)

    if 0.1 < eta_left < 0.2 and 0.2 > eta_right > 0.1:
        return -new_b  # 我们取负号是因为 DE 是最小化算法，而我们想要最大化 new_b
    else:
        return np.inf  # 不满足条件则返回无穷大


# Example usage
cur_k = 1
cur_b = 0
leftPoint = (1, 1)
rightPoint = (3, 3)
beta = radians(135)
# new_b = genetic_algorithm(cur_k, cur_b, leftPoint, rightPoint, beta)
beta_total = []
length_total = []
for beta_degree in range(9002, 9100, 2):

    k_values = []
    b_values = []

    print(f'                calculating beta as {beta_degree}')
    beta = radians(1.0 * beta_degree / 100)
    cur_k = tan(beta - pi / 2)

    # first line
    # 交点
    b_value = fsolve(lambda b: equation_first_line(b, cur_k, beta), 0.0)
    print(b_value[0])

    cur_b = b_value[0]

    success_flag = False
    cur_length_total = 0
    while True:
        # 求线段起始点的设的在x轴上的点 (left_on_x,0)
        # d =

        intersections = find_intersections(cur_k, cur_b)

        if intersections is None:
            print('                    succeed')
            success_flag = True
            break

        k_values.append(cur_k)
        b_values.append(cur_b)

        leftPoint = intersections[1]
        rightPoint = intersections[0]
        cur_length_total += ((leftPoint[0] - rightPoint[0]) ** 2 + (leftPoint[1] - rightPoint[1]) ** 2) ** 0.5

        de = DE(func=obj_func, n_dim=1, lb=[cur_b], ub=[cur_b + 1000])
        best_new_b, _ = de.run()
        best_new_b = best_new_b[0]

        new_leftPoint, new_rightPoint = find_perpendicular_intersections(cur_k, cur_b, best_new_b, leftPoint, rightPoint)
        eta_left = cal_eta(new_leftPoint[1], leftPoint[1], beta)
        eta_right = cal_eta(new_rightPoint[1], rightPoint[1], beta)
        print(f'eta left : {eta_left}, eta right : {eta_right}')


        p = [best_new_b]
        if obj_func(p) == np.inf:
            print('                    severe violation!!!!!!!!!!!!!!!!!!!!!')

            break

        print(f"new_b is {best_new_b}")
        if best_new_b is None:
            break
        cur_b = best_new_b
        # find_perpendicular_intersections(cur_k, cur_b,, leftPoint, rightPoint)

    # drawPlot(k_values, b_values)


    if success_flag:
        print(f'^^^^^^^^^^^^^^^^^^^^^^total length is {cur_length_total}')
        beta_total.append(beta_degree)
        length_total.append(cur_length_total)


print(beta_total)
print(length_total)