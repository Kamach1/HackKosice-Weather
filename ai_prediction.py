# 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
from openai import OpenAI
import pandas as pd
import keyboard

client = OpenAI()
OPENAI_API_KEY = "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"


def get_response(input_text, role="system", ):
    model_response = ""
    text = input_text

    # stream = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[{"role": role, "content": text}],
    #     # stream=True,
    #     stream=False,
    # )

    # for chunk in stream:
    #     if chunk.choices[0].delta.content is not None:
    #         generated_content = chunk.choices[0].delta.content
    #         print(generated_content, end="")
    #         # store model response chunks
    #         model_response += generated_content
    #
    #         # stop generating text when spacebar pressed
    #         if keyboard.is_pressed('s'):
    #             break

    model_response = ""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": role, "content": input_text},
        ],
        temperature=0,
    )

    return response.choices[0].message.content  # Return the model's response


def prepare_dataframe(df):
    # Convert the 'valid' column to datetime format
    df['valid'] = pd.to_datetime(df['valid'])

    df = df.drop(df.index[1::2])
    df = df.drop(df.index[1::2])
    df = df.drop(df.index[1::2])
    df = df.drop(df.index[1::2])
    df = df.drop(df.index[1::2])
    df.reset_index(drop=True, inplace=True)
    df = df.drop(columns=df.columns[0])

    # drop nulls
    df = drop_nulls(df)

    return df


def drop_nulls(df):
    # Check if any column has all null values
    columns_to_drop = []
    for column in df.columns:
        if df[column].isnull().all():
            columns_to_drop.append(column)

    # Drop columns with all null values
    if columns_to_drop:
        df.drop(columns=columns_to_drop, inplace=True)

    return df


def filter_in_range(df, start_date, end_date):
    # Filter the DataFrame based on the date range
    filtered_df = df[(df['valid'] >= start_date) & (df['valid'] < end_date)]

    return filtered_df


def predict(start_date, end_date, input_query):
    # Load the CSV file into a pandas DataFrame
    # df = pd.read_csv('LZIB.csv')
    # df = prepare_dataframe(df)
    # df.to_csv('output.csv', index=False)

    wind_speed_threshold = 25  # mph
    # precipitation_threshold = 0.1  # inches
    cloud_coverage_overcast = "OVC"  # percentage

    df = pd.read_csv('output.csv')
    empty_str = '-'
    df.fillna(empty_str, inplace=True)

    disaster_type = ["flood", "wildfire", "hurricane"]

    # start_date = '2021-01-01'
    # end_date = '2021-01-10'
    # start_date = input("input start date: ")
    # end_date = input("input end date: ")

    data_in_range = (filter_in_range(df, start_date, end_date)).to_string()

    # Clear(CLR), Few(FEW), Scattered(SCT),
    # Broken(BKN), or Overcast(OVC)

    # query = "Here are some weather data, create a prediction based on this data if its possible for" \
    #         + disaster_type[0] + "to happen. Answer strictly is it possible and why" + data_in_range

    # query = "here r some weather data, create a prediction for possible disaster" + data_in_range
    query = (input_query + " based on this data" + data_in_range +
             "answer strictly what i asked for and be short")
    response = get_response(query)
    print("hi")
    print(response)

    # Open a file in write mode
    with open("ai_response.pdf", "w") as f:
        f.write(response)


# example of usage
# predict('2021-07-01', '2021-07-10', "is it possible that hurricane occure the next day?")
# output:
# The temperature for the next day is predicted to be around 24°C based on the pattern in the data."
