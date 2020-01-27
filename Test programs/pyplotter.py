import matplotlib.pyplot as plt
import numpy as np
import math


wins = [50, 45, 14, 17]
losses = [0, 4, 36, 31]
draws = [0 , 1, 0, 2]
tags = ['Random', 'Roxanne', 'MC-10', 'CNN-6']
width = 0.3






plt.xticks(np.arange(len(wins)) + width, tags)
plt.xlabel('Agent')
plt.ylabel('No. of games')
plt.title('MC-1 game results (50 games)')
plt.bar(np.arange(len(wins)), wins, width=width, label='Wins')
plt.bar(np.arange(len(losses)) + width, losses, width=width, label='Losses')
plt.bar(np.arange(len(draws)) + width * 2, draws, width=width, label='Ties')

plt.legend(loc='upper right')

plt.show()