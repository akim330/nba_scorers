import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text

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
    elif get_standard_abbrev(s) in abbrev_name_copies:
        return s
    elif get_last_name(s) in last_name_copies:
        return  get_standard_abbrev(s)
    else:
        return get_last_name(s)

def get_last_name(s):
    try:
        return s.split(' ')[1]
    except IndexError:
        return s

def get_standard_abbrev(s):
    try:
        return s.split(' ')[0][0] + ". " + s.split(' ')[1]
    except IndexError:
        return s

total = pd.DataFrame()

for i in range(2001, 2022):
    scoring_temp = pd.read_csv(f"scoring_{str(i)}.csv")
    foul_temp = pd.read_csv(f"fouls_{str(i)}.csv")

    scoring_temp['Last Name'] = scoring_temp['Name'].apply(get_last_name)
    counts = scoring_temp['Last Name'].value_counts()
    last_name_copies = list(counts[counts > 1].keys())

    scoring_temp['Standard Abbrev Name'] = scoring_temp['Name'].apply(get_standard_abbrev)
    counts = scoring_temp['Standard Abbrev Name'].value_counts()
    abbrev_name_copies = list(counts[counts > 1].keys())

    scoring_temp['Name Abbrev'] = scoring_temp['Name'].apply(get_abbrev)
    scoring_temp['Name Abbrev Year'] = scoring_temp['Name Abbrev'].apply(lambda s: s + ' \'' + str(i)[2:])

    total = pd.concat([total, pd.merge(scoring_temp, foul_temp, how='inner', on='Name')])


total['Shots'] = total['FG2A'] + total['FG3A'] + (
            total['TwoPtShootingFoulsDrawn'] + total['ThreePtShootingFoulsDrawn'] + total['NonShootingFoulsDrawn'] -
            total['2pt And 1 Free Throw Trips'] - total['3pt And 1 Free Throw Trips'])
total['PPP'] = total['Points'] / total['Shots']
total['Shots Per Game'] = total['Shots'] / total['GamesPlayed_x']
total['myPPG'] = total['PPP'] * total['Shots Per Game']
total['True Fouls'] = total['Shots'] - total['FG2A'] - total['FG3A']
total['Est Fouls'] = total['FTA'] * 0.44


total_games = np.max(total['GamesPlayed_x'])
min_games = total_games * 0.6
min_ppp = 1.2
min_ppg = 25
min_shots = 25

df = total[(total['GamesPlayed_x'] > min_games) & ((total['myPPG'] > min_ppg) | (total['Shots Per Game'] > min_ppg))]


def search(s):
    return df[df['Name Abbrev'].apply(lambda name: s in name)]


x = 'Shots Per Game'
y = 'PPP'

plt.style.use('fivethirtyeight')
# matplotlib.rcParams['font.family'] = "roboto"

fig, ax = plt.subplots(figsize=(13, 8))
sns.scatterplot(data=df, x=x, y=y, s=3, ax=ax)
# graph = df.plot.scatter(x = x, y = y, s=3, ax=ax)
ax.set_xlabel("Volume: Shot attempts per game")
ax.set_ylabel("Efficiency: Points per shot")
# ax.set_xticks(range(2, 14, 1))
# ax.set_title("Scoring: Efficiency vs Volume")
x_min = 18
x_max = 34
y_min = 0.95
y_max = 1.55
ax.set_xlim(left=x_min, right=x_max)
ax.set_ylim(bottom=y_min, top=y_max)

xs = np.arange(x_min, x_max, 0.01)
curve_values = [15, 25, 30, 35]

colors = ['grey', '#fc4f30', '#e5ae38', '#6d904f', '#810f7c', '#8b8b8b', '#008fd5', ]
curves = []

# MAJOR CURVES
for i, value in enumerate(curve_values):
    curve = value / xs
    ax.plot(xs, curve, '-', color=colors[i], linewidth=0.5)
    if value not in [0, 15]:
        if value == 25:
            ax.text(value / (1.4) + 0.2, 1.4, f'{value} PPG', horizontalalignment='left',
                verticalalignment='bottom',
                size=7, color=colors[i], weight='semibold')
        else:
            ax.text(value / (y_max - 0.025), y_max - 0.025, f'{value} PPG', horizontalalignment='left',
                verticalalignment='bottom',
                size=7, color=colors[i], weight='semibold')
    curves.append(curve)

curves = np.vstack(curves)

# MINOR CURVES
for i in range(curves.shape[0]):
    if i == curves.shape[0] - 1:
        ax.fill_between(xs, curves[i], y_max, alpha=0.2, color=colors[i])
    else:
        ax.fill_between(xs, curves[i], curves[i + 1], alpha=0.2, color=colors[i])

# PPG MARKERS
for value in range(20, 40):
    curve = value / xs
    ax.plot(xs, curve, '-', color='grey', linewidth=0.25)


def min_without_zero(l):
    return np.min(l[l > 0])

texts = []

# NAME TEXT
size = 6
for i in range(0, df.shape[0]):
    ppg = df.myPPG.iloc[i]
    if df.PPP.iloc[i] > 1.3:
        size = 6
    elif df.PPP.iloc[i] < 0.93:
        size = 6
    elif ppg <= 10:
        size = 4
    elif ppg <= 15:
        size = 4
    elif ppg <= 20:
        size = 5
    else:
        size = 6

    texts.append(ax.text(df[x].iloc[i], df[y].iloc[i],
                         df['Name Abbrev Year'].iloc[i], horizontalalignment='left',
                         size=size, color='black', weight='semibold'))

adjust_text(texts,
            arrowprops=dict(arrowstyle="-", color='k', lw=0.5), )

ax.text(x=18, y=1.65, s="The Best NBA Scoring Seasons since 2001",
        fontsize=28, weight='bold', alpha=.85)

ax.text(x=18, y=1.6,
        s='Average points scored per shot attempt (shot attempts = field goal attempts + possessions leading to FTs)',
        fontsize=14, alpha=.75)


fig.tight_layout()

plt.savefig("scorers.png")
plt.show()





