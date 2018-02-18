import requests, os, pandas as pd
from io import StringIO
from multiprocessing import Pool

NO_OF_DAYS = input('Enter no. of days to pull:') #google doesnt give more than 15 days of data
EXCHANGE = 'NSE'
INTERVAL = '61'  # 61 for 1 minute(60+1) , 601 for 10 minutes(600+1) , 301 for 5 minutes etc(300+1), 
                 # 1 is added to get the timestamp data for parsing
DOWNLOAD_PATH = '/home/LTP/'

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
     'RAYMOND', 'RELIANCE', 'RELINFRA', 'RENUKA', 'RPOWER',
     'SADBHAV', 'SAIL', 'SBIN', 'SCI', 'SETCO', 'SNOWMAN', 
     'TALWALKARS', 'TATACHEM', 'TATACOMM', 'TATAELXSI', 'TATAMOTORS',  'TATAPOWER',
     'UBL', 'ULTRACEMCO', 'UNIONBANK', 'UNITECH', 'UPL', 'VAKRANGEE', 
     'WABCOINDIA', 'WALCHANNAG', 'WIPRO', 'WOCKPHARMA', 'YESBANK', 'ZEEL']

for stock in stocks:
  if not os.path.isfile(DOWNLOAD_PATH+stock+'.csv'):
    stockfile = open(DOWNLOAD_PATH+stock+'.csv','w')
    stockfile.write('Date,Time,Open,High,Low,Close,Volume\n')
    stockfile.close()

def puller(STOCK, NO_OF_DAYS,WRITE_TO_FILE=True):
    p = requests.get('http://finance.google.com/finance/getprices?q='+STOCK+'&x='+EXCHANGE+'&i='+INTERVAL+'&p='+NO_OF_DAYS+'d&f=d,c,h,l,o,v').text
    a = pd.read_csv(StringIO(p), skiprows=range(7), names =['date', 'Close', 'High', 'Low', 'Open', 'Volume'])
    
    a['Date'] = pd.to_datetime(a.date.str[1:],unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata').dt.strftime('%Y%m%d')
    a['Time'] = pd.to_datetime(a.date.str[1:],unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata').dt.strftime('%H%M%S')

    a = a[['Date','Time','Open','High','Low','Close','Volume']]
    
    if WRITE_TO_FILE:
      a.to_csv(DOWNLOAD_PATH+stock+'.csv', mode='a', header=False, index=False)
      print(STOCK)
    else:
      return a
     
if __name__ == '__main__':
        pool = Pool(processes = 10)
        for STOCK in stocks:
            pool.apply_async(func=puller, args=(STOCK, NO_OF_DAYS, EXCHANGE, INTERVAL))
            
