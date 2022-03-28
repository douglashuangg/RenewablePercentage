# from functools import total_ordering
import requests # allows access web resources
# from bs4 import BeautifulSoup # allows parse the web information
from datetime import date, timedelta
import database
import tweepy
import os

# tweeting
auth = tweepy.OAuth1UserHandler(
   os.environ.get('consumer_key'), os.environ.get('consumer_secret'), os.environ.get('access_token'), os.environ.get('access_token_secret')
)

api = tweepy.API(auth)

# database connection
connection = database.connect()
database.create_tables(connection)

# gets the new date whenever this runs everyday
yesterday = date.today() - timedelta(1)
yearAgo = date.today() - timedelta(366)
yesterday = yesterday.strftime("%m%d%Y")
yearAgo = yearAgo.strftime("%m%d%Y")

# I can just change the date here manually. And then set interval to scrape data.
URL = f'https://www.eia.gov/electricity/930-api/region_data_by_fuel_type/series_data?type[0]=NG&respondent[0]=US48&start={yearAgo}%2000:00:00&end={yesterday}%2023:59:59&frequency=daily&timezone=Eastern&series=undefined'

result = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'})

data = result.json()
refined = {}

# gets the fuel, date, and data
for i in range(len(data[0]["data"])):
    # print(data[0]["data"][i]['FUEL_TYPE_NAME'])
    fuelType = data[0]["data"][i]['FUEL_TYPE_NAME']
    dates = data[0]["data"][i]['VALUES']['DATES']
    values = data[0]["data"][i]['VALUES']['DATA']
    
    refined[fuelType] = {'DATES': dates, 'DATA': values }

# variables
dayTotal = 0
dayRenewable = 0
pDayTotal = 0
pDayRenewable = 0

# adds renewables and totals together from today and 1 year ago today
for fuel in refined:
    dayTotal += refined[fuel]['DATA'][-1]
    pDayTotal += refined[fuel]['DATA'][0]
    if(fuel == 'Wind' or fuel == 'Hydro' or fuel == 'Solar'):
        dayRenewable += refined[fuel]['DATA'][-1]
        pDayRenewable += refined[fuel]['DATA'][0]

# not sure what this is for
recent = refined["Coal"]["DATES"][-1]
oldest = refined["Coal"]["DATES"][0]
oldDate = open('yesterday.txt', 'r').read()
newDate = (date.today() - timedelta(1)).strftime("%m/%d/%Y")

if(newDate != oldDate):
    database.add_value(connection, recent, dayTotal, dayRenewable, pDayTotal, pDayRenewable)
# database.delete_by_id(connection, 3, 4)
def percent(num, den):
    return ('{:0.2f}%').format((num/den)*100)

testing = database.get_all(connection)
# for test in testing:
#     print(test)
dTotal = testing[-1][2]
dRenewable = testing[-1][3]
dPercent = percent(dRenewable, dTotal)

# tweets value
api.update_status(dPercent+" of electricity generated in the U.S. was renewable on {:%B %d, %Y}".format(date.today() - timedelta(1))+'.')

with open('yesterday.txt', 'w') as f:
    f.write(recent)

# get date index, to get data with same index, then add that together for total fuel generated that day.
# actually just get last index and add it to memory.

# soup = BeautifulSoup(result.content, "html.parser")
#df_list = pd.read_html(URL)

# df = pd.DataFrame(df_list[0])
# df.head()

# print(result.status_code)

# result = requests.get('https://www.eia.gov/electricity/gridmonitor/dashboard/custom/pending')
# src = result.content
# soup = BeautifulSoup(src, 'html.parser')

# gases = []
# svgs = soup.find_all("svg")
# for svg in svgs:
#     gases.append(svg.find('path'))

# print(gases)