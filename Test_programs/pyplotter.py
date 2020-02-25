import matplotlib.pyplot as plt
import numpy as np
import math
import csv

data_filepath = '../Results/CValTests.csv'

c_values = []
wins = []

with open(data_filepath) as csv_data_file:
    csv_reader = csv.reader(csv_data_file, delimiter=',')
    row_num = 0

    for row in csv_reader:
        if row_num != 0:
            c_values.append(float(row[0]))
            wins.append(float(row[1]))
        
        row_num += 1


plt.xlabel('C-Value')
plt.ylabel('Number of wins against standard value')
plt.title('Monte-Carloe C-Value testing')
plt.scatter(c_values, wins)

plt.show()