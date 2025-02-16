import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text

# LOAD DATA

scoring = pd.read_csv("scoring_ts_11_4_22.csv")

min_games_percent = 0.2
x_min = -1
x_max = 36
y_min = 30
y_max = 90

total = scoring

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

total_games = np.max(total['GamesPlayed'])
min_games = total_games * min_games_percent

df = total[(total['GamesPlayed'] > min_games) | (total.Name == 'LeBron James') | (total.Name == 'Joel Embiid')
    | (total.Name == 'Pascal Siakam') | (total.Name == 'Luka Doncic') | (total.Name == 'Jerami Grant')
    | (total.Name == 'Jimmy Butler') | (total.Name == 'Bam Adebayo') | (total.Name == 'Kevin Durant') | (total.Name == 'Devin Booker')]
df = df[df['TsPct'] < 1]
df['PPG'] = df.Points.divide(df.GamesPlayed)
df['TS%'] = df['TsPct'].apply(lambda x: round(x * 100, 1))

# PLOTTING

x = 'PPG'
y = 'TS%'

plt.style.use('fivethirtyeight')
# matplotlib.rcParams['font.family'] = "roboto"

fig, ax = plt.subplots(figsize=(13,8))
sns.scatterplot(data=df, x=x, y=y, s=3, ax=ax, color='black')
# graph = df.plot.scatter(x = x, y = y, s=3, ax=ax)
ax.set_xlabel("Volume: PPG")
ax.set_ylabel("Efficiency: TS%")
# ax.set_xticks(range(2, 14, 1))
# ax.set_title("Scoring: Efficiency vs Volume")

ax.set_xlim(left = x_min, right = x_max)
ax.set_ylim(bottom = y_min, top = y_max)

xs = np.arange(0.01, x_max, 0.01)

# AVERAGE LINE
y_avg = np.mean(df[y])
ax.axhline(y=y_avg, xmin = x_min, xmax = x_max, color = 'black', ls='--', lw=0.8, alpha=0.6)
ax.text(x_max + 0.1, y_avg + 0.005, f'Average TS%:\n {np.round(y_avg, 1)}', horizontalalignment = 'left', size = 6, weight='semibold')

x_avg = np.mean(df[x])
ax.axvline(x=x_avg, ymin = 0, ymax = y_max, color = 'black', ls='--', lw=0.8, alpha=0.6)
ax.text(x_avg + 0.005, y_max, f'Average PPG Per Game: {np.round(x_avg, 1)}', horizontalalignment = 'center', size = 6, weight='semibold')



def min_without_zero(l):
    return np.min(l[l > 0])


# NAME TEXT

texts = []
size = 6
for i in range(0,df.shape[0]):
    ppg = df[y].iloc[i]
    if df[y].iloc[i] > 1.3:
        size = 6
    elif df[y].iloc[i] < 0.93:
        size = 6
    elif ppg <= 10:
        size = 4
    elif ppg <= 15:
        size = 4
    elif ppg <= 20:
        size = 5
    else:
        size = 6
    #
    # if df['TeamAbbreviation'].iloc[i] == 'GSW':
    #     color = 'tab:olive'
    # elif df['TeamAbbreviation'].iloc[i] == 'BOS':
    #     color = 'tab:green'
    # else:
    color = 'black'

    texts.append(ax.text(df[x].iloc[i], df[y].iloc[i],
         df['Name Abbrev'].iloc[i], horizontalalignment='left',
         size=size, color=color, weight='semibold'))

adjust_text(texts,
            arrowprops=dict(arrowstyle="-", color='k', lw=0.5),)



ax.text(x = -2.5, y = y_max + 2, s = "The Best NBA Scorers",
               fontsize = 28, weight = 'bold', alpha = .85)


# fig.tight_layout()

plt.savefig("scorers.png")
plt.show()





