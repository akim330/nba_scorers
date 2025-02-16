import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

threes = pd.read_csv("threes.csv")
threes['PlayerName'] = threes['Player'].apply(lambda s: s.split('\\')[0])
threes['PlayerNameAbbrev'] = threes['PlayerName'].apply(lambda name: name.split(' ')[0][0] + ". " + name.split(' ')[1])
threes['3PT'] = threes['3P▼']
threes['3PA/G'] = threes['3PA'] / threes['G']
threes['3P%f'] = threes['3P%'].apply(lambda x: round(x * 100, 1))

data = threes[(threes['3PA/G'] >= 2) & (threes['3PT'] >= 25)]
x = '3PA/G'
y = '3P%f'

plt.style.use('fivethirtyeight')
# matplotlib.rcParams['font.family'] = "roboto"

fig, ax = plt.subplots(figsize=(7,5))
sns.scatterplot(data=data, x=x, y=y, s=1, ax=ax)
ax.set_xlabel("3PA per Game")
ax.set_ylabel("3PT Percentage")
ax.set_xticks(range(2, 14, 1))
ax.set_title("3-point Shooting: Efficiency vs Volume")
# plot.set_title("Minimum 2 attempts per game and 25 total made 3s")
for i in range(0,data.shape[0]):
    ax.text(data[x][i]+0.05, data[y][i],
     data['PlayerNameAbbrev'][i], horizontalalignment='left',
     size=6, color='black', weight='semibold')
fig.tight_layout()
plt.show()