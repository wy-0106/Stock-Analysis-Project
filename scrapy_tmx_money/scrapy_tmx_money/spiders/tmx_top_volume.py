# Import the necessary libraries
import datetime as datetime
import scrapy

# Spider class
class TmxTopVolumeSpider(scrapy.Spider):

    # Spider name
    name = 'tmx_top_volume'

    # Allowed domains
    allowed_domains = [

        "money.tmx.com"

    ]

    # Start URL
    start_urls = [

        "https://money.tmx.com/stock-list/TOP_VOLUME"

    ]

    # Custom settings
    custom_settings = {

        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

    }

    # Parse function
    def parse(self, response):

        # Loop the table rows
        for each_row in response.css('table tbody tr'):

            # Check if the table data is empty
            if not each_row.css('td'):

                continue

            # If the table data is not empty, then yield the data
            else:

                yield {

                    'Symbol': each_row.css('td:nth-child(3) div div div a span::text').get(),

                    'Company': each_row.css('td:nth-child(4) div div a span::text').get(),

                    'Price': each_row.css('td:nth-child(5) div div span::text').get(),

                    'Percentage_Net_Change': each_row.css('td:nth-child(7) div div span span::text').get(),

                    'Volume': each_row.css('td:nth-child(8) div div span::text').get(),

                    'Average_Volume': each_row.css('td:nth-child(9) div div span::text').get(),

                    'Date': datetime.datetime.today().strftime('%Y-%m-%d')

                }