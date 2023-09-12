from math import radians

import numpy as np


def transform_line(b, x_o, y_o, phi):
    # 定义旋转矩阵和平移向量
    rotation_matrix = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])
    translation_vector = np.array([x_o, y_o])

    # 在 O'x'y' 坐标系中选择两个点
    points_prime = np.array([[-1, b], [1, b]])

    # 转换到 Oxy 坐标系
    points = np.dot(rotation_matrix, points_prime.T).T + translation_vector

    # 计算直线的斜率和截距
    x1, y1 = points[0]
    x2, y2 = points[1]
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1

    print(f'y = {slope} * x + {intercept}')
    return slope, intercept

# 测试函数
# (9358.165855488067,1759.404907509646)
b = 8486.683869268403
x_o = 9358.165855488067
y_o = 1759.404907509646
phi = radians(103.29875428993601)
print(transform_line(b, x_o, y_o, phi))
