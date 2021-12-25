import os
import pandas as pd
from add_indicators import add_indicators

files = os.listdir('Data/bars1/')

number_files = 100
df = pd.DataFrame()
for f in files[-number_files:]:
    temp = pd.read_csv(f'Data/bars1/{f}')
    temp.drop(['time', 'wap'], axis=1, inplace=True)
    add_indicators(temp)
    temp.dropna(inplace=True)
    df = df.append(temp, ignore_index=True)

print('result shape', df.shape)
df.to_csv('Data/1mindata.csv', index=False)

print('DONE')