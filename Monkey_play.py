import plotly.graph_objects as go
import plotly
import pandas as pd
import numpy as np
import random
import datetime

#Function to calculate Exponential Moving average for period 30,20 and 10
#Function will take in previouse closing price list of period and ema list.
def EMA(first_round,prev_close,period_30_list,period_20_list,period_10_list,ema_30_list,ema_20_list,ema_10_list):
    
    #This calculates the simple moving avereage
    #SMA=(period sum)/n
    sma_30=round(np.mean(period_30_list),5)
    sma_20=round(np.mean(period_20_list),5)
    sma_10=round(np.mean(period_10_list),5)
    
    #This calculates the Weighted multiplier
    #WM=2/(n+1)
    wm_30=round(2/(30+1),5)
    wm_20=round(2/(20+1),5)
    wm_10=round(2/(10+1),5)
    
    #If it is the first calculation:
    #for previouse ema, use sma value
    if first_round==True:
        ema_30_list.append(sma_30)
        ema_20_list.append(sma_20)
        ema_10_list.append(sma_10)
        
    #This selects the previouse ema value for calculation 
    prev_ema_30=ema_30_list[-1]
    prev_ema_20=ema_20_list[-1]
    prev_ema_10=ema_10_list[-1]

    #This calculate the ema value
    #EMA=(close price - previouse ema) * WM + previouse ema 
    ema_30=round((prev_close-prev_ema_30)*wm_30+prev_ema_30, 6)
    ema_20=round((prev_close-prev_ema_20)*wm_20+prev_ema_20, 6)
    ema_10=round((prev_close-prev_ema_10)*wm_10+prev_ema_10, 6)

    #add the new ema value to the list
    ema_30_list.append(ema_30)
    ema_20_list.append(ema_20)
    ema_10_list.append(ema_10)
    
    #this returns the EMA updated list  
    return ema_30_list,ema_20_list,ema_10_list


#Function to calculate pivot point and:
#Support 1,2 and 3
#Resistance 1,2 and 3
#Function takes the four prviouse o,h,l and loce priced 
def piviot_point(prev_open,prev_high,prev_low,prev_close):
    
    #piviot point formula= (Previous high+Previous Low+ Previous Close)/3
    #this is rounded to 5 decimal plcaed same for r1,r2,r3,s1,s2,s3
    p=round((prev_high+prev_low+prev_close)/3,5)
    r1=round((p*2)-prev_low,5)
    s1=round((p*2)-prev_high,5)
    r2=round(p+prev_high-prev_low,5)
    s2=round(p-prev_high+prev_low,5)
    r3=round(r1+(prev_high-prev_low),5)
    s3=round(s1-(prev_high-prev_low),5)
    
    #returns piviot point value,r1,r2,r3,s1,s2 and s3
    return p,r1,r2,r3,s1,s2,s3


text='long time no see my friend!'
print(text)

#This function will prepaer the raw test data into-
#A custom usable data frame 
def prep_test_data():
    
    #read the csv data and store in a temp defult dataframe
    df = pd.read_csv('EURUSD_M5_temp.csv')

    #count the number of rows i.e Numeber of Candle sticks
    no_rows=len(df.index)
    row=[]
    
    #This for loop will rearange each row in to the the columns below
    for i in range(no_rows):
        raw=df.iloc[i,0]
        day=raw.split()[0]
        time=raw.split()[1]
        Open=float(raw.split()[2])
        high=float(raw.split()[3])
        low=float(raw.split()[4])
        Close=float(raw.split()[5])
        row.append([day+' '+time,Open,high,low,Close])
    
    # this is now made in to a Data Frame with these columns
    data=pd.DataFrame(row,columns=['Time','Open','High','Low','Close'])

    test_data=data.head(len(data.index))
    #print(test_data)
    
    #return the new usable data frame
    return test_data

profit_log=[]

#This is main game 'the waves'
test_data=prep_test_data()
#for i in range(5):
    
#these are the counters to its respective variable 
profit=0
wins=0
loss=0
buys=0
sells=0
holdings=0

#Nutral here means: it's currently holding a buy/sell possition 
nutral=False

first_round=True
#store the result total profit for each cycle
money_log=[]

#Initialise lists for EMA function
#this is a list of the first 30 or 20 or 10 closing price 
period_30_list=test_data.iloc[0:30,4].to_list()
period_20_list=test_data.iloc[10:30,4].to_list()
period_10_list=test_data.iloc[20:30,4].to_list()

#Initialise lists for EMA function 
#this will store all the calculated ema values
ema_30_list=[]
ema_20_list=[]
ema_10_list=[]

#list for candle stick
time_cs=[]
open_cs=[]
high_cs=[]
low_cs=[]
close_cs=[]

#start timer
start= datetime.datetime.now()


#This loop goes through each row of the test_data i.e each candle stick.
#The loop will start from the second candle stick as the previouse is needed-
#to calculate pivot point 
for i in range(31,len(test_data.index)-1):

    #Set the variables of the previouse open,high,low and close pices
    #If it is the first loob grab the 1st candle stick
    if first_round==True:
        prev_open=test_data.iloc[i-1,1]
        prev_high=test_data.iloc[i-1,2]
        prev_low=test_data.iloc[i-1,3]
        prev_close=test_data.iloc[i-1,4]
        
        
    else:
        prev_open=test_data.iloc[i,1]
        prev_high=test_data.iloc[i,2]
        prev_low=test_data.iloc[i,3]
        prev_close=test_data.iloc[i,4]
        
    
    p,r1,r2,r3,s1,s2,s3=piviot_point(prev_open,prev_high,prev_low,prev_close)
    

    #Set the variables for the present open,high,low and close prices
    high_p=test_data.iloc[i,2]
    low_p=test_data.iloc[i,3]
    open_p=test_data.iloc[i,1]
    close_p=test_data.iloc[i,4]

    #Set the variables for the future open,high,low and close prices
    #This is to simulate the real future price movement and compare-
    #current possiotion againaset future prices
    f_high_p=test_data.iloc[i+1,2]
    f_low_p=test_data.iloc[i+1,3]
    f_open_p=test_data.iloc[i+1,1]
    f_close_p=test_data.iloc[i+1,4]

    #Updated then list for candlestick
    time_cs.append(test_data.iloc[i+1,0])
    open_cs.append(test_data.iloc[i+1,1])
    high_cs.append(test_data.iloc[i+1,2])
    low_cs.append(test_data.iloc[i+1,3])
    close_cs.append(test_data.iloc[i+1,4])
    
    #this calles the the EMA function and
    #recives the new updated ema list
    ema_30_list,ema_20_list,ema_10_list=EMA(first_round,prev_close,period_30_list,period_20_list,period_10_list,
                                            ema_30_list,ema_20_list,ema_10_list)
    
    #This preps the updated list of closing prices for the next loop
    #remove the oldest closing price
    period_30_list.pop(0)
    period_20_list.pop(0)
    period_10_list.pop(0)
    #and add the new closing price
    period_30_list.append(prev_close)
    period_20_list.append(prev_close)
    period_10_list.append(prev_close)

    #if i==0:

    #If no open possitions:
    if nutral==False:

        #Set the price to a random price between the current highest and lowest price
        #This wil simulate real life price before buying or selling 
        price=round(random.uniform(high_p,low_p),5)
        print('\nPrice= ', price)

        #Aray of buy or sell and randomly choese one command 
        acc=['buy','sell']
        action=random.choice(acc)
        print(action)

        #counter for buy and sell
        if action=='buy':
            buys+=1
        if action=='sell':
            sells+=1
    #If we still have an open possition hold
    #This will save the current action for price comparison down bellow
    else:
        action=action
        holdings+=1
        print('\nPrice= ', price)
        print('\nHolding ',action)
    

    #If a buy possion is opened:
    #Set Take profit and stop lose prices
    #Compare tp and sp vs future prices to determine if win or losse
    #if win or lose then set the new price betewen current high and low
    #swithc on the holding state
    if action=='buy':

        #In a normal trading account the buy price is offseted by 0.00013 from real price
        #In a demo trading account the buy price is offseted by 0.00015 from real price
        #In a 0.1 trade volume a 0.0001 move will equal to $1 or
        #a move of 0.00001 will eqaul to $0.1
        #So take profit is set at Current real price + offset of 0.00013 + 0.0005 equivilant to $5
        tp=round(price + 0.00013 + 0.0005,5)
        sp=round(price - 0.00013 - 10.0015,5)

#            print('TP= ',tp)
#           print('SP= ',sp)

        #Compare stop lose price with future open,low and close price
        #If higher, close possition with a loss and set new price
        if f_open_p <= sp or f_low_p <= sp or f_close_p <= sp:

            money_log.append(profit)
            profit -= 15
#                print('LOSS $15! Profit= ', profit)
            #switch off holding state
            nutral=False
            loss+=1
            price=round(random.uniform(high_p,low_p),5)

        #Compare take profit price with future open,high and close price
        #If lower, close possition and take profit and set new price
        elif f_open_p >= tp or f_high_p >= tp or f_close_p >= tp:

            money_log.append(profit)
            profit +=5
            print('WIN $5! Profit= ', profit)
            #switch off holding state
            nutral=False
            wins+=1
            price=round(random.uniform(high_p,low_p),5)

        #If none of the above:
        #swithc on the holding state
        #and keep the buying pice
        else:
#                print('No win No loss! Profit= ', profit)
            nutral=True
            money_log.append(profit)
            price=price

    #If a sell possion is opened:
    #Set Take profit and stop lose prices
    #Compare tp and sp vs future prices to determine if win or losse
    #if win or lose then set the new price betewen current high and low
    #swithc on the holding state
    if action=='sell':

        #In a normal trading account the buy price is offseted by 0.00007 from real price
        #In a demo trading account the buy price is offseted by 0.00008 from real price
        #In a 0.1 trade volume a 0.0001 move will equal to $1 or
        #a move of 0.00001 will eqaul to $0.1
        #So take profit is set at Current real price - offset of 0.00007 - 0.0005 equivilant to $5
        tp=round(price - 0.00007 - 0.0005,5)
        sp=round(price + 0.00007 + 10.0015,5)

#            print('TP= ',tp)
#           print('SP= ',sp)

        #Compare stop lose price with future open,low and close price
        #If lower, close possition with a loss and set new price
        if f_open_p >= sp or f_high_p >= sp or f_close_p >= sp:

            money_log.append(profit)
            profit -= 15
#                print('LOSS $15! Profit= ', profit)
            nutral=False
            loss+=1
            price=round(random.uniform(high_p,low_p),5)

        #Compare take profit price with future open,high and close price
        #If lower, close possition and take profit and set new price
        elif f_open_p <= tp or f_low_p <= tp or f_close_p <= tp:

            money_log.append(profit)
            profit +=5
            print('WIN $5! Profit= ', profit)
            nutral=False
            wins+=1
            price=round(random.uniform(high_p,low_p),5)

        else:

            print('No win No loss! Profit= ', profit)
            nutral=True
            money_log.append(profit)
            price=price
        
        first_round=False
        
    print('**********************************************************')
    print(i,' Data= ',test_data.iloc[i,])

    print('\nTP= ',tp)

    print('\no=',round(tp-f_open_p,5),' ','h=',round(tp-f_high_p,5),' ','l=',round(tp-f_low_p,5),' ','c=',round(tp-f_close_p,5))

    print('\nR3= ',r3)
    print('R2= ',r2)
    print('R1= ',r1)
    print('PV= ',p)
    print('S1= ',s1)
    print('S2= ',s2)
    print('S3= ',s3)

    print('\nEMA 30= ',ema_30_list[-1])
    print('EMA 20= ',ema_20_list[-1])
    print('EMA 10= ',ema_10_list[-1])

    print('**********************************************************')

    fig=go.Figure(data=[go.Candlestick(x=time_cs, open=open_cs, high=high_cs, low=low_cs, close=close_cs),
                   go.Scatter(x=time_cs, y=ema_30_list[1:], line=dict(color='yellow', width=1)),
                   go.Scatter(x=time_cs, y=ema_20_list[1:], line=dict(color='green', width=1)),
                   go.Scatter(x=time_cs, y=ema_10_list[1:], line=dict(color='blue', width=1))])

    fig.add_hline(y=tp, x0=0,x1=1, annotation_text='TP= '+str(tp),annotation_position="top right")
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()



    
profit_log.append(profit)
end= datetime.datetime.now()

print('\n/////////////////////////////////////////////////////')
print('\nBuys= ',buys)
print('\nSells= ',sells)
print('\nHolds= ',holdings)
print('\nWins= ',wins,'  ', round((wins/(buys+sells))*100 , 1),'%')
print('\nLosses= ',loss,'  ',round((loss/(buys+sells))*100,1),'%')
print('\nProfit= $',profit)
print('\nTime Lapseg= ',end-start)
print('/////////////////////////////////////////////////////')
profit=0

print('\nProfit Log= ',profit_log)

#print(money_log[99875])
#print(money_log)
