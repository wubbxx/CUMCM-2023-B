% 读取xlsx文件
data = xlsread('problem/scanned_points_7.xlsx');

% 提取Dim1、Dim2和Label列
Dim1 = data(:, 2);
Dim2 = data(:, 1);
Label = data(:, 3);

% 获取Label列的不同取值
unique_values = unique(Label);

% 为每个不同的Label取值分配不同的颜色
colors = [
    1 0 0;  % 红色
    0 1 0;  % 绿色
    1 1 0;  % 黄色
    1 0 1;  % 紫色
    0.5 0 0.5;
    0 0 0;
];

% 创建一个图形窗口
figure;


% 循环绘制散点图
for i = 1:length(unique_values)
    % 选择当前取值的数据点
    indices = Label == unique_values(i);

    % 添加if语句进行条件筛选

    % if (Dim1(i) < 1852 * 5 / 2) && (Dim2(i) < 1852 * 2)
        % 绘制散点图，使用不同的颜色
        scatter(Dim1(indices), Dim2(indices), 50, colors(i, :), 'filled');
    % end

    hold on;
end


% 添加图例
legend(cellstr(num2str(unique_values)), 'Location', 'Best');

% 添加轴标签和标题
xlabel('南北距离/m');
ylabel('东西距离/m');
title('7');
