# -*- coding: utf-8 -*-

import pandas as pd
import zipfile

# Define the path to the zipfile
path = '/content/archive.zip'

# Define the bucketing function
def get_aqi_bucket(aqi):
    if aqi > 400:
        return 'Severe'
    elif aqi > 300:
        return 'Very Poor'
    elif aqi > 200:
        return 'Poor'
    elif aqi > 100:
        return 'Moderate'
    elif aqi > 50:
        return 'Satisfactory'
    else:
        return 'Good'

# Read the dataset from the zipfile
with zipfile.ZipFile(path, 'r') as f:
    for name in f.namelist():
        if name == 'city_day.csv':
            df_c = pd.read_csv(f.open(name))  # Reading all columns
import missingno as msno
msno.heatmap(df_c)
# Forward fill followed by backward fill for 'PM2.5' and 'PM10'
df_c['PM2.5'] = df_c['PM2.5'].fillna(method='ffill').fillna(method='bfill')
df_c['PM10'] = df_c['PM10'].fillna(method='ffill').fillna(method='bfill')

df_c['NO'] = df_c['NO'].fillna(method='ffill').fillna(method='bfill')
df_c['NO2'] = df_c['NO2'].fillna(method='ffill').fillna(method='bfill')
df_c['NOx'] = df_c['NOx'].fillna(method='ffill').fillna(method='bfill')
df_c['NH3'] = df_c['NH3'].fillna(method='ffill').fillna(method='bfill')
df_c['CO'] = df_c['CO'].fillna(method='ffill').fillna(method='bfill')
df_c['SO2'] = df_c['SO2'].fillna(method='ffill').fillna(method='bfill')
df_c['O3'] = df_c['O3'].fillna(method='ffill').fillna(method='bfill')
df_c['Benzene'] = df_c['Benzene'].fillna(method='ffill').fillna(method='bfill')
df_c['Toluene'] = df_c['Toluene'].fillna(method='ffill').fillna(method='bfill')
df_c['Xylene'] = df_c['Xylene'].fillna(method='ffill').fillna(method='bfill')

# Now check again for any null values
print(df_c['PM2.5'].isnull().sum(), "null values in PM2.5 after fill")
print(df_c['PM10'].isnull().sum(), "null values in PM10 after fill")


# Backward fill for 'AQI'
df_c['AQI'] = df_c['AQI'].fillna(method='bfill')

# Apply the bucketing function only where 'AQI_Bucket' is NaN
df_c.loc[df_c['AQI_Bucket'].isnull(), 'AQI_Bucket'] = df_c.loc[df_c['AQI_Bucket'].isnull(), 'AQI'].apply(get_aqi_bucket)

df_c.drop(['Xylene'], axis=1, inplace=True)

# Save the updated dataframe with all columns to a new csv file
output_file_path = 'updated_cleaned_city_day.csv'
df_c.to_csv(output_file_path, index=False)

print("Updated dataframe saved to:", output_file_path)