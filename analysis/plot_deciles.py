import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import argparse

parser = argparse.ArgumentParser(description='provide the id of the measure to be plotted')
parser.add_argument('measure_id')
args=parser.parse_args()
measure_id = args.measure_id

df = pd.read_csv(f'output/measures/measure_{measure_id}.csv.gz')

df.date= pd.to_datetime(df.date)
df.rename(columns={'value':f'{measure_id}'},inplace=True)

# ## Ensure count columns are actually integers, and cast as such
# nonint_count = len(df[df[f].broad_spectrum_antibiotics_prescriptions-np.abs(df.broad_spectrum_antibiotics_prescriptions) > 0])
# if (nonint_count >0):
#     raise ValueError(f'non-integer values for counts of broad_spectrum_antibiotics_prescriptions: {nonint_count} rows affected')

# nonint_count = len(df[df.antibacterial_prescriptions-np.abs(df.antibacterial_prescriptions) > 0])
# if (nonint_count >0):
#     raise ValueError(f'non-integer values for counts of antibacterial_prescriptions: {nonint_count} rows affected')

# df.broad_spectrum_antibiotics_prescriptions = df.broad_spectrum_antibiotics_prescriptions.astype(np.int32)
# df.antibacterial_prescriptions = df.antibacterial_prescriptions.astype(np.int32)

## replace dummy data with values in expected range
#df.broad_spectrum_proportion = np.percentile(df['broad_spectrum_proportion'].values,(10*np.arange(0,11)))

deciles = df.groupby('date')[f'{measure_id}']\
            .quantile(np.arange(0.1,1,0.1))\
            .reset_index()\
            .rename(columns={'level_1':'decile'})\
            .set_index('date')\
            .pivot(columns='decile',values=f'{measure_id}')\
            .rename(columns=lambda c: round(c,1))


plt.rcParams['figure.figsize']=(15,10)
dfmt =mdates.DateFormatter("%b %Y")
for decile in deciles.columns:
    ls = '-' if decile==0.5 else '--'
    plt.plot(deciles[decile].index,deciles[decile].values,c='b',linestyle=ls)

plt.ylabel(f'{measure_id}')
plt.xlabel('Month')
plt.xticks(rotation=90)


if not os.path.exists('output/figures'):
    os.makedirs('output/figures')

plt.savefig(f'output/figures/{measure_id}_decile_chart.png')