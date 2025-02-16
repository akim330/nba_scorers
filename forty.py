import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text

# LOAD DATA

total = pd.read_csv("forty.csv")

total['Last Name'] = total['PLAYER'].apply(lambda s: s.split(' ')[1])
counts = total['Last Name'].value_counts()
last_name_copies = list(counts[counts>1].keys())

total['Standard Abbrev Name'] = total['PLAYER'].apply(lambda s: s.split(' ')[0][0] + ". " + s.split(' ')[1])
counts = total['Standard Abbrev Name'].value_counts()
abbrev_name_copies = list(counts[counts > 1].keys())

# Here I hand-code some abbreviations that are intuitive (for example having Giannis instead of Antetokounmpo or Lebron instead of James)
def get_abbrev(s):
    if 'Stephen Curry' in s:
        return 'Steph Curry'
    elif 'Seth Curry' in s:
        return 'Seth Curry'
    elif 'Durant' in s:
        return 'KD'
    elif 'Giannis' in s:
        return 'Giannis'
    elif 'LeBron' in s:
        return 'LeBron'
    elif 'Seth Curry' in s:
        return s
    elif 'DeRozan' in s:
        return 'DeRozan'
    elif s == 'Nick Richards':
        return s
    elif s == 'DeAndre Jordan':
        return 'DAJ'
    elif s == 'Fred VanVleet':
        return 'FVV'
    elif s == 'Anthony Davis':
        return 'AD'
    elif 'Shai' in s:
        return 'SGA'
    elif 'Jackson Jr.' in s:
        return 'JJJ'
    elif 'D\'Angelo' in s:
        return 'DLo'
    elif 'Towns' in s:
        return 'KAT'
    elif 'Caldwell-Pope' in s:
        return 'KCP'
    elif s == 'Paul George':
        return 'PG'
    elif 'Brogdan' in s:
        return 'Brogdan'
    elif s == 'Chris Paul':
        return 'CP3'
    elif s == 'Draymond Green':
        return 'Draymond'
    elif 'Luwawu' in s:
        return 'TLC'
    elif s == 'Javonte Green':
        return 'Javonte'
    elif s == 'Danny Green':
        return 'DG'
    elif s.split(' ')[0][0] + ". " + s.split(' ')[1] in abbrev_name_copies:
        return s
    elif s.split(' ')[1] in last_name_copies:
        return s.split(' ')[0][0] + ". " + s.split(' ')[1]
    else:
        return s.split(' ')[1]

total['Name Abbrev'] = total['PLAYER'].apply(get_abbrev)

total['ts'] = total.PTS / (2 * total.FGA + 0.88 * total.FTA)

plt.style.use('fivethirtyeight')
# matplotlib.rcParams['font.family'] = "roboto"

fig, ax = plt.subplots(figsize=(13,8))
sns.scatterplot(data=total, x='PTS', y='ts', s=3, ax=ax, color='black')
# graph = df.plot.scatter(x = x, y = y, s=3, ax=ax)
ax.set_xlabel("Volume: PTS")
ax.set_ylabel("Efficiency: TS%")
# ax.set_xticks(range(2, 14, 1))
# ax.set_title("Scoring: Efficiency vs Volume")

ax.set_xlim(left = 35, right = 60)
ax.set_ylim(bottom = 0.50, top = 1.0)

texts = []
for i in range(0,total.shape[0]):

    #
    # if df['TeamAbbreviation'].iloc[i] == 'GSW':
    #     color = 'tab:olive'
    # elif df['TeamAbbreviation'].iloc[i] == 'BOS':
    #     color = 'tab:green'
    # else:
    color = 'black'

    texts.append(ax.text(total['PTS'].iloc[i], total['ts'].iloc[i],
         total['Name Abbrev'].iloc[i] + ' ' + str(total['PTS'].iloc[i]) + ' ' + total['GAME DATE'].iloc[i][:-5] + ' ' + total['MATCH UP'].iloc[i][4:], horizontalalignment='left',
         size=5, color=color, weight='semibold'))

adjust_text(texts,
            arrowprops=dict(arrowstyle="-", color='k', lw=0.5),)

ax.set_title("Best 40/50-point Games", size = 40)

# fig.tight_layout()

plt.savefig("scorers.png")
plt.show()





