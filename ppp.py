import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text

# LOAD DATA

scoring = pd.read_csv("scoring_2_19.csv")
fouls = pd.read_csv("fouls_2_19.csv")

total = pd.merge(scoring, fouls, how='inner', on='Name')
total['Shots'] = total['FG2A'] + total['FG3A'] + (total['TwoPtShootingFoulsDrawn'] + total['ThreePtShootingFoulsDrawn'] + total['NonShootingFoulsDrawn'] - total['2pt And 1 Free Throw Trips'] - total['3pt And 1 Free Throw Trips'])
total['PPP'] = total ['Points'] / total['Shots']
total['Shots Per Game'] = total['Shots'] / total['GamesPlayed_x']
total['myPPG'] = total['PPP'] * total['Shots Per Game']
total['True Fouls'] = total['Shots'] - total['FG2A'] - total['FG3A']
total['Est Fouls'] = total['FTA'] * 0.44

total['Last Name'] = total['Name'].apply(lambda s: s.split(' ')[1])
counts = total['Last Name'].value_counts()
last_name_copies = list(counts[counts>1].keys())

total['Standard Abbrev Name'] = total['Name'].apply(lambda s: s.split(' ')[0][0] + ". " + s.split(' ')[1])
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

total['Name Abbrev'] = total['Name'].apply(get_abbrev)

total_games = np.max(total['GamesPlayed_x'])
min_games = total_games * 0.6

df = total[(total['GamesPlayed_x'] > min_games) | (total.Name == 'LeBron James') | (total.Name == 'Joel Embiid')
    | (total.Name == 'Pascal Siakam') | (total.Name == 'Luka Doncic') | (total.Name == 'Jerami Grant')
    | (total.Name == 'Jimmy Butler') | (total.Name == 'Bam Adebayo') | (total.Name == 'Kevin Durant')]

# PLOTTING

x = 'Shots Per Game'
y = 'PPP'

plt.style.use('fivethirtyeight')
# matplotlib.rcParams['font.family'] = "roboto"

fig, ax = plt.subplots(figsize=(13,8))
sns.scatterplot(data=df, x=x, y=y, s=3, ax=ax)
# graph = df.plot.scatter(x = x, y = y, s=3, ax=ax)
ax.set_xlabel("Volume: Shot attempts per game")
ax.set_ylabel("Efficiency: Points per shot")
# ax.set_xticks(range(2, 14, 1))
# ax.set_title("Scoring: Efficiency vs Volume")
x_min = -1
x_max = 31
y_min = 0.65
y_max = 1.55
ax.set_xlim(left = x_min, right = x_max)
ax.set_ylim(bottom = y_min, top = y_max)

xs = np.arange(0.01, x_max, 0.01)
curve_values = [0, 10, 15, 20, 25, 30]

colors = ['grey', '#008fd5', '#fc4f30', '#e5ae38', '#6d904f',  '#810f7c', '#8b8b8b',]

curves = []

# MAJOR CURVES
for i, value in enumerate(curve_values):
    curve = value / xs
    ax.plot(xs, curve, '-', color = colors[i], linewidth=0.5)
    if value != 0:
        ax.text(value / (y_max - 0.025), y_max - 0.025, f'{value} PPG',horizontalalignment='left', verticalalignment='bottom',
         size=7, color=colors[i], weight='semibold')
    curves.append(curve)

curves = np.vstack(curves)

# MINOR CURVES
for i in range(curves.shape[0]):
    if i == curves.shape[0] - 1:
        ax.fill_between(xs, curves[i], y_max, alpha=0.2, color = colors[i])
    else:
        ax.fill_between(xs, curves[i], curves[i+1], alpha=0.2, color = colors[i])

# PPG MARKERS
for value in range(0, 40):
    curve = value / xs
    ax.plot(xs, curve, '-', color = 'grey', linewidth=0.25)

# AVERAGE LINE
ppp_avg = np.mean(df['PPP'])
ax.axhline(y=ppp_avg, xmin = x_min, xmax = x_max, color = 'black', ls='--', lw=0.8, alpha=0.6)
ax.text(x_min + 0.1, ppp_avg + 0.005, f'Average PPS: {np.round(ppp_avg, 2)}', horizontalalignment = 'left', size = 6, weight='semibold')

shots_avg = np.mean(df['Shots Per Game'])
ax.axvline(x=shots_avg, ymin = 0, ymax = y_max, color = 'black', ls='--', lw=0.8, alpha=0.6)
ax.text(shots_avg + 0.005, y_max, f'Average Shots Per Game: {np.round(shots_avg, 1)}', horizontalalignment = 'center', size = 6, weight='semibold')



def min_without_zero(l):
    return np.min(l[l > 0])




# NAME TEXT

texts = []
size = 6
for i in range(0,df.shape[0]):
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

    if 'Embiid' in df.Name.iloc[i] or 'Giannis' in df.Name.iloc[i]:
        texts.append(ax.text(df[x].iloc[i], df[y].iloc[i],
         df['Name Abbrev'].iloc[i] + f" ({round(df.myPPG.iloc[i], 2)} PPG)", horizontalalignment='left',
         size=size, color='black', weight='semibold'))
    else:
        texts.append(ax.text(df[x].iloc[i], df[y].iloc[i],
         df['Name Abbrev'].iloc[i], horizontalalignment='left',
         size=size, color='black', weight='semibold'))

adjust_text(texts,
            arrowprops=dict(arrowstyle="-", color='k', lw=0.5),)



ax.text(x = -2.5, y = 1.65, s = "The Best NBA Scorers",
               fontsize = 28, weight = 'bold', alpha = .85)

ax.text(x = -2.5, y = 1.6,
               s = 'Average points scored per shot attempt (shot attempts = field goal attempts + possessions leading to FTs)',
              fontsize = 14, alpha = .75)

# CATEGORIES 
category_size = 14
y_margin = 0.05
x_margin = 0.5
alpha = 0.3
ax.text(x = x_margin, y = y_max - y_margin, s = "Efficient Role-Players", horizontalalignment = 'left', verticalalignment = 'center',
               fontsize = category_size, alpha = alpha)

ax.text(x = x_max - x_margin, y = y_max - y_margin, s = "Offensive Stars",horizontalalignment = 'right',verticalalignment = 'center',
               fontsize = category_size, alpha = alpha)

ax.text(x = x_margin, y = y_min + y_margin, s = "Offensive Scrubs", horizontalalignment = 'left',verticalalignment = 'center',
               fontsize = category_size, alpha = alpha)

ax.text(x = x_max - x_margin, y = y_min + y_margin, s = "Chuckers", horizontalalignment = 'right',verticalalignment = 'center',
               fontsize = category_size, alpha = alpha)

y_avg = 0.5 * (y_min + y_max)


fig.tight_layout()

plt.savefig("scorers.png")
plt.show()





