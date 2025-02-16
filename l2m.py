import pandas as pd

df = pd.read_csv("L2M.csv")

def code_incorrect(s):
    if pd.isnull(s):
        return False
    else:
        return s[0] == 'I'

df['incorrect'] = df.decision.apply(code_incorrect)
df['home_disadvantaged'] = df.disadvantaged_team == df.home

current = df[(df.season == 2022) & (df.incorrect)][['time', 'call_type', 'committing', 'disadvantaged', 'decision', 'away_team', 'home_team', 'call', 'type',
                                        'ref_1', 'ref_2', 'ref_3', 'committing_team',
                                        'disadvantaged_team', 'home_disadvantaged']]

home_counts = df[['date', 'home_team', 'away_team']].drop_duplicates().home_team.value_counts().reset_index()
away_counts = df[['date', 'home_team', 'away_team']].drop_duplicates().away_team.value_counts().reset_index()
total_counts = home_counts.merge(away_counts, how='outer', on='index')

total_counts['total'] = total_counts.home_team + total_counts.away_team

total_counts = total_counts.merge(current.disadvantaged_team.value_counts().reset_index(), how='outer', on='index')

total_counts['screw_rate'] = total_counts.disadvantaged_team / total_counts.total

ref_counts1 = current.ref_1.value_counts().reset_index()
ref_counts2 = current.ref_2.value_counts().reset_index()
ref_counts3 = current.ref_3.value_counts().reset_index()


ref_counts = ref_counts1.merge(ref_counts2, how='outer', on='index')
ref_counts = ref_counts.merge(ref_counts3, how='outer', on='index')

ref_counts.fillna(value=0, inplace=True)
ref_counts['total_wrong'] = ref_counts.ref_1 + ref_counts.ref_2 + ref_counts.ref_3

ref_df = df[['date', 'home_team', 'away_team', 'ref_1', 'ref_2', 'ref_3']].drop_duplicates()

ref_counts1 = ref_df.ref_1.value_counts().reset_index()
ref_counts2 = ref_df.ref_2.value_counts().reset_index()
ref_counts3 = ref_df.ref_3.value_counts().reset_index()

ref_counts_total = ref_counts1.merge(ref_counts2, how='outer', on='index')
ref_counts_total = ref_counts_total.merge(ref_counts3, how='outer', on='index')

ref_counts_total.fillna(value=0, inplace=True)
ref_counts_total['total_games'] = ref_counts_total.ref_1 + ref_counts_total.ref_2 + ref_counts_total.ref_3

ref_counts = ref_counts.merge(ref_counts_total, how='outer', on='index')

ref_stats = ref_counts[['index', 'total_wrong', 'total_games']]
ref_stats.fillna(value=0, inplace=True)
ref_stats['wrong_rate'] = ref_stats.total_wrong / ref_stats.total_games