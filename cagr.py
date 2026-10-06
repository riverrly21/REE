import pandas as pd

### READ CSV FILES ###
import pandas as pd

australia = pd.read_csv('rare-earths-production-australia-2026-10-05.csv', skiprows=6)
china = pd.read_csv('rare-earths-production-china-2026-10-05.csv', skiprows=6)
america = pd.read_csv('rare-earths-production-united-states-of-america-2026-10-05.csv', skiprows=6)

print(australia.head())
print(china.head())
print(america.head())

### DATA MERGE ###
df = pd.merge(
    australia, china, on='Year', how='outer', suffixes=('_Australia', '_China')
)
    #first we merge australia and china 

df = pd.merge(df, america, on='Year', how='outer')

    #then we merge the result with america

df.rename(
    columns={
        'Production (t)_Australia': 'Australia',
        'Production (t)_China': 'China',
        'Production (t)': 'USA',
    },
    inplace=True,
)

df = df.sort_values('Year').reset_index(drop=True)
print(df.head())

### CAGR CALCULATION ###
def calculate_cagr(start_value, end_value, periods):
    if start_value <= 0 or end_value <= 0 or periods <= 0:
        raise ValueError("Start value, end value, and periods must be greater than zero.")
    return ((end_value / start_value) ** (1 / periods) - 1) * 100

# Analyze period: 2015 - 2025 (10 Year)
start_year = 2015
end_year = 2025
period = end_year - start_year

# 2015 and 2025 production values from the table
aus_2015 = df.loc[df['Year'] == start_year, 'Australia'].values[0]
aus_2025 = df.loc[df['Year'] == end_year, 'Australia'].values[0]

chn_2015 = df.loc[df['Year'] == start_year, 'China'].values[0]
chn_2025 = df.loc[df['Year'] == end_year, 'China'].values[0]

usa_2015 = df.loc[df['Year'] == start_year, 'USA'].values[0]
usa_2025 = df.loc[df['Year'] == end_year, 'USA'].values[0]

# CAGR calculations
cagr_aus = calculate_cagr(aus_2015, aus_2025, period)
cagr_chn = calculate_cagr(chn_2015, chn_2025, period)
cagr_usa = calculate_cagr(usa_2015, usa_2025, period)

print(f'\n--- {start_year}-{end_year} CAGR Growth Rates ---')
print(f'USA CAGR        : {cagr_usa:.2f}%')
print(f'China CAGR        : {cagr_chn:.2f}%')
print(f'Australia CAGR : {cagr_aus:.2f}%')

### VISUALIZATION ###
import matplotlib.pyplot as plt
plt.plot(df['Year'], df['Australia'], label='Australia', marker='o')
plt.plot(df['Year'], df['China'], label='China', marker='o')
plt.plot(df['Year'], df['USA'], label='USA', marker='o')
plt.title('Rare Earths Production (1994-2025)')
plt.xlabel('Year')
plt.ylabel('Production (Metric Tons)')
plt.legend()
plt.savefig('rare_earths_production.png') #it saves the figure as PNG file
plt.show() # it displays the figure in a new window
