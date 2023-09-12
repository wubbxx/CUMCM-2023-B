import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# 指定Excel文件路径
excel_file_path = 'linear_output.xlsx'

# 使用pandas读取Excel文件
df = pd.read_excel(excel_file_path)

plt.figure(figsize=(8, 8))
x_min, x_max = 0, 10000
y_min, y_max = 0, 10000
x = np.linspace(x_min, x_max, 400)
# 打印每行数据的前三列
for index, row in df.iterrows():
    # 提取前三列数据
    data = row[:4]
    A, B, C = data[0], data[1], data[2]
    if data[3] != 2:
        continue
    if B == 0:
        B = 0.01
    y = (-A * x - C) / B
    plt.plot(x, y, label=f'{A}x + {B}y + {C} = 0')
    print(f"{data[0]}*x+{data[1]}*y+{data[2]}=0")

# 设置图形标题和标签
plt.title('Lines')
plt.xlabel('x')
plt.ylabel('y')

# 设置坐标轴范围
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

# 添加图例
# plt.legend()

# 显示图形
plt.grid()
plt.show()


