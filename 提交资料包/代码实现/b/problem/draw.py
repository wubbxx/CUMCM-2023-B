import matplotlib.pyplot as plt
import numpy as np


def drawPlot(k_values, b_values):
    # 定义矩形的边界
    x_max = 1852 * 2
    y_max = 1852 * 4

    # 创建矩形的顶点
    rectangle_x = [0, x_max, x_max, 0, 0]
    rectangle_y = [0, 0, y_max, y_max, 0]

    # 绘制矩形
    plt.plot(rectangle_x, rectangle_y, label='Rectangle', linewidth=2, color='black')

    # # 定义一组 k 和 b 的值
    # k_values = [1, 0.5, -1, -0.5]
    # b_values = [0, 1000, 2000, 3000]

    # 创建 x 值的数组
    x_values = np.linspace(0, x_max, 400)

    # 绘制直线
    for k, b in zip(k_values, b_values):
        y_values = k * x_values + b
        plt.plot(x_values, y_values, label=f'y = {k}x + {b}')

    # 设置坐标轴范围和标签
    plt.xlim(0, x_max)
    plt.ylim(0, y_max)
    plt.xlabel('x')
    plt.ylabel('y')

    # 添加图例
    # plt.legend()

    # 显示图形
    plt.show()
