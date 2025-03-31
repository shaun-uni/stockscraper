# Web Scraping Stock Indicator Data to create a Stock Screener in a csv

## A python file that uses the Selenium library to webscrape data from a free stock screener online [StockAnalysis.com](https://stockanalysis.com/stocks/screener/)

## Setup:
1. Download ChromeDriver from: https://chromedriver.chromium.org/downloads.
2. Make sure the version matches your Chrome browser.
3. Update the ChromeDriver path in the script; chrome_driver_path = r"C:\your_path_here\chromedriver.exe" to the location of your downloaded ChromeDriver.

## Usage:
The script will:
1. Open StockAnalysis.com screener
2. Select all indicator checkboxes
3. Scrape data from every page of results
4. Save the data into a file named stocks.csv

