import matplotlib.pyplot as plt

# Given x and y values
x_values = [9002, 9004, 9006, 9008, 9010, 9012, 9014, 9016, 9018, 9020, 9022, 9024, 9026, 9028, 9030, 9032, 9034, 9036,
            9038, 9040]

y_values = [125936.00767246024, 125936.03068984582, 125936.06905217035, 125936.12275945765, 125936.19181174028,
            125936.27620906041, 125936.37595146924, 125936.49103902743, 125936.62147180559, 125936.76724988277,
            125936.92837334797, 125937.10484229948, 125937.29665684447, 125937.50381709979, 125937.72632319202,
            125937.96417525664, 125938.21737343815, 125938.48591789135, 125938.76980877973, 125939.0690462759
            ]

# Round y-values to 3 decimal places
y_values_rounded = [round(y, 3) for y in y_values]

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(x_values, y_values_rounded, color='blue', label='Data Points')  # Plot points
plt.plot(x_values, y_values_rounded, color='red', label='Line')  # Plot line

# Set axis labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis (Rounded to 3 decimal places)')
plt.title('Plot with Large Y-values but Small Differences')

# Add grid for better visibility of points
plt.grid(True)

# Add legend
plt.legend()

# Show the plot
plt.show()
