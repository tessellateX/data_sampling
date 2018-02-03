import pandas as pd

df = pd.read_csv('../tables/csv/mouzas.csv')
df = df[['id', 'name', 'jl_number', 'block_id']]
for i in range(0,21):
    path="split_data/split_mouzas"+str(i)+".csv" # path to split file
    df.iloc[2000*i:2000*(i+1)].to_csv(path,sep=',',encoding='utf-8', index=False)
    print("\rSplit {} completed".format(i))

print("Splitting done")
