import math
from math import radians, sin, cos, tan, pi

alpha = radians(0.47)  # 斜面倾角
theta = radians(120)  # 多波束换能器的开角
d = 50  # 测线间距
ans_left = []  # 左覆盖宽度
ans_right = []  # 右覆盖宽度

for i in range(9):
    L = -800 + i * d
    D = 70 - L * tan(alpha)
    up = sin(theta / 2) * cos(alpha) * D
    ans_left.append(up / cos(alpha + theta / 2))
    ans_right.append(up / cos(alpha - theta / 2))
    # print(up / cos(alpha + theta / 2), up / cos(alpha - theta / 2))

print("problem 1:")
for i in range(9):
    W = ans_left[i] + ans_right[i]
    if i == 0:
        print(f'W : {W}')
    if i != 0:
        overlap = ans_right[i - 1] + ans_left[i] - d
        eta = 1.0 * (overlap / W)
        print(f'W : {W} eta: {eta}')
