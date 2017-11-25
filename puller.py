import requests, os, pandas as pd
from io import StringIO
from multiprocessing import Pool

DAYS = input('Enter no. of days to pull:') #google doesnt give more than 15 days of data
EXCHANGE = 'NSE'
INTERVAL = '61'  # 61 for 1 minute(60+1) , 601 for 10 minutes(600+1) , 301 for 5 minutes etc(300+1), 
                 # 1 is added to get the timestamp data for parsing
DOWNLOAD_PATH = '/home/LTP/'
count = 0

# given below are some sample stocks symbols from NSE 
# if you want to add your own stocks just add their symbol in the list below

stocks = ['ABB', 'ACC', 'ACCELYA', 'ACE', 'ADANIENT', 'ADANIPORTS', 'ADANIPOWER',
     'ALLCARGO', 'AMARAJABAT', 'AMBUJACEM', 'ANANTRAJ', 'ANDHRABANK', 'APOLLOHOSP', 
     'APOLLOTYRE', 'ARVIND', 'ASAHIINDIA', 'ASHOKLEY', 'ASIANPAINT', 'ASTRAMICRO', 'AXISBANK',
     'BAJAJ-AUTO', 'BAJAJFINSV', 'BAJFINANCE', 'BANKBARODA', 'BANKINDIA',
     'BANKNIFTY', 'BATAINDIA', 'BEL', 'BEML', 'BERGEPAINT', 'BHARATFIN', 'BHARATFORG', 'BHEL',
     'CADILAHC','CANBK', 'CARBORUNIV', 'CASTROLIND', 'CCL', 'CEATLTD', 'CENTRALBK',
     'CENTURYPLY', 'CENTURYTEX', 'CESC', 'CIPLA', 'CNXIT', 'COALINDIA', 'COLPAL', 'CONCOR', 
     'L%26TFH', 'LICHSGFIN', 'LT', 'LTI', 'M%26M', 'M%26MFIN', 'MARICO', 'MARUTI',
     'NATIONALUM', 'NBCC', 'NCC', 'NELCAST', 'NHPC', 'NIFTY', 'NIITTECH', 'NMDC',
     'PETRONET', 'PFC', 'PHOENIXLL', 'PIDILITIND', 'PIIND', 
     'RADICO', 'RAJESHEXPO', 'RAYMOND', 'RELIANCE', 'RELINFRA', 'RENUKA', 'RPOWER',
     'SADBHAV', 'SAIL', 'SBIN', 'SCI', 'SETCO', 'SNOWMAN', 'SOBHA', 'SOUTHBANK', 'SYNDIBANK',
     'TALWALKARS', 'TATACHEM', 'TATACOMM', 'TATAELXSI', 'TATAGLOBAL', 'TATAMOTORS',  'TATAPOWER',
     'UBL', 'ULTRACEMCO', 'UNIONBANK', 'UNITECH', 'UPL', 'VAKRANGEE', 'VEDL', 'VIDEOIND', 
     'WABCOINDIA', 'WALCHANNAG', 'WIPRO', 'WOCKPHARMA', 'YESBANK', 'ZEEL']

for stock in stocks:
  if not os.path.isfile(DOWNLOAD_PATH+stock+'.csv'):
    stockfile = open(DOWNLOAD_PATH+stock+'.csv','w')
    stockfile.write('Date,Time,Open,High,Low,Close,Volume\n')
    stockfile.close()

def puller(stock, EXCHANGE, INTERVAL, DAYS, count):
    p = requests.get('http://finance.google.com/finance/getprices?q='+stock+'&x='+EXCHANGE+'&i='+INTERVAL+'&p='+DAYS+'d&f=d,c,h,l,o,v').text
    a = pd.read_csv(StringIO(p), skiprows=range(7), names =['date', 'Close', 'High', 'Low', 'Open', 'Volume'])
    
    a['Date'] = pd.to_datetime(a.date.str[1:],unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata').dt.strftime('%Y%m%d')
    a['Time'] = pd.to_datetime(a.date.str[1:],unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata').dt.strftime('%H%M%S')

    a = a[['Date','Time','Open','High','Low','Close','Volume']]
    a.to_csv(DOWNLOAD_PATH+stock+'.csv', mode='a', header=False, index=False)
    print(count, stock)
     
if __name__ == '__main__':
        pool = Pool(processes = 10)
        for stock in stocks:
            count+=1
            pool.apply_async(func=puller, args=( stock, EXCHANGE, INTERVAL, DAYS, count))
            
