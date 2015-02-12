# Meteofrance scraper
## Description
This is a tool to scrape daily weather data off the official French weather forecaster's [website] (http://www.meteofrance.com), for any city in France and any day after year 2001.
The tool is written in python and makes use of the web scraping framework [Scrapy](http://scrapy.org/).
## Installation
Open a terminal and make sure you have `python` and `git` installed.
If you want to install this project in folder `dir`, type:
```
cd dir
git clone https://github.com/sgskt/meteofrance.git
cd meteofrance
pip install -r requirements.txt
```
## Usage
### Basics
The tool scrapes data for all dates and places specified in an input `csv` file, and outputs the result to another `csv` file.
To run the tool:
```
cd dir/meteofrance
scrapy crawl meteofrance -a input=input_file.csv -a output=output_file.csv
```
Each line of `input_file.csv` should be specified as follows:
```
place_type, place_id, date
```
where:
* `place_type` is one of `VILLE_FRANCE` or `STATION_CLIM`
* `place_id` is the code of the place to scrape data for. If `place_type=VILLE_FRANCE`, then this is the 5-digit INSEE code of the city. If `place_type=STATION_CLIM`, then this is the 8-digit identifier of the weather station (list of all weather stations can be found in the project folder)
* `date` is the date for which to scrape data, in `DD-MM-YYYY` format.

### Advanced
Settings can be tweaked in the `settings.py` file. For example, you can increase the number of concurrent requests made to be able to scrape faster.
If you have access to a proxy server, you can use that too. Just add it in the `middleware.py` file, and uncomment the corresponding setting in the settings file.
Information can be found in the `Scrapy` documentation.
