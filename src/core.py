import pandas as pd

df = pd.read_csv('../input/AppleStore.csv')

outDf = df[df['rating_count_tot'] == 354058]

gp = df.groupby("prime_genre")
for i, d in gp['rating_count_tot']:
    if (i == "Music"):
        count = 0
        for c in d:
            print(c)
            count = count+1
            if count == 10:
                break