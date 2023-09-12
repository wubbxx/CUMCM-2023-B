import math
from math import sin, cos, tan, pi, atan, radians

# 初始化一个空的列表来存储数据
table = []

theta = math.radians(120)
alpha = math.radians(1.5)

# 横坐标: beta_degree (角度)
# 纵坐标: L (长度)
for beta_degree in range(0, 360, 45):
    row = []
    for i in range(0, 9):
        L = 0.3 * i * 1852
        beta = radians(beta_degree)
        gamma = atan(tan(alpha) * sin(beta))
        phi = atan(-tan(alpha) * cos(beta))
        D = 120 - L * tan(phi)
        W = D * sin(theta / 2) * cos(gamma) * (1 / cos(theta / 2 + gamma) + 1 / cos(theta / 2 - gamma))
        row.append(W)
        # print(f'W: {W} eta: {(W-500)/W}')
    table.append(row)

# 打印表头
print("Beta\\L", end='\t')
for i in range(0, 9):
    print(f"{0.3 * i:.2f}", end='\t')
print()

# 打印数据行
for beta_degree, row in zip(range(0, 360, 45), table):
    print(beta_degree, end='\t')
    for item in row:
        print(f"{item:.3f}", end='\t')
    print()



# for i in range(7):
#     beta = math.radians(i * 45)
#     alpha = math.atan(math.sin(beta) * math.tan(math.radians(1.5)))
#     for j in range(7):
#         L = j * 0.3 * 1852
#         D = 120 + L * math.tan(atan(math.radians(1.5) * math.sin(beta - 90)))
#         up = math.sin(theta / 2) * math.cos(alpha) * D
#         left = up / math.cos(alpha + theta / 2)
#         right = up / math.cos(alpha - theta / 2)
#         W = left + right
#         print(W, end=" ,")
#     print("")
