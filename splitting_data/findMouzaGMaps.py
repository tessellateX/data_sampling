import numpy as np
import pandas as pd
from geopy.geocoders import GoogleV3
import json, os

def config():
    with open('config.json', 'r') as f:
        params = json.load(f)
    return params

def read_mouza(mouza_path):
    df = pd.read_csv("split_data/split_mouzas{}.csv".format(mouza_path))
    return df

def coor_search_pass1(mouzas, gmaps):
    '''
    We will later go for more passes if this fails
    '''
    # Storing Raw data
    raw = {}

    # Stats
    hit_count = 0

    for idx, mouza in enumerate(mouzas['name']):
        percentage = idx / len(mouzas) * 100
        try:
            result = gmaps.geocode('{}, West Bengal'.format(mouza))
            if result == None:
                raise Exception('Value Not Found')

            raw[mouza] = result.raw
            mouzas.set_value(idx, 'latitude', result.latitude)
            mouzas.set_value(idx, 'longitude', result.longitude)

            hit_count += 1
            print('{0}% \t {1} \t\t {2}'.format(percentage, mouza, result.address))
        except Exception as e:
            raw[mouza] = None
            mouzas.set_value(idx, 'latitude', -1)
            mouzas.set_value(idx, 'longitude', -1)

            print('{0}% \t {1} \t\t {2}'.format(percentage, mouza, e))

    print('Hit percent = {}%'.format(hit_count/len(mouzas)*100.0))
    return mouzas, raw

def save_results(df, raw, path='results/'):
    final_directory = os.path.join(os.getcwd(), path)
    if not os.path.exists(final_directory):
        os.mkdir(final_directory)

    df.to_csv('{}mouzas_coor{}.csv'.format(final_directory, mouza_path), index=False)
    with open('{}mouzas_raw{}.json'.format(final_directory, mouza_path), 'w') as f:
        json.dump(raw, f, indent=4)

    print('Results Saved')

if __name__ == '__main__':
    params = config()
    api_key = params["api_key"]

    mouza_path = int(input("Enter file no : "))
    mouzas = read_mouza(mouza_path)
    # Add cols to mouza
    mouzas['latitude'] = pd.Series(0.0, index=mouzas.index)
    mouzas['longitude'] = pd.Series(0.0, index=mouzas.index)

    gmaps = GoogleV3(api_key=api_key)

    mouzas_locations, mouzas_raw = coor_search_pass1(mouzas=mouzas, gmaps=gmaps)
    save_results(mouzas_locations, mouzas_raw)
