# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 19:51:14 2018

@author: ANURAN
"""

import pandas as pd

df=pd.read_csv('mouzas.csv')

for i in range(0,21):
    name="split_data/split_mouzas"+str(i)+".csv" # path to split file
    print("Split "+str(i)+" started...")
    df.iloc[2000*i:2000*(i+1)].to_csv(name,sep=',',encoding='utf-8')
    print("Split "+str(i)+" completed")

i=i+1
name="split_data/split_mouzas"+str(i)+".csv" # path to split file
print("Split "+str(i)+" started...")
df.iloc[2000*i:].to_csv(name,sep=',',encoding='utf-8')
print("Split "+str(i)+" completed")

print("Splitting done")

