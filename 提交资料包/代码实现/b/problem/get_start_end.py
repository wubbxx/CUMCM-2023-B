import numpy as np
from matplotlib import pyplot as plt


def find_intersection(line1, line2):
    A1, B1, C1 = line1
    A2, B2, C2 = line2

    denominator = A1 * B2 - A2 * B1

    if denominator == 0:
        return None

    x = (B1 * C2 - B2 * C1) / denominator
    y = (A2 * C1 - A1 * C2) / denominator

    return x, y


# 传入的是按顺序排好的多边形边所在直线，和要求直线的 k 和 b
def get_start_end(lines, k, b):
    # 定义多边形的边
    # lines = [
    #     (-5.88, 0.44, 5.74),  # Line 1
    #     (-1.15, -6.44, 15.21),  # Line 2
    #     (3.34, -0.88, -23.67),  # Line 3
    #     (0.57, -3.16, 10.34)  # Line 4
    # ]

    # 找到多边形的顶点
    vertices = []
    for i in range(len(lines)):
        line1 = lines[i]
        line2 = lines[(i + 1) % len(lines)]
        vertex = find_intersection(line1, line2)
        if vertex:
            vertices.append(vertex)

    # 将顶点与相应的边关联
    edges_with_vertices = {}
    for i in range(len(lines)):
        edge = lines[i]
        vertex1 = vertices[i]
        vertex2 = vertices[(i - 1) % len(vertices)]
        edges_with_vertices[edge] = (vertex1, vertex2)

    # print(edges_with_vertices)
    # 绘制多边形
    polygon = plt.Polygon(vertices, fill=None, edgecolor='r')
    plt.gca().add_patch(polygon)

    # 给定另一条直线 y = kx + b
    # k = 0.18
    # b = 1.03
    another_line = (-k, 1, -b)

    # 找到这条直线与多边形的交点
    intersection_points = []
    for edge in lines:
        intersection = find_intersection(edge, another_line)
        if intersection:
            vertex1, vertex2 = edges_with_vertices[edge]
            x, y = intersection
            x1, y1 = vertex1
            x2, y2 = vertex2
            # 检查交点是否在边上
            if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
                intersection_points.append(intersection)

    # print("Intersection points:", list(intersection_points[:2]))

    # 画画验证正确性
    # x_values = np.linspace(min([x for x, y in vertices]) - 1, max([x for x, y in vertices]) + 1, 400)
    # y_values = k * x_values + b
    # # 绘制直线
    # plt.plot(x_values, y_values, label='y=kx+b')
    #
    # # 设置图表
    # plt.axis('equal')
    # plt.grid(True)
    # plt.legend()
    # plt.show()

    return intersection_points
