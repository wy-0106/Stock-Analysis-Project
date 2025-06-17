# Import the necessary libraries
import pandas as pd

### Clean the data
def clean_top_volume(json_file):

    # Load the data
    dataframe = pd.read_json(json_file)

    # Convert the type of Volume and Average Volume to numeric
    dataframe['Volume'] = pd.to_numeric(dataframe['Volume'].str.replace(',', ''), errors='coerce')
    dataframe['Average_Volume'] = pd.to_numeric(dataframe['Average_Volume'].str.replace(',', ''), errors='coerce')
    dataframe['Average_Volume'] = dataframe['Average_Volume'].astype('float64')

    # Convert the type of Date to datetime
    dataframe['Date'] = pd.to_datetime(dataframe['Date']).dt.date

    # Drop rows with null values
    dataframe.dropna(axis=0, how='any', subset=None, inplace=True)

    # Save cleaned data as a CSV file
    dataframe.to_csv('scrapy_tmx_money/cleaned_top_volume.csv', index=False)

    return dataframe