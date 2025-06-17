## NOTE: This tmx_top_volume_etl.py file combines tmx_top_volume.py, tmx_top_volume_database.py, and tmx_top_volume_cleaning.py.

## NEED TO RUN THE FILE EVERYDAY TO UPDATE THE DATABASE

# Import necessary libraries
from scrapy.crawler import CrawlerProcess
import datetime as datetime
import os

# Import necessary functions
from spiders.tmx_top_volume import TmxTopVolumeSpider
from tmx_top_volume_cleaning import clean_top_volume
from tmx_top_volume_database import upload_dataframe_to_sql

# Main function that combines the ETL process
def main():

    # Settings that output the data to a JSON file
    settings = {

        'FEEDS': {

            os.path.join(os.getcwd(), "scrapy_tmx_money", "top_volume.json"): {

                'format': 'json',

                'overwrite': True,

            }

        }

    }

    # Run the spider
    process = CrawlerProcess(settings)
    process.crawl(TmxTopVolumeSpider)
    process.start()

    # Load the data
    json_file = os.path.join(os.getcwd(), "scrapy_tmx_money", "top_volume.json")

    # Clean the data
    dataframe = clean_top_volume(json_file)

    # Upload the data to SQL
    upload_dataframe_to_sql(dataframe)

if __name__ == '__main__':

    main()

