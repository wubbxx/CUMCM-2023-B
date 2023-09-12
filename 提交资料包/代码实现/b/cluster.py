import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

import numpy as np

n_samples = 50451
n_features = 6

new_data = np.empty((n_samples, n_features))

# 读取z.xlsx文件
input_file = 'data.xlsx'
df = pd.read_excel(input_file)


i = int(0)
for row in new_data:
    row[0] = df['x'][i]
    row[1] = df['y'][i]
    row[2] = df['z'][i]
    row[3] = df['xn'][i]*100000
    row[4] = df['yn'][i]*100000
    row[5] = df['zn'][i]*100000
    i += 1


# 使用K-means进行聚类
n_clusters = 4  # 聚类数量
n_init = 10     # 多次运行以找到最佳结果
max_iter = 300  # 最大迭代次数
tol = 1e-4      # 收敛容忍度


# distortions = []  # 用于存储簇内平方和
# K_range = range(1, 11)  # 尝试不同的k值范围
# for k in K_range:
#     # 创建KMeans对象
#     kmeans = KMeans(
#         n_clusters=k,
#         init="k-means++",
#         n_init=n_init,
#         max_iter=max_iter,
#         tol=tol,
#         random_state=42  # 随机数种子，可选
#     )
#     kmeans.fit(new_data)
#     distortions.append(kmeans.inertia_)
#
# plt.figure(figsize=(8, 6))
# plt.plot(K_range, distortions, marker='o')
# plt.xlabel('Number of Clusters (k)')
# plt.ylabel('Distortion (Inertia)')
# plt.title('Elbow Method for Optimal k')
# plt.grid(True)
# plt.show()

kmeans = KMeans(
    n_clusters=4,
    init="k-means++",
    n_init=n_init,
    max_iter=max_iter,
    tol=tol,
    random_state=42  # 随机数种子，可选
)
kmeans.fit(new_data)
# 将每个数据点的聚类标签添加到数据中
new_data_with_labels = np.column_stack((new_data, kmeans.labels_))

# 创建一个Pandas DataFrame来存储数据和标签
column_names = ['Dim' + str(i+1) for i in range(n_features)] + ['Label']
df = pd.DataFrame(new_data_with_labels, columns=column_names)

excel_file = "output.xlsx"

# 使用to_excel方法将DataFrame输出到Excel文件中
df.to_excel(excel_file, index=False, engine='openpyxl')

# 输出成功消息
print(f"DataFrame已成功输出到 {excel_file}")
