import math

import numpy as np
import pandas as pd
from math import sqrt, acos, atan, asin, pi, radians, degrees

SCAN_NUM = 3


def find_intersection(A1, B1, C1, A2, B2, C2):
    determinant = A1 * B2 - A2 * B1
    if determinant == 0:
        return None
    x_intersection = (C2 * B1 - C1 * B2) / determinant
    y_intersection = - (A1 * C2 - A2 * C1) / determinant
    return x_intersection, y_intersection


def is_scanned(k, b, x, y, z, x_start, x_end):
    f1 = y - k * x - b + sqrt(3) * sqrt(k * k + 1) * z
    f2 = y - k * x - b - sqrt(3) * sqrt(k * k + 1) * z
    y_start = k * x_start + b
    y_end = k * x_end + b
    f3 = (k * (y - y_start) + x - x_start) * (k * (y - y_end) + x - x_end)
    if (f1 < 0) & (f2 > 0) & (f3 < 0):
        # if (f3 > 0):
        #     print(f"y={k}x+{b}")
        #     print(f"({x},{y})::{(k * (y - y_start) + x - x_start)} {(k * (y - y_end) + x - x_end)}")
        #     print(f"y:{y_start} {y_end}")
        #     print(f"x:{x_start} {x_end}")
        return True
    return False


def simulate_line(k, b, data, x_start, x_end, record):
    num_new = 0
    num_old = 0
    for item in data:
        if is_scanned(k, b, item[0], item[1], item[2], x_start, x_end):
            if item[SCAN_NUM] == 0:
                num_new += 1
            else:
                num_old += 1
            item[SCAN_NUM] += 1
    if num_old + num_new == 0:
        return None
    overlap = num_old / (num_new + num_old)
    length = sqrt(1 + k*k) * abs(x_end - x_start)
    if b >= 0:
        record.append([f"y={round(k, 6)}x+{round(b, 6)}", length, overlap])
    else:
        record.append([f"y={round(k, 6)}x{round(b, 6)}", length, overlap])
    return overlap


def find_rectangle(funcs, face):
    xn, yn, zn = -face[0], -face[1], -face[2]
    intersections = []
    intersection_num = len(funcs)
    for i in range(intersection_num):
        A1, B1, C1 = funcs[i][0], funcs[i][1], funcs[i][2]
        if i == 0:
            A2, B2, C2 = funcs[intersection_num - 1][0], funcs[intersection_num - 1][1], funcs[intersection_num - 1][2]
        else:
            A2, B2, C2 = funcs[i - 1][0], funcs[i - 1][1], funcs[i - 1][2]
        intersections.append(find_intersection(A1, B1, C1, A2, B2, C2))
    intersections = list(set(intersections))
    A = xn / sqrt(xn * xn + yn * yn)
    B = yn / sqrt(xn * xn + yn * yn)
    Cl = []
    Cr = []
    for i in range(intersection_num):
        Cl.append(-(A * intersections[i][0] + B * intersections[i][1]))
        Cr.append(-(A * intersections[i][1] - B * intersections[i][0]))
    max_cl = max(Cl)
    min_cl = min(Cl)
    max_cr = max(Cr)
    min_cr = min(Cr)
    print(f"{A}x+{B}y+{max_cl}=0")
    print(f"{A}x+{B}y+{min_cl}=0")
    print(f"{-B}x+{A}y+{max_cr}=0")
    print(f"{-B}x+{A}y+{min_cr}=0")
    L = (max_cl - min_cl) / sqrt(A * A + B * B)
    R = (max_cr - min_cr) / sqrt(A * A + B * B)
    G_1 = find_intersection(A, B, max_cl, -B, A, max_cr)
    G_2 = find_intersection(A, B, max_cl, -B, A, min_cr)
    G_3 = find_intersection(A, B, min_cl, -B, A, max_cr)
    G_4 = find_intersection(A, B, min_cl, -B, A, min_cr)

    peak = [G_1, G_2, G_3, G_4]
    origin = []
    depth = min(-(face[0] * G_1[0] + face[1] * G_1[1] + face[3]) / face[2],
                -(face[0] * G_2[0] + face[1] * G_2[1] + face[3]) / face[2],
                -(face[0] * G_3[0] + face[1] * G_3[1] + face[3]) / face[2],
                -(face[0] * G_4[0] + face[1] * G_4[1] + face[3]) / face[2])
    alpha = degrees(acos(abs(zn / sqrt(xn * xn + yn * yn + zn * zn))))

    for i in range(4):
        tolerance = 1e-6
        temp_depth = -(face[0] * peak[i][0] + face[1] * peak[i][1] + face[3]) / face[2]
        print(f"A:{face[0]} B:{face[1]} C:{face[2]} D:{face[3]}")
        # 检查 depth 是否在容差范围内
        print(f"{peak[i]} - dep:{temp_depth}")
        if abs(depth - temp_depth) < tolerance:
            origin.append(peak[i])
    # 两个点判断谁是原点，用0号点-1号点，点乘法向量投影旋转90°后的向量，若大于零则说明1号点在x轴小的一侧，为原点
    # x轴正向向量为 (-B, A) 向量1->0为(x0-x1, y0-y1)
    if ((origin[0][1] - origin[1][1]) * A - (origin[0][0] - origin[1][0]) * B) > 0:
        OP = origin[1]
    else:
        OP = origin[0]
    if A < 0:
        phi = 360 - degrees(acos(-B / sqrt(A * A + B * B)))
    else:
        phi = degrees(acos(-B / sqrt(A * A + B * B)))
    return [OP, phi, L, R, alpha, depth]


def preprocess(get_polygon_num, get_polygon, polygon_index):
    # 从Excel文件中读取数据到DataFrame
    linear_df = pd.read_excel('../excel/linear_output_7.xlsx')
    plane_df = pd.read_excel('../excel/plane_output_7.xlsx')

    # print(len(linear_df['Label'].values) - 1)
    total_func = []
    for _ in range(50):
        total_func.append([])

    if get_polygon_num:
        return linear_df['Label'].values[len(linear_df['Label'].values) - 1]
    for i in range(len(linear_df['Label'].values)):
        total_func[linear_df['Label'].values[i]].append([linear_df['A'].values[i],
                                                         linear_df['B'].values[i],
                                                         linear_df['C'].values[i]])
    # 获取第一行数据
    face = [plane_df.iloc[polygon_index].iloc[0],
            plane_df.iloc[polygon_index].iloc[1],
            plane_df.iloc[polygon_index].iloc[2],
            plane_df.iloc[polygon_index].iloc[3]]

    # print("over!")
    # print(total_func[0])
    if get_polygon:
        return total_func[polygon_index]
    return find_rectangle(total_func[polygon_index], face)


#
def simulate(k_trans_tot, b_trans_tot, start_tot, end_tot):
    df = pd.read_excel('../excel/interpolation.xlsx')

    data_size = len(df)

    # 初始化一个四维数据点的NumPy数组，所有元素初始值为0
    num_points = data_size
    num_dimensions = 4
    data = np.zeros((num_points, num_dimensions))
    # 将数据存储到NumPy数组的特定维度
    data[:, 0] = df['x'].values  # 存储到第一维
    data[:, 1] = df['y'].values  # 存储到第二维
    data[:, 2] = df['z'].values  # 存储到第三维

    record = []
    for i in range(len(k_trans_tot)):
        overlap = simulate_line(k_trans_tot[i], b_trans_tot[i], data, x_start=start_tot[i], x_end=end_tot[i], record=record)
        print(f"finish line{i}, overlap = {overlap}")
        print(f"y={k_trans_tot[i]}x+{b_trans_tot[i]}")
    df_record = pd.DataFrame(record)
    df_record.to_excel('record_7.xlsx', index=False)
    count_dict = {}

    # 遍历数据数组 data
    for i in range(len(data)):
        value = data[i][SCAN_NUM]
        if value in count_dict:
            count_dict[value] += 1
        else:
            count_dict[value] = 1

    num_scan_total = 0
    num_miss_total = count_dict[0]
    num_multi_total = 0
    num_total = len(data)
    # 输出每个取值对应的计数
    for value, count in count_dict.items():
        print("取值", value, "的总数为", count)
        if value != 0:
            num_scan_total += count
        if value > 1:
            num_multi_total += count
    print(f"总体丢失率：{(num_miss_total/num_total)}\n平均重叠率：{(num_multi_total/num_total)}")
    

    scanned_points = []
    for item in data:
        scanned_points.append([item[0], item[1], item[3]])

    df = pd.DataFrame(scanned_points, columns=["x", "y", "Label"])
    df.to_excel("scanned_points_7.xlsx", index=False)  # index=False表示不包含行索引

    print("数据已保存到 scanned_points.xlsx 文件")
