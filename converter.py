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
for col in ['air_temperature', 'dew_point', 'relative_humidity', 'wind_direction', 'wind_speed', 'sea_level_pressure']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Simplified risk estimation
def estimate_risks(row):
    floods_risk = hurricanes_risk = wildfires_risk = 0

    if pd.notnull(row['relative_humidity']) and row['relative_humidity'] > 90:
        floods_risk = 70
    elif pd.notnull(row['relative_humidity']) and row['relative_humidity'] > 80:
        floods_risk = 50
    elif pd.notnull(row['relative_humidity']) and row['relative_humidity'] > 70:
        floods_risk = 30

    if pd.notnull(row['wind_speed']) and row['wind_speed'] > 20 and pd.notnull(row['sea_level_pressure']) and row['sea_level_pressure'] < 1000:
        hurricanes_risk = 60
    elif pd.notnull(row['wind_speed']) and row['wind_speed'] > 15:
        hurricanes_risk = 40

    if pd.notnull(row['air_temperature']) and row['air_temperature'] > 0 and pd.notnull(row['relative_humidity']) and row['relative_humidity'] < 30:
        wildfires_risk = 80
    elif pd.notnull(row['relative_humidity']) and row['relative_humidity'] < 50:
        wildfires_risk = 60

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

print(js_object)

# Save the JavaScript object to a file named data.js
with open("bratislava.js", "w") as file:
    file.write(js_object)

