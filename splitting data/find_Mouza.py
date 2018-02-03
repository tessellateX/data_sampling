import numpy as np
import pandas as pd
import googlemaps
import json

def read_File():
    df=pd.read_csv("split_data/split_mouzas0.csv") # change the file name to get output for various splits
    df=df['name']
    return df

def find_Pos(mouzas):
    from mpl_toolkits.basemap import Basemap
    found=[]
    badLuck=[]
    geo_json={}
    positions=pd.DataFrame(columns=['lat','lon'],index=mouzas)
    gmaps = googlemaps.Client(key='AIzaSyBLyHeiYIxFNG2eGBqzZ-IwgM8xDQ-c3WA')
    for i in mouzas:
        try:
            geocode_result = gmaps.geocode(i+", West Bengal")
            geo_json[i]=geocode_result
            positions.loc[i]['lat'] = geocode_result[0]["geometry"]["location"]["lat"]
            positions.loc[i]['lon'] = geocode_result[0]["geometry"]["location"]["lng"]
            found.append(i)
            print (i+" t") #i at end of mouza name denotes FOUND
        except Exception:
            badLuck.append(i)
            print (i+" e")  #e at end of mouza name denotes FOUND
            continue
    bad=pd.DataFrame(index=badLuck)
    return positions,found,bad,geo_json

geo_j={}
mouzas=read_File()
positions,found,bad,geo_j=find_Pos(mouzas)

print ("\n \n")

print (positions)
print ("\n \n")

print (found)
print (len(found))
print ("\n \n")

print (bad)
print (len(bad))

positions.to_csv('csv/positions0.csv',sep=',',encoding='utf-8')  # change the file name to get output for various splits
bad.to_csv('notFoundMouza/notFound0.csv',sep=',',encoding='utf-8') # change the file name to get output for various splits
with open('json/positions0.txt', 'w') as outfile:  # change the file name to get output for various splits
    json.dump(geo_j, outfile)

