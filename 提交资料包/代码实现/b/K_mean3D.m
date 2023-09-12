% 读取xlsx文件
data = xlsread('output.xlsx');

% 提取Dim1、Dim2和Label列
Dim2 = data(:, 1);
Dim1 = data(:, 2);
Label = data(:, 7); % 将Dim7更改为Label

% 获取Label列的不同取值
unique_values = unique(Label);

% 为每个不同的Label取值分配不同的颜色
colors = jet(length(unique_values)); % 可以选择其他颜色映射

% 创建一个图形窗口
figure;

% 循环绘制散点图
for i = 1:length(unique_values)
    % 选择当前取值的数据点
    indices = Label == unique_values(i);
    
    % 绘制散点图，使用不同的颜色
    scatter(Dim1(indices), Dim2(indices), 50, colors(i, :), 'filled');
    hold on;
end

% 添加图例
legend(cellstr(num2str(unique_values)), 'Location', 'Best');

% 添加轴标签和标题
xlabel('Dim1');
ylabel('Dim2');
title('散点图');

% 可以根据需要自定义图形属性和样式
