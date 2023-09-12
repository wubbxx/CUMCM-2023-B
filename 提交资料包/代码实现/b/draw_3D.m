% 读取整个表格
[num, txt, raw] = xlsread('real.xlsx');

% 提取 x, y 轴坐标和高度
x = num(1, 2:end);  % 第一行（除去第一个元素）是 x 轴坐标
y = num(2:end, 1);  % 第一列（除去第一个元素）是 y 轴坐标
z = 0 - num(2:end, 2:end);  % 其他单元格是高度

% 创建 x, y 网格
[Y, X] = meshgrid(x, y);

% 使用 surf 绘制三维图
figure; % 创建一个新的图形窗口
surf(X, Y, z);
hold on; % 保持当前图形

% 添加标签和标题
xlabel('X-axis');
ylabel('Y-axis');
zlabel('Height');
title('3D Surface Plot');

% colormap(parula);
a = -0.009635238

b = -0.002961582

d = 2.109046245


% 绘制新的平面
% 例如，绘制一个平面 z = 0.5（可以根据需要更改平面方程）
%new_plane = a*x + b*y + d;
%surf(X, Y, new_plane, 'FaceColor', 'r', 'FaceAlpha', 0.5); % 'FaceColor' 和 'FaceAlpha' 可以根据需要自定义

% 添加图例（可选）
legend({'Surface', 'New Plane'});

% 恢复默认的绘图状态
hold off;
