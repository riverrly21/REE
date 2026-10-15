import matplotlib.pyplot as plt
import pandas as pd
df_aus = pd.read_csv(
    'rare-earths-production-australia-2026-10-05.csv', skiprows=6
)
df_chn = pd.read_csv('rare-earths-production-china-2026-10-05.csv', skiprows=6)
df_usa = pd.read_csv(
    'rare-earths-production-united-states-of-america-2026-10-05.csv', skiprows=6
)
df_aus = df_aus[['Year', 'Production (t)']].rename(
    columns={'Production (t)': 'Australia'}
)
df_chn = df_chn[['Year', 'Production (t)']].rename(
    columns={'Production (t)': 'China'}
)
df_usa = df_usa[['Year', 'Production (t)']].rename(
    columns={'Production (t)': 'USA'}
)
# Merge the three dataframes on the 'Year' column
df = (
    df_chn.merge(df_usa, on='Year', how='outer')
    .merge(df_aus, on='Year', how='outer')
)
df = df.sort_values('Year').fillna(0)

df['Annual_Total'] = df['China'] + df['USA'] + df['Australia']

df['China_Cum'] = df['China'].cumsum()
df['USA_Cum'] = df['USA'].cumsum()
df['Australia_Cum'] = df['Australia'].cumsum()
df['Total_Cum'] = df['Annual_Total'].cumsum()

print('\n' + '=' * 65)
print('--- SUMMARY: CUMULATIVE REE EXTRACTION (1994 - 2025) ---')
print('=' * 65)

total_all_time = df['Total_Cum'].iloc[-1]
china_share_cum = (df['China_Cum'].iloc[-1] / total_all_time) * 100
usa_share_cum = (df['USA_Cum'].iloc[-1] / total_all_time) * 100
aus_share_cum = (df['Australia_Cum'].iloc[-1] / total_all_time) * 100

pre_2016_total = df[df['Year'] < 2016]['Annual_Total'].sum()
post_2016_total = df[df['Year'] >= 2016]['Annual_Total'].sum()

print(f'Total Cumulative Extracted (1994-2025): {total_all_time:,.0f} Metric Tons')
print(
    f'China All-Time Share: {china_share_cum:.1f}%'
    f' ({df["China_Cum"].iloc[-1]:,.0f} MT)'
)
print(
    f'USA All-Time Share:   {usa_share_cum:.1f}%'
    f' ({df["USA_Cum"].iloc[-1]:,.0f} MT)'
)
print(
    f'Aus All-Time Share:   {aus_share_cum:.1f}%'
    f' ({df["Australia_Cum"].iloc[-1]:,.0f} MT)'
)
print('-' * 65)
print(
    f'Extracted in Pre-Transition Era (1994-2015):  {pre_2016_total:,.0f} MT'
    f' ({(pre_2016_total/total_all_time)*100:.1f}%)'
)
print(
    f'Extracted in Energy Transition Era (2016-2025): {post_2016_total:,.0f} MT'
    f' ({(post_2016_total/total_all_time)*100:.1f}%)'
)
print('=' * 65 + '\n')

print('Recent 5 Years Cumulative Progress:')
print(
    df[
        [
            'Year',
            'Annual_Total',
            'China_Cum',
            'USA_Cum',
            'Australia_Cum',
            'Total_Cum',
        ]
    ]
    .tail(5)
    .to_string(index=False)
)

#Stacked Area Chart
plt.figure(figsize=(10, 6))

plt.stackplot(
    df['Year'],
    df['China_Cum'],
    df['USA_Cum'],
    df['Australia_Cum'],
    labels=['China', 'USA', 'Australia'],
    colors=['#ff7f0e', '#2ca02c', '#1f77b4'],
    alpha=0.85,
)

plt.axvline(
    x=2015,
    color='black',
    linestyle='--',
    linewidth=1.5,
    label='Energy Transition Acceleration (2015+)',
)

plt.title('Cumulative REE Extraction (1994-2025): Energy Transition Surge')
plt.xlabel('Year')
plt.ylabel('Cumulative Production (Metric Tons)')
plt.legend(loc='upper left')
plt.grid(True, linestyle=':', alpha=0.5)

plt.savefig('ree_cumulative_extraction.png')
plt.show()