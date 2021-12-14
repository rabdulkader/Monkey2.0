import pandas as pd
import random
import datetime

#Function to calculate pivot point and:
#Support 1 and 2
#Resistance 1 and 2
#Function takes the four prviouse o,h,l and loce priced 
def piviot_point(prev_open,prev_high,prev_low,prev_close):
    
    #piviot point formula= (Previous high+Previous Low+ Previous Close)/3
    #this is rounded to 5 decimal plcaed same for r1,r2,s1,s2
    p=round((prev_high+prev_low+prev_close)/3,5)
    r1=round((p*2)-prev_low,5)
    r2=round(p+prev_high-prev_low,5)
    s1=round((p*2)-prev_high,5)
    s2=round(p-prev_high+prev_low,5)
    
    #returns piviot point value,r1,r2,s1 and s2
    return p,r1,r2,s1,s2


text='long time no see my friend!'
print(text)

#This function will prepaer the raw test data into-
#A custom usable data frame 
def prep_test_data():
    
    #read the csv data and store in a temp defult dataframe
    df = pd.read_csv('EURUSD_M5_2019_2020.csv')

    #count the number of rows i.e Numeber of Candle sticks
    no_rows=len(df.index)
    row=[]
    
    #This for loop will rearange each row in to the the columns below
    for i in range(no_rows):
        raw=df.iloc[i,0]
        time=raw.split()[1]
        Open=float(raw.split()[2])
        high=float(raw.split()[3])
        low=float(raw.split()[4])
        Close=float(raw.split()[5])
        row.append([time,Open,high,low,Close])
    
    # this is now made in to a Data Frame with these columns
    data=pd.DataFrame(row,columns=['Time','Open','High','Low','Close'])

    test_data=data.head(len(data.index))
    #print(test_data)
    
    #return the new usable data frame
    return test_data

profit_log=[]

#This is main game 'the waves'
test_data=prep_test_data()
for i in range(5):
    
    #these are the counters to its respective variable 
    profit=0
    wins=0
    loss=0
    buys=0
    sells=0
    holdings=0
    
    #Nutral here means: it's currently holding a buy/sell possition 
    nutral=False
    
    #store the result total profit for each cycle
    money_log=[]
    
    #start timer
    start= datetime.datetime.now()
    
    #This loop goes through each row of the test_data i.e each candle stick.
    #The loop will start from the second candle stick as the previouse is needed-
    #to calculate pivot point 
    for i in range(1,len(test_data.index)-1):
        
        #Set the variables of the previouse open,high,low and close pices
        #If it is the first loob grab the 1st candle stick
        if i==1:
            prev_open=test_data.iloc[i-1,1]
            prev_high=test_data.iloc[i-1,2]
            prev_low=test_data.iloc[i-1,3]
            prev_close=test_data.iloc[i-1,4]
            
        else:
            prev_open=test_data.iloc[i,1]
            prev_high=test_data.iloc[i,2]
            prev_low=test_data.iloc[i,3]
            prev_close=test_data.iloc[i,4]



#        print('*************************************************')
 #       print(i,'  ',test_data.iloc[i,])

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

        #if i==0:
        
        #If no open possitions:
        if nutral==False:
            
            #Set the price to a random price between the current highest and lowest price
            #This wil simulate real life price before buying or selling 
            price=round(random.uniform(high_p,low_p),5)
#            print('\nPrice= ', price)
 #           print('\n'+"Buy b or Sell s? \n")
            
            ###########################################
            #            action=input()
            #            p,r1,r2,s1,s2=piviot_point(prev_open,prev_high,prev_low,prev_close)
              #          if (price > p and price < r1) or (price > r1 and price < r2) :
               #             action='b'
                 #       elif (price < p and price > s1) or (price < s1 and price > s2):
                  #          action='s'
                    #    else:
            ############################################
            
            #Aray of buy or sell and randomly choese one command 
            acc=['buy','sell']
            action=random.choice(acc)
#            print(action)
            
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
#            print('\nPrice= ', price)
 #           print('\nHolding ',action)
        
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
#                print('WIN $5! Profit= ', profit)
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
#                print('WIN $5! Profit= ', profit)
                nutral=False
                wins+=1
                price=round(random.uniform(high_p,low_p),5)

            else:
                
#                print('No win No loss! Profit= ', profit)
                nutral=True
                money_log.append(profit)
                price=price
            
#        print('*************************************************')
#        print('o=',round(tp-f_open_p,5),' ','h=',round(tp-f_high_p,5),' ','l=',round(tp-f_low_p,5),' ','c=',round(tp-f_close_p,5))
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
