import random

import pandas as pd
from io import StringIO

csv_path = 'output.csv'

df_csv = pd.read_csv(csv_path)

data = ''  # Start of the string

data += ' '.join(df_csv.columns) + '\n'

for index, row in df_csv.iterrows():
    data += ' '.join(row.dropna().astype(str).tolist()) + '\n'

df = pd.read_csv(StringIO(data), sep='\s+')

# Convert 'valid' to datetime and ensure numerical fields are processed correctly
df['valid'] = pd.to_datetime(df['valid'])
for col in ['air_temperature', 'dew_point', 'relative_humidity', 'wind_direction', 'wind_speed', 'sea_level_pressure', 'one_hour_precipitation']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Simplified risk estimation
def estimate_risks(row):
    floods_risk = hurricanes_risk = wildfires_risk = 0

    # print(row['air_temperature'])     |
    # print(row['dew_point'])           |^
    # print(row['relative_humidity'])   |^
    # print(row['wind_direction'])      |^

    if pd.notnull(row['wind_direction']) and 90 < row['wind_direction'] < 100:
        floods_risk = random.randint(40,50)
    elif pd.notnull(row['wind_direction']) and 70 < row['wind_direction'] < 90:
        floods_risk = random.randint(30, 40)
    elif pd.notnull(row['wind_direction']) and 50 < row['wind_direction'] < 70:
        floods_risk = random.randint(20,30)

    if pd.notnull(row['wind_speed']) and row['wind_speed'] > 20 and pd.notnull(row['one_hour_precipitation']) and row['one_hour_precipitation'] < 1000:
        hurricanes_risk = random.randint(20, 40)
    elif pd.notnull(row['wind_speed']) and row['wind_speed'] > 15:
        hurricanes_risk = random.randint(0, 20)

    # for col in ['air_temperature', 'dew_point', 'relative_humidity', 'wind_direction', 'wind_speed', 'sea_level_pressure', 'one_hour_precipitation']:
    # print(row['air_temperature'])    #|
    print(row['dew_point'])            #|^
    # print(row['relative_humidity'])  #|^
    print(row['wind_direction'])       #|^

    if pd.notnull(row['dew_point']) and row['dew_point'] > 30 and pd.notnull(row['wind_direction']) and 10 < row['wind_direction'] < 30:
        wildfires_risk = random.randint(50, 70)
    elif pd.notnull(row['dew_point']) and row['dew_point'] > 25 and pd.notnull(row['wind_direction']) and 30 < row['wind_direction'] < 50:
        wildfires_risk = random.randint(20, 50)
    elif pd.notnull(row['dew_point']) and row['dew_point'] > 20 and pd.notnull(row['wind_direction']) and 50 < row['wind_direction'] < 70:
        wildfires_risk = random.randint(0, 20)

    return pd.Series([floods_risk, hurricanes_risk, wildfires_risk])

# Apply the function
df[['floods_risk', 'hurricanes_risk', 'wildfires_risk']] = df.apply(estimate_risks, axis=1)

df['valid_date'] = df['valid'].dt.date
risk_levels = df.groupby('valid_date')[['floods_risk', 'hurricanes_risk', 'wildfires_risk']].mean().round(0).astype(int)

# Convert to a JavaScript object
js_object = "const bratislava = {\n"
for disaster in ['floods', 'hurricanes', 'wildfires']:
    js_object += f"    {disaster}: {{\n"
    for date, risks in risk_levels.iterrows():
        js_object += f"        '{date}': {risks[f'{disaster}_risk']},\n"
    js_object += "    },\n"
js_object += "};\n"
js_object += "export default bratislava;"

# print(js_object)

# Save the JavaScript object to a file named data.js
with open("bratislava.js", "w") as file:
    file.write(js_object)
