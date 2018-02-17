import pandas as pd
import matplotlib.pyplot as plt

intraday = pd.read_csv('/home/nav/bhavcopy/Intraday_data/ZEEL.csv')
eod = pd.read_csv('/home/nav/bhavcopy/Intraday_data/ZEEL_eod.csv')

inp = input('Date to plot:')

tmp = intraday['Close'].groupby(intraday['Date'])
intraday['mma20'] = tmp.rolling(window=20).mean().reset_index(0,drop=True)
intraday['mma30'] = tmp.rolling(window=30).mean().reset_index(0,drop=True)

eod['Pivot'] = (eod['High'] + eod['Low'] + eod['Close'])/3
eod['R2'] = eod['Pivot'] + (eod['High'] - eod['Low'])
eod['R1'] = 2*eod['Pivot'] - eod['Low']
eod['S1'] = 2*eod['Pivot'] - eod['High']
eod['S2'] = eod['Pivot'] - (eod['High'] - eod['Low'])

eod = eod[['Date','Close','R2','R1','Pivot','S1','S2']]

# we have to shift the pivot,resistance,support values to the next day
# because the vaules we calculated on today's date will be used on the next day

eod['R2'] = eod['R2'].shift(1)
eod['R1'] = eod['R1'].shift(1)
eod['S2'] = eod['S2'].shift(1)
eod['S1'] = eod['S1'].shift(1)
eod['Pivot'] = eod['Pivot'].shift(1)

eod = eod.set_index('Date')
tmp1=intraday[['Close','mma20','mma30','mma40']].groupby(intraday['Date'])

tmp1=list(tmp1)
for i in tmp1[1:]:
    if str(i[0]) == inp:
        f = eod.loc[i[0]]
        ax = i[1].plot(figsize = (11,10) ,grid = True)
        plt.axhline(y=f.Pivot, color='r')
        plt.axhline(y=f.R1, color='r')
        plt.axhline(y=f.S1, color='r')
        fig = ax.get_figure()
        fig.savefig('/home/'+str(i[0])+'.png', bbox_inches='tight', pad_inches=0)
        plt.close(fig)
    else:
        print(inp,'not in the file')
        break
